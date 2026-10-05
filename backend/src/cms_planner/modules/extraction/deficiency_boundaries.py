"""Identify evidence-linked F-tag and SOD boundaries in ordered pages."""

import re
from dataclasses import dataclass, field

from pydantic import BaseModel, ConfigDict, Field

from cms_planner.domain.cms_layout import CmsLayout, CmsLayoutStatus
from cms_planner.domain.text_span import ClassifiedPageText


# Accept common CMS tag representations with any single-letter prefix,
# anchored to the start of a line to avoid false matches on abbreviations
# like "BP 180" or "RN 2" within SOD body text.
#
# F880  L532  K123
# F 880  L 532
# F-880  F.880  L-532, including common Unicode dash substitutions from OCR.
_F_TAG = re.compile(
    r"^[{[(]?\s*([A-Z])\s*[.\-\u2010-\u2015 ]?\s*(\d{3,6})\b\s*[])}]?",
    re.IGNORECASE,
)

_EMPTY_SOD = re.compile(
    r"^\s*(?:SOD|SUMMARY OF DEFICIENCIES)\s*:?\s*$",
    re.IGNORECASE,
)

_CONTINUATION = re.compile(
    r"(?:continued?|cont\.?|cont['’]d)\s+from\s+(?:page|p(?:g)?\.?)\s*\d+",
    re.IGNORECASE,
)

_PAGE_HEADER = re.compile(
    r"^(?:PRINTED:|FORM APPROVED|STATEMENT OF DEFICIENCIES|AND PLAN OF CORRECTION|"
    r"\(X[1-6]\)|PROVIDER/SUPPLIER|IDENTIFICATION NUMBER|NAME OF PROVIDER|"
    r"STREET ADDRESS|SUMMARY STATEMENT OF DEFICIENCIES|EACH DEFICIENCY MUST|"
    r"ID\s+PREFIX|PREFIX\s+TAG|PROVIDER.S PLAN OF CORRECTION|EACH CORRECTIVE|"
    r"CROSS-REFERENCED|COMPLETE\s+DATE|Health Facilities|LABORATORY DIRECTOR|"
    r"STATE FORM|If continuation sheet|"
    r"Colorado\s+De?[a-z]*\s+(?:of|Department)|"  # Colorado Dept of Public Health
    r"\(EACH\s+(?:DEFICIENCY|CORRECTIVE)|REGULATORY\s+OR\s+LSC|"
    r"CROSS.REFERENCED\s+TO|CORRECTIVE\s+ACTION\s+SHOULD|"
    r"[A-Z][A-Z ]+DIALYSIS\s+CENTER|"             # facility name line
    r"DEFICIENCY\))",                              # lone column header fragment
    re.IGNORECASE,
)

# Short standalone lines that are repeating CMS-2567 form column headers or
# metadata fragments — not SOD content. Matched against the full stripped line.
_FORM_FRAGMENT = re.compile(
    r"^(?:"
    r"\d{4,}|"                          # pure numbers like 6899
    r"(?![A-Z]0{1,2}\d{4}$)[A-Z]\d{5,}|" # form codes, excluding padded tags
    r"(?![A-Z](?:\d{3,4}|0{1,2}\d{4})$)[A-Z0-9]{4,}X?|" # exclude tags
    r"A\.\s*BUILDING[:\s]*|"            # A. BUILDING:
    r"B\.?\s*WING[:\s]*|"               # B.WING
    r"CONSTRUCTION[:\s]*|"              # CONSTRUCTION
    r"COMPLETED[:\s]*|"                 # COMPLETED
    r"\d{2}/\d{2}/\d{4}|"              # dates like 04/10/2024
    r"PREFIX[:\s]*|"                    # PREFIX
    r"TAG[:\s]*|"                       # TAG
    r"DATE[:\s]*|"                      # DATE
    r"TITLE[:\s]*|"                     # TITLE
    r"ID[:\s]*|"                        # ID
    r"\d{3,5}\s+[A-Z]\s+\w+|"         # street numbers like 1057 S WADSWORTH
    r"[A-Z ,\.]+,\s*[A-Z]{2}\s+\d+|"  # city/state/zip like LAKEWOOD, CO 802
    r"BLVD|"                            # BLVD alone
    r"\d+\s*$"                          # lone numbers like 26
    r")$",
    re.IGNORECASE,
)


_INITIAL_COMMENTS = re.compile(
    r"^Initial\s+Comments\s*$",
    re.IGNORECASE,
)

_DEFICIENCIES_CITED = re.compile(
    r"\b(?:no|one|\d+)\s+deficienc(?:y|ies)\s+(?:was|were)\s+cited\b",
    re.IGNORECASE,
)

_LIFE_SAFETY_SECTION = re.compile(r"\bLIFE\s+SAFETY\s+CODE\b", re.IGNORECASE)
_NFPA_HEADING = re.compile(r"^NFPA\s+\d+[A-Z.-]*$", re.IGNORECASE)


class BoundaryEvidence(BaseModel):
    """Source text retained for one page of a deficiency boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    page_number: int = Field(ge=1)
    text: str = Field(min_length=1)


class DeficiencyBoundary(BaseModel):
    """One independently identified F-tag and its bounded SOD text."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    boundary_id: str = Field(min_length=1)
    f_tag: str = Field(pattern=r"^[A-Z]\d{4}$")
    sod_text: str | None
    evidence: tuple[BoundaryEvidence, ...] = Field(min_length=1)
    complete: bool
    uncertainty: bool
    confirmed: bool


@dataclass
class _BoundaryDraft:
    ordinal: int
    f_tag: str
    evidence_lines: list[tuple[int, str]] = field(default_factory=list)
    sod_lines: list[str] = field(default_factory=list)
    continuation_page_numbers: set[int] = field(default_factory=set)


def identify_deficiency_boundaries(
    layout: CmsLayout,
    pages: tuple[ClassifiedPageText, ...],
) -> tuple[DeficiencyBoundary, ...]:
    """Return one ordered boundary per F-tag for recognized CMS-2567 pages."""

    if layout.status is CmsLayoutStatus.UNRECOGNIZED:
        return ()

    completed: list[DeficiencyBoundary] = []
    current: _BoundaryDraft | None = None

    for page in pages:
        page_content_started = False
        page_lines = _normalize_header_tag_order(_page_lines(page))

        for line_index, line in enumerate(page_lines):
            current = _consume_line(
                completed,
                current,
                page.page_number,
                line,
                starts_page=not page_content_started,
                ends_page=line_index == len(page_lines) - 1,
                next_line=(
                    page_lines[line_index + 1]
                    if line_index + 1 < len(page_lines)
                    else None
                ),
            )

            cleaned = line.strip()
            if not (_PAGE_HEADER.search(cleaned) or _FORM_FRAGMENT.match(cleaned)):
                page_content_started = True

    if current is not None:
        completed.append(_finish(current))

    return _coalesce_by_tag(completed)


def _coalesce_by_tag(
    boundaries: list[DeficiencyBoundary],
) -> tuple[DeficiencyBoundary, ...]:
    grouped: dict[str, list[DeficiencyBoundary]] = {}

    for boundary in boundaries:
        grouped.setdefault(boundary.f_tag, []).append(boundary)

    coalesced: list[DeficiencyBoundary] = []
    for ordinal, same_tag in enumerate(grouped.values(), start=1):
        sod_parts = [
            boundary.sod_text
            for boundary in same_tag
            if boundary.sod_text is not None
        ]
        sod_text = "\n".join(dict.fromkeys(sod_parts)).strip() or None
        evidence_lines = [
            (evidence.page_number, evidence.text)
            for boundary in same_tag
            for evidence in boundary.evidence
        ]

        coalesced.append(
            DeficiencyBoundary(
                boundary_id=f"cms-2567:{ordinal:04d}",
                f_tag=same_tag[0].f_tag,
                sod_text=sod_text,
                evidence=_group_evidence(evidence_lines),
                complete=sod_text is not None,
                uncertainty=sod_text is None,
                confirmed=False,
            )
        )

    return tuple(coalesced)


def _normalize_header_tag_order(lines: tuple[str, ...]) -> tuple[str, ...]:
    """Move a prefetched deficiency tag after its Initial Comments summary."""

    lines = _normalize_prefetched_life_safety_tag(lines)
    lines = _normalize_prefetched_regulatory_heading(lines)

    for index in range(len(lines) - 1):
        zero_match = _F_TAG.fullmatch(lines[index])
        deficiency_match = _F_TAG.fullmatch(lines[index + 1])
        if (
            zero_match is None
            or deficiency_match is None
            or _normalize_tag_number(zero_match.group(2)) != "0000"
            or _normalize_tag_number(deficiency_match.group(2)) == "0000"
        ):
            continue

        saw_initial_comments = False
        for summary_end in range(index + 2, len(lines)):
            if _F_TAG.fullmatch(lines[summary_end]) is not None:
                break
            saw_initial_comments = saw_initial_comments or bool(
                _INITIAL_COMMENTS.fullmatch(lines[summary_end])
            )
            if saw_initial_comments and _DEFICIENCIES_CITED.search(lines[summary_end]):
                return (
                    lines[:index + 1]
                    + lines[index + 2:summary_end + 1]
                    + (lines[index + 1],)
                    + lines[summary_end + 1:]
                )

    return lines


def _normalize_prefetched_regulatory_heading(
    lines: tuple[str, ...],
) -> tuple[str, ...]:
    for tag_index, line in enumerate(lines):
        tag = _line_tag(line)
        if tag is None or tag.endswith("0000"):
            continue

        heading_start = next(
            (
                index
                for index in range(max(0, tag_index - 3), tag_index)
                if _NFPA_HEADING.fullmatch(lines[index])
            ),
            None,
        )
        if heading_start is not None:
            return (
                lines[:heading_start]
                + (line,)
                + lines[heading_start:tag_index]
                + lines[tag_index + 1:]
            )

    return lines


def _normalize_prefetched_life_safety_tag(
    lines: tuple[str, ...],
) -> tuple[str, ...]:
    for index in range(len(lines) - 1):
        emergency_tag = _line_tag(lines[index])
        life_safety_tag = _line_tag(lines[index + 1])
        if emergency_tag != "E0000" or life_safety_tag != "K0000":
            continue

        for section_start in range(index + 2, len(lines)):
            if _LIFE_SAFETY_SECTION.search(lines[section_start]):
                return (
                    lines[:index + 1]
                    + lines[index + 2:section_start]
                    + (lines[index + 1],)
                    + lines[section_start:]
                )

    return lines


def _consume_line(
    completed: list[DeficiencyBoundary],
    current: _BoundaryDraft | None,
    page_number: int,
    line: str,
    *,
    starts_page: bool,
    ends_page: bool,
    next_line: str | None,
) -> _BoundaryDraft | None:
    cleaned = line.strip()

    if not cleaned:
        return current

    if _PAGE_HEADER.search(cleaned) or _FORM_FRAGMENT.match(cleaned):
        return current

    match = _F_TAG.search(cleaned)

    if match:
        prefix = match.group(1).upper()
        number = _normalize_tag_number(match.group(2))
        tag = f"{prefix}{number}"
        rest = cleaned[match.end():].strip()

        if number == "0000":
            if current is None:
                return _start_boundary(
                    ordinal=len(completed) + 1,
                    page_number=page_number,
                    line=cleaned,
                    match=match,
                )
            if current.f_tag == tag:
                return current
            if not current.f_tag.endswith("0000") and _line_tag(next_line) == current.f_tag:
                return current
            completed.append(_finish(current))
            return _start_boundary(
                ordinal=len(completed) + 1,
                page_number=page_number,
                line=cleaned,
                match=match,
            )

        # Skip continuation headers: "L 532 Continued From page N"
        if _CONTINUATION.search(rest) and current is not None and current.f_tag == tag:
            current.continuation_page_numbers.add(page_number)
            return current

        if starts_page and current is not None and current.f_tag == tag:
            current.evidence_lines.append((page_number, cleaned))
            if rest:
                current.sod_lines.append(rest)
            return current

        if ends_page and not rest and current is not None and current.f_tag == tag:
            return current

        # Skip bare footer tag that repeats the already-open boundary
        # e.g. "L 532" alone at the bottom of each continuation page
        if (
            not rest
            and current is not None
            and current.f_tag == tag
            and page_number in current.continuation_page_numbers
        ):
            return current

        if current is not None:
            completed.append(_finish(current))

        return _start_boundary(
            ordinal=len(completed) + 1,
            page_number=page_number,
            line=cleaned,
            match=match,
        )

    if current is not None:
        current.evidence_lines.append(
            (page_number, cleaned)
        )

        current.sod_lines.append(cleaned)

    return current


def _line_tag(line: str | None) -> str | None:
    if line is None:
        return None
    match = _F_TAG.fullmatch(line.strip())
    if match is None:
        return None
    return f"{match.group(1).upper()}{_normalize_tag_number(match.group(2))}"


def _normalize_tag_number(number: str) -> str:
    return number[-4:].zfill(4)


def _page_lines(page: ClassifiedPageText) -> tuple[str, ...]:
    lines: list[str] = []

    for span in page.spans:
        for line in span.text.splitlines():
            cleaned = line.strip()

            if cleaned:
                lines.append(cleaned)

    return tuple(lines)


def _start_boundary(
    ordinal: int,
    page_number: int,
    line: str,
    match: re.Match[str],
) -> _BoundaryDraft:
    prefix = match.group(1).upper()
    number = _normalize_tag_number(match.group(2))
    f_tag = f"{prefix}{number}"

    draft = _BoundaryDraft(
        ordinal=ordinal,
        f_tag=f_tag,
    )

    draft.evidence_lines.append(
        (page_number, line)
    )

    # Preserve any text appearing after the F-tag.
    trailing_text = line[match.end():].strip()

    if trailing_text:
        draft.sod_lines.append(trailing_text)

    return draft


def _finish(draft: _BoundaryDraft) -> DeficiencyBoundary:
    sod_text = "\n".join(draft.sod_lines).strip() or None

    if sod_text is not None and _EMPTY_SOD.fullmatch(sod_text):
        sod_text = None

    complete = sod_text is not None

    return DeficiencyBoundary(
        boundary_id=f"cms-2567:{draft.ordinal:04d}",
        f_tag=draft.f_tag,
        sod_text=sod_text,
        evidence=_group_evidence(draft.evidence_lines),
        complete=complete,
        uncertainty=not complete,
        confirmed=False,
    )


def _group_evidence(
    lines: list[tuple[int, str]],
) -> tuple[BoundaryEvidence, ...]:
    grouped: dict[int, list[str]] = {}

    for page_number, text in lines:
        page_lines = grouped.setdefault(page_number, [])
        if text not in page_lines:
            page_lines.append(text)

    return tuple(
        BoundaryEvidence(
            page_number=page_number,
            text="\n".join(page_lines),
        )
        for page_number, page_lines in sorted(grouped.items())
    )
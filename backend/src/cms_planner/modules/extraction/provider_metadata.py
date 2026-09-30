"""Extract evidence-linked provider identity from CMS-2567 headers."""

import re
from dataclasses import dataclass

from cms_planner.domain.text_span import ClassifiedPageText


_NUMBER_LABEL = re.compile(
    r"(?:PROVIDER/SUPPLIER/CLIA\s+)?IDENTIFICATION\s+NUMBER\s*:?\s*(.*)$",
    re.IGNORECASE,
)
_NAME_LABEL = re.compile(
    r"NAME\s+OF\s+PROVIDER\s+OR\s+SUPPLIER\s*:?\s*(.*)$",
    re.IGNORECASE,
)
_PROVIDER_NUMBER = re.compile(r"^[A-Z0-9][A-Z0-9-]{3,15}$", re.IGNORECASE)
_HEADER_LINE = re.compile(
    r"^(?:\(X\d+\)|STREET\s+ADDRESS|CITY,?\s+STATE|SUMMARY\s+STATEMENT|"
    r"ID\s+PREFIX|PREFIX\s+TAG|FORM\s+CMS|STATEMENT\s+OF\s+DEFICIENCIES)",
    re.IGNORECASE,
)
_CITY_STATE_ZIP = re.compile(r",\s*[A-Z]{2}\s+\d{3,}", re.IGNORECASE)


@dataclass(frozen=True)
class ProviderMetadata:
    provider_name: str
    provider_number: str
    page_number: int
    evidence_text: str


def extract_provider_metadata(
    pages: tuple[ClassifiedPageText, ...],
) -> ProviderMetadata | None:
    """Return provider identity from the first header containing both values."""

    for page in pages:
        lines = _page_lines(page)
        provider_number = _extract_provider_number(lines)
        provider_name = _extract_provider_name(lines)
        if provider_name is not None and provider_number is not None:
            return ProviderMetadata(
                provider_name=provider_name,
                provider_number=provider_number,
                page_number=page.page_number,
                evidence_text="\n".join(lines),
            )

    return None


def _extract_provider_number(lines: tuple[str, ...]) -> str | None:
    for index, line in enumerate(lines):
        match = _NUMBER_LABEL.search(line)
        if match is None:
            continue

        inline_value = match.group(1).strip()
        if _PROVIDER_NUMBER.fullmatch(inline_value):
            return inline_value.upper()

        for candidate in lines[index + 1:index + 6]:
            if _HEADER_LINE.search(candidate):
                continue
            if _PROVIDER_NUMBER.fullmatch(candidate):
                return candidate.upper()

    return None


def _extract_provider_name(lines: tuple[str, ...]) -> str | None:
    for index, line in enumerate(lines):
        match = _NAME_LABEL.search(line)
        if match is None:
            continue

        inline_value = match.group(1).strip()
        if _is_provider_name(inline_value):
            return inline_value

        candidates: list[str] = []
        for candidate in lines[index + 1:]:
            if candidate.upper().startswith("(X4)"):
                break
            if _is_provider_name(candidate):
                candidates.append(candidate)

        if candidates:
            return max(candidates, key=len)

    return None


def _is_provider_name(value: str) -> bool:
    if not value or _HEADER_LINE.search(value):
        return False
    if any(character.isdigit() for character in value):
        return False
    if _CITY_STATE_ZIP.search(value):
        return False
    return len(value.split()) >= 2


def _page_lines(page: ClassifiedPageText) -> tuple[str, ...]:
    return tuple(
        cleaned
        for span in page.spans
        for line in span.text.splitlines()
        if (cleaned := line.strip())
    )
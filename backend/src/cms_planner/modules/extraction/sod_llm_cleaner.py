"""Use the configured LLM to clean raw SOD text and suggest per-point POC drafts."""

import json
import re
from dataclasses import dataclass, field

import httpx

_BOILERPLATE = re.compile(
    r"^(?:"
    r"PRINTED:.*|FORM\s+APPROVED.*|STATE\s+FORM.*|If\s+continuation\s+sheet.*|"
    r"Health\s+Facilities.*|LABORATORY\s+DIRECTOR.*|"
    r"Colorado\s+De?[a-z]*\s+(?:of|Department|De).*|"
    r"[A-Z][A-Z ]+DIALYSIS\s+CENTER.*|[A-Z][A-Z ]+CROSSING.*|"
    r"\(X[1-6]\).*|PROVIDER/SUPPLIER.*|IDENTIFICATION\s+NUMBER.*|"
    r"NAME\s+OF\s+PROVIDER.*|STREET\s+ADDRESS.*|"
    r"SUMMARY\s+STATEMENT.*|EACH\s+DEFICIENCY.*|REGULATORY\s+OR\s+LSC.*|"
    r"ID\s+PREFIX.*|PREFIX\s+TAG.*|PROVIDER.S\s+PLAN.*|EACH\s+CORRECTIVE.*|"
    r"CROSS.REFERENCED.*|COMPLETE\s+DATE.*|CORRECTIVE\s+ACTION\s+SHOULD.*|"
    r"A\.\s*BUILDING.*|B\.?\s*WING.*|CONSTRUCTION\s*|COMPLETED\s*|"
    r"\d{2}/\d{2}/\d{4}|[A-Z]\d{5,}|\d{4,5}X?|\d{4,}|\d+\s*|"
    r"\d{3,5}\s+[A-Z]\s+\w+.*|[A-Z ,\.]+,\s*[A-Z]{2}\s+\d+.*|BLVD\s*"
    r")$",
    re.IGNORECASE,
)

# Matches numbered sub-points: "1.", "A.", "i.", "a.", "B.", "ii.", "1)", "A)"
# Anchored to start of line so mid-sentence abbreviations are not matched.
_NUMBERED_POINT = re.compile(
    r"^((?:\d+|[A-Z]|[ivxlcdm]+)\.(?:\s|$)|(?:\d+|[A-Z])\)(?:\s|$))",
    re.IGNORECASE,
)

_EXCESS_BLANK = re.compile(r"\n{3,}")


@dataclass
class SodPoint:
    """One numbered sub-point within a deficiency SOD."""
    label: str          # e.g. "1.", "A.", "i.", "a."
    text: str           # full narrative text of this point


@dataclass
class PreprocessedSod:
    """Cleaned SOD text split into individually addressable points."""
    intro: str                          # text before the first numbered point
    points: list[SodPoint]              # ordered numbered sub-points
    is_initial_comments: bool

    @property
    def full_text(self) -> str:
        """Reassemble into a single readable string."""
        parts = [self.intro] if self.intro else []
        for p in self.points:
            parts.append(f"{p.label} {p.text}")
        return "\n\n".join(parts).strip()


def preprocess_sod_text(raw_text: str, f_tag: str = "") -> PreprocessedSod:
    """Strip boilerplate, deduplicate, then split into numbered sub-points."""
    # --- strip boilerplate and deduplicate ---
    lines = raw_text.splitlines()
    seen: set[str] = set()
    cleaned: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if _BOILERPLATE.match(stripped):
            continue
        if stripped in seen:
            continue
        seen.add(stripped)
        cleaned.append(stripped)

    clean_text = _EXCESS_BLANK.sub("\n\n", "\n".join(cleaned)).strip()
    tag_number = f_tag[1:] if len(f_tag) > 1 else ""
    is_initial = (
        bool(tag_number)
        and set(tag_number) == {"0"}
    ) or "Initial Comments" in clean_text[:120]

    # --- split into numbered sub-points ---
    intro_lines: list[str] = []
    points: list[SodPoint] = []
    current_label: str | None = None
    current_lines: list[str] = []

    for line in clean_text.splitlines():
        m = _NUMBERED_POINT.match(line.strip())
        if m:
            if current_label is not None:
                points.append(SodPoint(label=current_label, text=" ".join(current_lines).strip()))
            elif current_lines:
                intro_lines.extend(current_lines)
            current_label = m.group(1).strip()
            remainder = line.strip()[len(m.group(0)):].strip()
            current_lines = [remainder] if remainder else []
        else:
            current_lines.append(line.strip())

    # flush last open point or remaining intro
    if current_label is not None:
        points.append(SodPoint(label=current_label, text=" ".join(current_lines).strip()))
    else:
        intro_lines.extend(current_lines)

    return PreprocessedSod(
        intro=" ".join(intro_lines).strip(),
        points=points,
        is_initial_comments=is_initial,
    )


# ---- LLM prompt ----

_USER_TEMPLATE = """\
You are a CMS-2567 deficiency analyst reviewing tag {f_tag}.

{context_instruction}

For each numbered point below, write a precise Plan of Correction (2-4 sentences) that directly addresses that specific finding. Preserve the point order. If a point is purely factual/contextual with no corrective action needed, set its poc to "".

Points:
{points_json}

Respond with ONLY this JSON (no other text):
{{"points": [{{"label": "<label>", "poc": "<plan of correction>"}}, ...]}}"""

_INITIAL_COMMENTS_INSTRUCTION = (
    "This is an Initial Comments section. Summarize the survey context "
    "(survey type, date, number of deficiencies cited) as the narrative. "
    "No corrective action is needed — set poc to \"\" for all points."
)
_DEFICIENCY_INSTRUCTION = (
    "Produce a clean, readable deficiency narrative as sod_text. "
    "For each numbered point, write a targeted Plan of Correction."
)


@dataclass(frozen=True)
class LlmPointResult:
    label: str
    text: str
    poc: str


@dataclass(frozen=True)
class LlmCleanResult:
    sod_text: str
    poc_suggestion: str                         # top-level combined POC (backward compat)
    points: list[LlmPointResult] = field(default_factory=list)


async def clean_sod_with_llm(
    preprocessed: PreprocessedSod,
    f_tag: str,
    *,
    endpoint: str,
    api_key: str,
    model: str,
    timeout_seconds: float = 60.0,
) -> LlmCleanResult | None:
    """Call the LLM with structured per-point input and return per-point POC.

    Returns None on any failure so the caller can fall back to regex clean.
    """
    base = endpoint.rstrip("/")
    if not base.endswith("/chat/completions"):
        base = f"{base}/chat/completions"

    # Build the points JSON the LLM will annotate
    if preprocessed.points:
        points_input = [
            {"label": p.label, "text": p.text}
            for p in preprocessed.points
        ]
    else:
        # No numbered points — treat the whole text as a single unlabelled point
        points_input = [{"label": "—", "text": preprocessed.full_text}]

    context_instruction = (
        _INITIAL_COMMENTS_INSTRUCTION
        if preprocessed.is_initial_comments
        else _DEFICIENCY_INSTRUCTION
    )

    prompt = _USER_TEMPLATE.format(
        f_tag=f_tag,
        context_instruction=context_instruction,
        points_json=json.dumps(points_input, indent=2),
    )

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {"type": "json_object"},
        "temperature": 0.1,
        "max_tokens": 2048,
    }

    try:
        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            response = await client.post(
                base,
                json=payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
            )
        print(f"[LLM] POST {base} -> {response.status_code}")
        response.raise_for_status()
        body = response.json()
        content = body["choices"][0]["message"]["content"]
        parsed = json.loads(content)

        raw_points = parsed.get("points", [])

        point_results: list[LlmPointResult] = []
        for index, source_point in enumerate(points_input):
            response_point = raw_points[index] if index < len(raw_points) else {}
            poc = response_point.get("poc", "") if isinstance(response_point, dict) else ""
            point_results.append(
                LlmPointResult(
                    label=source_point["label"],
                    text=source_point["text"],
                    poc=poc.strip() if isinstance(poc, str) else "",
                )
            )

        # Combined POC: join non-empty per-point POCs for backward compat
        combined_poc = "\n\n".join(
            f"{pt.label} {pt.poc}".strip() for pt in point_results if pt.poc
        )

        sod = preprocessed.full_text
        if sod:
            print(f"[LLM] OK - sod={len(sod)} chars, points={len(point_results)}")
            return LlmCleanResult(
                sod_text=sod,
                poc_suggestion=combined_poc,
                points=point_results,
            )
        print("[LLM] Empty source SOD after preprocessing")
    except Exception as exc:
        print(f"[LLM] ERROR: {type(exc).__name__}: {exc}")

    return None

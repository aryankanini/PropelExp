"""Required labeling invariant for locally delivered exports."""

import re
from typing import Final

DRAFT_EXPORT_PREFIX: Final = (
    "DRAFT - Approved for compliance handling; not submitted to CMS."
)

_CONTROL_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


class EmptyExportContentError(ValueError):
    """Raised when approved content cannot form a meaningful export."""


def prefix_export_content(content: str) -> str:
    """Prefix non-empty approved content with the required draft label."""
    sanitized = _CONTROL_CHARS_RE.sub("", content).strip()
    if not sanitized:
        raise EmptyExportContentError("approved content must not be empty")
    return f"{DRAFT_EXPORT_PREFIX}\n\n{sanitized}"
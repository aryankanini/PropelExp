"""Provider-neutral guardrail for AI-produced export claims."""

from collections.abc import Mapping

from cms_planner.domain.approval import ApprovalState
from cms_planner.domain.export_policy import authorize_export
from cms_planner.domain.poc import PocDraft


def guard_export_output(
    provider_output: Mapping[str, object],
    *,
    draft: PocDraft | None,
    approval: ApprovalState,
) -> str:
    """Return candidate content only when backend export policy authorizes it."""
    blocker = authorize_export(draft, approval)
    if blocker is not None:
        raise PermissionError(blocker.code.value)
    candidate = provider_output.get("candidate_text")
    if not isinstance(candidate, str) or not candidate.strip():
        raise ValueError("provider output must contain candidate_text")
    return candidate.strip()
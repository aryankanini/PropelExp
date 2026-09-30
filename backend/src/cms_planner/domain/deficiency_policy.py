"""Policies governing deficiency candidate confirmation transitions."""

from cms_planner.domain.deficiency_candidate import DeficiencyCandidate


class CandidateConfirmationError(ValueError):
    """Report a candidate that cannot transition to confirmed."""


def confirm_deficiency_candidate(candidate: DeficiencyCandidate) -> DeficiencyCandidate:
    """Confirm only a complete candidate whose uncertainty has been resolved."""
    if candidate.sod_text is None:
        raise CandidateConfirmationError("confirmation requires a complete SOD")
    if candidate.uncertainty:
        raise CandidateConfirmationError("confirmation requires resolved uncertainty")
    if candidate.confirmed:
        return candidate
    return candidate.model_copy(update={"confirmed": True})
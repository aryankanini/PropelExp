"""Own the fail-closed decision for outbound provider availability."""

from pydantic import BaseModel, ConfigDict


class ProviderApproval(BaseModel):
    """Required safeguards for transmitting case content to a provider."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    baa: bool
    retention: bool
    training_use: bool
    risk: bool

    @property
    def missing(self) -> tuple[str, ...]:
        return tuple(
            name
            for name in ("baa", "retention", "training_use", "risk")
            if not getattr(self, name)
        )


class ProviderNotApprovedError(Exception):
    """Identify absent approvals without including provider configuration."""

    def __init__(self, approval_names: tuple[str, ...]) -> None:
        super().__init__("Provider approval is incomplete")
        self.approval_names = approval_names


def require_provider_approval(approval: ProviderApproval) -> ProviderApproval:
    """Return a complete approval or block the provider before invocation."""
    missing = approval.missing
    if missing:
        raise ProviderNotApprovedError(missing)
    return approval
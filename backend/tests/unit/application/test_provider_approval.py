import pytest

from cms_planner.application.provider_approval import (
    ProviderApproval,
    ProviderNotApprovedError,
    require_provider_approval,
)


@pytest.mark.parametrize(
    "missing_approval",
    ("baa", "retention", "training_use", "risk"),
)
def test_provider_approval_requires_every_safeguard(missing_approval: str) -> None:
    approvals = {
        "baa": True,
        "retention": True,
        "training_use": True,
        "risk": True,
    }
    approvals[missing_approval] = False

    with pytest.raises(ProviderNotApprovedError):
        require_provider_approval(ProviderApproval(**approvals))


def test_provider_approval_accepts_all_safeguards() -> None:
    approval = ProviderApproval(
        baa=True,
        retention=True,
        training_use=True,
        risk=True,
    )

    assert require_provider_approval(approval) is approval
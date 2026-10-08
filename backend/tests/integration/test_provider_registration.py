import logging
from pathlib import Path

import pytest

from cms_planner.app import (
    _UnavailablePocProvider,
    create_configured_poc_provider,
    register_provider_adapters,
)
from cms_planner.infrastructure.config.provider import (
    ProviderConfigurationError,
    ProviderSettings,
)


class FakeOcrProvider:
    async def recognize(self, request: object) -> object:
        raise AssertionError("provider should not be invoked during registration")


def test_unapproved_provider_is_not_registered(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            (
                "PROVIDER_ENDPOINT=https://provider.example/v1",
                "PROVIDER_API_KEY=secret-value",
                "PROVIDER_TIMEOUT_SECONDS=120",
                "PROVIDER_BAA_APPROVED=true",
                "PROVIDER_RETENTION_APPROVED=true",
                "PROVIDER_TRAINING_USE_APPROVED=true",
                "PROVIDER_RISK_APPROVED=false",
            )
        ),
        encoding="utf-8",
    )

    with pytest.raises(ProviderConfigurationError):
        register_provider_adapters(
            ProviderSettings.load(env_file),
            FakeOcrProvider(),
        )


def test_invalid_poc_provider_configuration_logs_setting_names_only(
    monkeypatch,
    caplog,
) -> None:
    error = ProviderConfigurationError(("api_key", "risk_approved"))
    monkeypatch.setattr(
        ProviderSettings,
        "load",
        classmethod(lambda cls: (_ for _ in ()).throw(error)),
    )

    with caplog.at_level(logging.WARNING):
        provider = create_configured_poc_provider()

    assert isinstance(provider, _UnavailablePocProvider)
    assert "invalid settings=api_key,risk_approved" in caplog.text
    assert "secret" not in caplog.text
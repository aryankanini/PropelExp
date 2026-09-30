from pathlib import Path

import pytest

from cms_planner.app import register_provider_adapters
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
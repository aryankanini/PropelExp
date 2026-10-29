from pathlib import Path

import pytest

from cms_planner.infrastructure.config.provider import (
    ProviderConfigurationError,
    ProviderSettings,
)


def write_environment(path: Path, **overrides: str) -> None:
    values = {
        "PROVIDER_ENDPOINT": "https://provider.example/v1",
        "PROVIDER_API_KEY": "provider-secret-value",
        "PROVIDER_TIMEOUT_SECONDS": "120",
        "PROVIDER_BAA_APPROVED": "true",
        "PROVIDER_RETENTION_APPROVED": "true",
        "PROVIDER_TRAINING_USE_APPROVED": "true",
        "PROVIDER_RISK_APPROVED": "true",
    }
    values.update(overrides)
    path.write_text(
        "\n".join(f"{name}={value}" for name, value in values.items()),
        encoding="utf-8",
    )


def test_provider_settings_load_approved_tls_configuration(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    write_environment(env_file)

    settings = ProviderSettings.load(env_file)

    assert str(settings.endpoint) == "https://provider.example/v1"
    assert settings.timeout_seconds == 120
    assert settings.approval.baa is True


def test_provider_settings_serialization_excludes_api_key(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    write_environment(env_file)

    settings = ProviderSettings.load(env_file)
    serialized = f"{settings.model_dump()}{ProviderSettings.model_json_schema()}"

    assert "provider-secret-value" not in serialized
    assert "api_key" not in serialized


def test_azure_openai_variables_are_supported_without_provider_duplicates(
    tmp_path: Path,
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            (
                "AZURE_OPENAI_ENDPOINT=https://resource.openai.azure.com",
                "AZURE_OPENAI_API_KEY=azure-secret-value",
                "AZURE_OPENAI_API_VERSION=2025-01-01-preview",
                "AZURE_OPENAI_DEPLOYMENT=poc-deployment",
                "PROVIDER_TIMEOUT_SECONDS=120",
                "PROVIDER_BAA_APPROVED=true",
                "PROVIDER_RETENTION_APPROVED=true",
                "PROVIDER_TRAINING_USE_APPROVED=true",
                "PROVIDER_RISK_APPROVED=true",
            )
        ),
        encoding="utf-8",
    )

    settings = ProviderSettings.load(env_file)

    assert str(settings.endpoint) == (
        "https://resource.openai.azure.com/openai/deployments/poc-deployment"
    )
    assert settings.model == "poc-deployment"
    assert settings.api_version == "2025-01-01-preview"
    assert settings.api_key.get_secret_value() == "azure-secret-value"


@pytest.mark.parametrize(
    ("name", "value"),
    (
        ("PROVIDER_ENDPOINT", "http://provider.example/v1"),
        ("PROVIDER_API_KEY", "changeme"),
        ("PROVIDER_TIMEOUT_SECONDS", "121"),
        ("PROVIDER_BAA_APPROVED", "false"),
        ("PROVIDER_RETENTION_APPROVED", "false"),
        ("PROVIDER_TRAINING_USE_APPROVED", "false"),
        ("PROVIDER_RISK_APPROVED", "false"),
    ),
)
def test_provider_settings_fail_closed(tmp_path: Path, name: str, value: str) -> None:
    env_file = tmp_path / ".env"
    write_environment(env_file, **{name: value})

    with pytest.raises(ProviderConfigurationError) as error:
        ProviderSettings.load(env_file)

    assert "provider-secret-value" not in str(error.value)


def test_provider_settings_report_missing_name_without_secret(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    write_environment(env_file)
    env_file.write_text(
        "\n".join(
            line
            for line in env_file.read_text(encoding="utf-8").splitlines()
            if not line.startswith("PROVIDER_RISK_APPROVED=")
        ),
        encoding="utf-8",
    )

    with pytest.raises(ProviderConfigurationError) as error:
        ProviderSettings.load(env_file)

    assert error.value.setting_names == ("risk_approved",)
    assert "provider-secret-value" not in str(error.value)


def test_reload_revokes_provider_after_approval_change(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    write_environment(env_file)
    ProviderSettings.load(env_file)
    write_environment(env_file, PROVIDER_BAA_APPROVED="false")

    with pytest.raises(ProviderConfigurationError) as error:
        ProviderSettings.load(env_file)

    assert error.value.setting_names == ("baa",)
    assert "provider-secret-value" not in str(error.value)
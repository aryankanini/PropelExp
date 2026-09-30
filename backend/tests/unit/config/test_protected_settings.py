from pathlib import Path

import pytest

from config.protected_settings import ProtectedSettings, ProtectedSettingsError


def write_environment(path: Path, approval: str = "true") -> None:
    path.write_text(
        "\n".join(
            (
                "CREDENTIAL_HASH=argon2-test-value",
                "SESSION_SECRET=session-test-value",
                "PROVIDER_KEY=provider-test-value",
                f"PROVIDER_APPROVED={approval}",
            )
        ),
        encoding="utf-8",
    )


def test_protected_values_load_but_never_serialize_or_enter_schema(
    tmp_path: Path,
) -> None:
    env_file = tmp_path / ".env"
    write_environment(env_file)

    settings = ProtectedSettings.load(env_file)

    assert settings.provider_approved is True
    assert settings.provider_key.get_secret_value() == "provider-test-value"
    assert settings.model_dump() == {}
    assert ProtectedSettings.model_json_schema()["properties"] == {}
    assert "test-value" not in repr(settings)


def test_invalid_protected_value_reports_only_setting_name(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    write_environment(env_file, approval="not-a-boolean-secret")

    with pytest.raises(ProtectedSettingsError) as error:
        ProtectedSettings.load(env_file)

    assert error.value.setting_names == ("provider_approved",)
    assert "not-a-boolean-secret" not in str(error.value)
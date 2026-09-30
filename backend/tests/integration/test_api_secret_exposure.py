from pathlib import Path

from config.protected_settings import ProtectedSettings


def test_protected_configuration_has_no_response_shaped_fields(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            (
                "CREDENTIAL_HASH=credential-value-not-for-api",
                "SESSION_SECRET=session-value-not-for-api",
                "PROVIDER_KEY=provider-value-not-for-api",
                "PROVIDER_APPROVED=true",
            )
        ),
        encoding="utf-8",
    )
    settings = ProtectedSettings.load(env_file)

    response_payload = settings.model_dump(mode="json")
    response_schema = ProtectedSettings.model_json_schema()

    assert response_payload == {}
    assert response_schema["properties"] == {}
    serialized = f"{response_payload}{response_schema}".lower()
    assert "credential" not in serialized
    assert "session_secret" not in serialized
    assert "provider_key" not in serialized
    assert "approved" not in serialized
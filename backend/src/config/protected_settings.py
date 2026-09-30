"""Environment-backed protected configuration with no public serialization."""

from pathlib import Path

from pydantic import BaseModel, PrivateAttr, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProtectedSettingsError(Exception):
    """Report invalid setting names without exposing protected values."""

    def __init__(self, setting_names: tuple[str, ...]) -> None:
        names = ", ".join(setting_names)
        super().__init__(f"Protected settings are invalid: {names}")
        self.setting_names = setting_names


class _ProtectedEnvironment(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        extra="ignore",
        case_sensitive=False,
    )

    credential_hash: SecretStr
    session_secret: SecretStr
    provider_key: SecretStr
    provider_approved: bool


class ProtectedSettings(BaseModel):
    """Keep secrets and approval state outside model dumps and API schemas."""

    _credential_hash: SecretStr = PrivateAttr()
    _session_secret: SecretStr = PrivateAttr()
    _provider_key: SecretStr = PrivateAttr()
    _provider_approved: bool = PrivateAttr()

    @classmethod
    def load(cls, env_file: Path | None = None) -> "ProtectedSettings":
        options = {} if env_file is None else {"_env_file": env_file}
        try:
            environment = _ProtectedEnvironment(**options)
        except ValidationError as error:
            names = tuple(
                str(item["loc"][0]) for item in error.errors(include_input=False)
            )
            raise ProtectedSettingsError(names) from None

        settings = cls()
        settings._credential_hash = environment.credential_hash
        settings._session_secret = environment.session_secret
        settings._provider_key = environment.provider_key
        settings._provider_approved = environment.provider_approved
        return settings

    @property
    def credential_hash(self) -> SecretStr:
        return self._credential_hash

    @property
    def session_secret(self) -> SecretStr:
        return self._session_secret

    @property
    def provider_key(self) -> SecretStr:
        return self._provider_key

    @property
    def provider_approved(self) -> bool:
        return self._provider_approved
"""Load approved provider configuration without exposing credentials."""

from pathlib import Path
from typing import Self

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, PrivateAttr, SecretStr
from pydantic import ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from cms_planner.application.provider_approval import (
    ProviderApproval,
    ProviderNotApprovedError,
    require_provider_approval,
)

MAX_PROVIDER_TIMEOUT_SECONDS = 120
DISALLOWED_API_KEYS = frozenset({"changeme", "default", "placeholder"})


class ProviderConfigurationError(Exception):
    """Report invalid setting names while excluding their values."""

    def __init__(self, setting_names: tuple[str, ...]) -> None:
        names = ", ".join(setting_names)
        super().__init__(f"Provider settings are invalid: {names}")
        self.setting_names = setting_names


class _ProviderEnvironment(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="provider_",
        extra="ignore",
        case_sensitive=False,
    )

    endpoint: AnyHttpUrl
    api_key: SecretStr = Field(min_length=1)
    model: str = Field(default="gpt-4o-mini", min_length=1)
    timeout_seconds: int = Field(gt=0, le=MAX_PROVIDER_TIMEOUT_SECONDS)
    baa_approved: bool
    retention_approved: bool
    training_use_approved: bool
    risk_approved: bool

    @field_validator("endpoint")
    @classmethod
    def require_tls(cls, endpoint: AnyHttpUrl) -> AnyHttpUrl:
        if endpoint.scheme != "https":
            raise ValueError("provider endpoint must use TLS")
        return endpoint

    @field_validator("api_key")
    @classmethod
    def reject_default_key(cls, api_key: SecretStr) -> SecretStr:
        if api_key.get_secret_value().strip().lower() in DISALLOWED_API_KEYS:
            raise ValueError("provider API key must not be a default value")
        return api_key


class ProviderSettings(BaseModel):
    """Validated non-secret provider settings and private credential access."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    endpoint: AnyHttpUrl
    model: str
    timeout_seconds: int
    approval: ProviderApproval
    _api_key: SecretStr = PrivateAttr()

    @classmethod
    def load(cls, env_file: Path | None = None) -> Self:
        options = {} if env_file is None else {"_env_file": env_file}
        try:
            environment = _ProviderEnvironment(**options)
            approval = ProviderApproval(
                baa=environment.baa_approved,
                retention=environment.retention_approved,
                training_use=environment.training_use_approved,
                risk=environment.risk_approved,
            )
            require_provider_approval(approval)
        except ValidationError as error:
            names = tuple(
                str(item["loc"][0])
                for item in error.errors(include_input=False)
            )
            raise ProviderConfigurationError(names) from None
        except ProviderNotApprovedError as error:
            raise ProviderConfigurationError(error.approval_names) from None

        settings = cls(
            endpoint=environment.endpoint,
            model=environment.model,
            timeout_seconds=environment.timeout_seconds,
            approval=approval,
        )
        settings._api_key = environment.api_key
        return settings

    @property
    def api_key(self) -> SecretStr:
        return self._api_key
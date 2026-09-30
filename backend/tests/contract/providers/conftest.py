from pathlib import Path
from typing import Any

import pytest

from cms_planner.infrastructure.config.provider import ProviderSettings


@pytest.fixture
def provider_settings(tmp_path: Path) -> ProviderSettings:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            (
                "PROVIDER_ENDPOINT=https://provider.example/v1",
                "PROVIDER_API_KEY=contract-secret",
                "PROVIDER_TIMEOUT_SECONDS=120",
                "PROVIDER_BAA_APPROVED=true",
                "PROVIDER_RETENTION_APPROVED=true",
                "PROVIDER_TRAINING_USE_APPROVED=true",
                "PROVIDER_RISK_APPROVED=true",
            )
        ),
        encoding="utf-8",
    )
    return ProviderSettings.load(env_file)


@pytest.fixture
def valid_extraction_response() -> dict[str, Any]:
    return {
        "provider_name": "North Clinic",
        "f_tag": "F880",
        "sod": "Complete statement of deficiency",
        "uncertain_fields": [],
    }


@pytest.fixture
def valid_poc_response() -> dict[str, Any]:
    return {
        "content": {
            "affected_residents": "Resident review completed",
            "others_at_risk": "At-risk residents assessed",
            "corrective_measures": "Policy corrected",
            "monitoring": "Weekly audit",
            "completion_date": "2026-10-01",
        },
        "claims": [],
        "missing_information": [],
    }
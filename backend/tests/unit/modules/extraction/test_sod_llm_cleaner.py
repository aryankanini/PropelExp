import json

import httpx
import pytest

from cms_planner.modules.extraction.sod_llm_cleaner import (
    clean_sod_with_llm,
    preprocess_sod_text,
)


def test_only_all_zero_tag_is_treated_as_initial_comments() -> None:
    initial_comments = preprocess_sod_text("Survey completed.", "L0000")
    deficiency = preprocess_sod_text("The facility failed.", "F1000")

    assert initial_comments.is_initial_comments is True
    assert deficiency.is_initial_comments is False


@pytest.mark.asyncio
async def test_cleaner_sends_preprocessed_points_and_parses_structured_response(
    monkeypatch,
) -> None:
    captured: dict[str, object] = {}

    class StubAsyncClient:
        def __init__(self, timeout: float) -> None:
            captured["timeout"] = timeout

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, traceback) -> None:
            return None

        async def post(self, url: str, *, json: dict, headers: dict) -> httpx.Response:
            captured["url"] = url
            captured["payload"] = json
            return httpx.Response(
                200,
                request=httpx.Request("POST", url),
                json={
                    "choices": [
                        {
                            "message": {
                                "content": json_module.dumps(
                                    {
                                        "sod_text": "1. Cleaned finding.",
                                        "points": [
                                            {
                                                "label": "1.",
                                                "text": "Cleaned finding.",
                                                "poc": "Audit records each shift.",
                                            }
                                        ],
                                    }
                                )
                            }
                        }
                    ]
                },
            )

    json_module = json
    monkeypatch.setattr(httpx, "AsyncClient", StubAsyncClient)

    result = await clean_sod_with_llm(
        preprocess_sod_text(
            "FORM APPROVED\n1. Repositioning was not documented.",
            "F0686",
        ),
        "F0686",
        endpoint="https://provider.example/v1",
        api_key="secret",
        model="test-model",
    )

    assert result is not None
    assert result.sod_text == "1. Repositioning was not documented."
    assert result.points[0].text == "Repositioning was not documented."
    assert result.points[0].poc == "Audit records each shift."
    prompt = captured["payload"]["messages"][0]["content"]
    assert "FORM APPROVED" not in prompt
    assert '"label": "1."' in prompt
    assert '"text": "Repositioning was not documented."' in prompt


def test_preprocessor_preserves_long_point_text() -> None:
    detailed_finding = "Detailed evidence " * 200

    preprocessed = preprocess_sod_text(f"1. {detailed_finding}", "F0686")

    assert preprocessed.points[0].text == detailed_finding.strip()

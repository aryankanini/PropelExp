"""OpenAI-compatible POC generation provider using the AI HTTP adapter."""

import json
from pathlib import Path

from cms_planner.application.failures import ProviderFailure
from cms_planner.application.providers.executor import ProviderExecutor
from cms_planner.application.providers.results import (
    ExhaustedProviderRetries,
    InvalidProviderResponse,
)
from cms_planner.domain.poc_generation import PocGenerationInput, ProviderPocResponse
from cms_planner.domain.poc import POC_SECTION_ORDER
from cms_planner.infrastructure.config.provider import ProviderSettings

_PROMPTS_DIR = Path(__file__).parents[5] / "prompts" / "poc"


def _load_system_prompt() -> str:
    parts = [
        (_PROMPTS_DIR / "five_part_draft.md").read_text(encoding="utf-8"),
        (_PROMPTS_DIR / "grounded_claims.md").read_text(encoding="utf-8"),
        (_PROMPTS_DIR / "missing_information.md").read_text(encoding="utf-8"),
    ]
    return "\n\n".join(parts)


_SYSTEM_PROMPT = _load_system_prompt()

_POC_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        section.value: {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
        }
        for section in POC_SECTION_ORDER
    },
    "required": [section.value for section in POC_SECTION_ORDER],
    "additionalProperties": False,
}


class OpenAiPocProvider:
    """Generate a five-part POC draft via an OpenAI-compatible chat endpoint."""

    def __init__(
        self,
        settings: ProviderSettings,
        transport: object,
        executor: ProviderExecutor,
    ) -> None:
        self._settings = settings
        self._transport = transport
        self._executor = executor

    def generate(self, request: PocGenerationInput) -> ProviderPocResponse:
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                future = pool.submit(asyncio.run, self._generate_async(request))
                return future.result()
        return loop.run_until_complete(self._generate_async(request))

    async def _generate_async(self, request: PocGenerationInput) -> ProviderPocResponse:
        user_content = json.dumps(
            {
                "deficiency_id": request.deficiency_id,
                "deficiency_revision_id": request.deficiency_revision_id,
                "reviewed_fields": [f.model_dump() for f in request.reviewed_fields],
                "evidence_spans": [e.model_dump() for e in request.evidence_spans],
            }
        )
        payload = {
            "model": self._settings.model,
            "messages": [
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "cms_plan_of_correction",
                    "strict": True,
                    "schema": _POC_RESPONSE_SCHEMA,
                },
            },
        }

        async def invoke():
            endpoint = str(self._settings.endpoint).rstrip("/")
            if not endpoint.endswith("/chat/completions"):
                endpoint = f"{endpoint}/chat/completions"
            return await self._transport.post_json(
                endpoint=endpoint,
                api_key=self._settings.api_key.get_secret_value(),
                payload=payload,
            )

        result = await self._executor.execute(invoke)
        if isinstance(result, ExhaustedProviderRetries):
            raise ProviderFailure(provider_payload=result)

        try:
            raw = result["choices"][0]["message"]["content"]
            parsed = json.loads(raw)
            return ProviderPocResponse.model_validate_json(
                json.dumps(_normalize_provider_response(parsed))
            )
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ProviderFailure(provider_payload=InvalidProviderResponse()) from exc


def _normalize_provider_response(payload: object) -> object:
    if not isinstance(payload, dict) or "sections" in payload:
        return payload

    section_names = tuple(section.value for section in POC_SECTION_ORDER)
    if set(payload) != set(section_names):
        return payload

    sections = []
    for name in section_names:
        statements = payload[name]
        if not isinstance(statements, list):
            return payload
        normalized_statements = []
        for statement in statements:
            if isinstance(statement, str) and statement.strip():
                normalized_statements.append(
                    {"kind": "generic_guidance", "text": statement.strip()}
                )
                continue
            if not isinstance(statement, dict):
                return payload
            normalized = dict(statement)
            if "kind" not in normalized and "type" in normalized:
                normalized["kind"] = normalized.pop("type")
            normalized_statements.append(normalized)
        sections.append({"name": name, "statements": normalized_statements})
    return {"sections": sections}

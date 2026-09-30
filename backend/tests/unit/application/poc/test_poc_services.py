from concurrent.futures import ThreadPoolExecutor

import pytest

from cms_planner.adapters.ai.guardrails import DeterministicPocGuardrails
from cms_planner.adapters.repositories.in_memory_poc_repository import InMemoryPocRepository
from cms_planner.application.failures import (
    GenerationDeniedFailure,
    RetentionFailure,
    StaleStateFailure,
    ValidationFailure,
)
from cms_planner.application.poc_generation_service import PocGenerationService
from cms_planner.application.poc_revision_service import PocRevisionService
from cms_planner.application.ports.poc_repository import PocRetentionError
from cms_planner.domain.deficiency import (
    Deficiency,
    DeficiencyRevision,
    EvidenceSpan,
    ReviewedField,
)
from cms_planner.domain.poc import PocSectionName, SectionOrigin
from cms_planner.domain.poc_generation import PocGenerationInput


def provider_payload() -> dict[str, object]:
    return {
        "sections": [
            {
                "name": section.value,
                "statements": [
                    {"kind": "generic_guidance", "text": f"Guidance for {section.value}."}
                ],
            }
            for section in PocSectionName
        ]
    }


class RecordingProvider:
    def __init__(self, payload: object | None = None) -> None:
        self.payload = payload or provider_payload()
        self.requests: list[PocGenerationInput] = []

    def generate(self, request: PocGenerationInput) -> object:
        self.requests.append(request)
        return self.payload


class FailingUpdateRepository(InMemoryPocRepository):
    def update_draft(self, deficiency_id, updater):
        current = self.get_draft(deficiency_id)
        assert current is not None
        updater(current)
        raise PocRetentionError()


def deficiency(*, confirmed: bool) -> Deficiency:
    revision = DeficiencyRevision(
        revision_id="def-rev-1",
        reviewed_fields=(ReviewedField(field_id="field-1", name="SOD", value="value"),),
        evidence_spans=(
            EvidenceSpan(evidence_id="evidence-1", page_number=1, text="source"),
        ),
        confirmed=confirmed,
    )
    return Deficiency(
        deficiency_id="deficiency-1",
        revisions=(revision,),
        current_revision_id=revision.revision_id,
    )


def test_generation_denies_unconfirmed_revision_before_provider_call() -> None:
    repository = InMemoryPocRepository()
    repository.add_deficiency(deficiency(confirmed=False))
    provider = RecordingProvider()

    with pytest.raises(GenerationDeniedFailure):
        PocGenerationService(
            repository, provider, DeterministicPocGuardrails()
        ).generate("deficiency-1")

    assert provider.requests == []
    assert repository.get_draft("deficiency-1") is None


def test_generation_is_scoped_and_idempotent_under_concurrency() -> None:
    repository = InMemoryPocRepository()
    repository.add_deficiency(deficiency(confirmed=True))
    provider = RecordingProvider()
    service = PocGenerationService(
        repository,
        provider,
        DeterministicPocGuardrails(),
        lambda: "poc-rev-1",
    )

    with ThreadPoolExecutor(max_workers=8) as executor:
        drafts = tuple(executor.map(lambda _: service.generate("deficiency-1"), range(16)))

    assert {draft.current_revision_id for draft in drafts} == {"poc-rev-1"}
    assert len(provider.requests) == 1
    assert provider.requests[0].deficiency_id == "deficiency-1"
    assert tuple(field.field_id for field in provider.requests[0].reviewed_fields) == (
        "field-1",
    )
    assert drafts[0].current_revision.status == "unapproved"


def test_invalid_generation_is_not_retained() -> None:
    repository = InMemoryPocRepository()
    repository.add_deficiency(deficiency(confirmed=True))
    provider = RecordingProvider({"sections": []})

    with pytest.raises(ValidationFailure):
        PocGenerationService(
            repository, provider, DeterministicPocGuardrails()
        ).generate("deficiency-1")

    assert repository.get_draft("deficiency-1") is None


def test_edit_and_stale_failure_preserve_current_revision() -> None:
    repository = InMemoryPocRepository()
    repository.add_deficiency(deficiency(confirmed=True))
    draft = PocGenerationService(
        repository,
        RecordingProvider(),
        DeterministicPocGuardrails(),
        lambda: "poc-rev-1",
    ).generate("deficiency-1")
    service = PocRevisionService(repository, lambda: "poc-rev-2")

    edited = service.save(
        deficiency_id="deficiency-1",
        expected_revision_id=draft.current_revision_id,
        section_updates={PocSectionName.MONITORING: "Audit daily."},
    )

    assert edited.current_revision.status == "unapproved"
    assert edited.current_revision.section_origins[PocSectionName.MONITORING] == (
        SectionOrigin.USER_EDITED
    )
    with pytest.raises(StaleStateFailure):
        service.save(
            deficiency_id="deficiency-1",
            expected_revision_id="poc-rev-1",
            section_updates={PocSectionName.MONITORING: "Overwrite."},
        )
    assert repository.get_draft("deficiency-1").current_revision_id == "poc-rev-2"


def test_retention_failure_preserves_current_revision() -> None:
    repository = FailingUpdateRepository()
    repository.add_deficiency(deficiency(confirmed=True))
    draft = PocGenerationService(
        repository,
        RecordingProvider(),
        DeterministicPocGuardrails(),
        lambda: "poc-rev-1",
    ).generate("deficiency-1")

    with pytest.raises(RetentionFailure):
        PocRevisionService(repository, lambda: "poc-rev-2").save(
            deficiency_id="deficiency-1",
            expected_revision_id=draft.current_revision_id,
            section_updates={PocSectionName.MONITORING: "Audit daily."},
        )

    assert repository.get_draft("deficiency-1").current_revision_id == "poc-rev-1"
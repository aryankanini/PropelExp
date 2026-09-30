import hashlib
import json
from pathlib import Path

from evaluation.run import evaluate_release, write_report
from evaluation.scoring import EvaluationOutcome


def successful_outcome() -> EvaluationOutcome:
    return EvaluationOutcome(
        duration_seconds=299,
        documented_outage=False,
        provider_name_correct=True,
        f_tag_correct=True,
        complete_sod_correct=True,
    )


def test_evaluation_report_is_reproducible(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    manifest.write_text('{"pages": 100}', encoding="utf-8")
    digest = hashlib.sha256(manifest.read_bytes()).hexdigest()
    acceptance = tmp_path / "acceptance.yaml"
    acceptance.write_text(
        json.dumps(
            {
                "dataset": {"id": "approved-v1", "sha256": digest},
                "thresholds": {
                    "maximum_duration_seconds": 300,
                    "minimum_timing_rate": 0.95,
                    "minimum_field_accuracy": 0.95,
                },
            }
        ),
        encoding="utf-8",
    )
    outcomes = (successful_outcome(),)

    first = evaluate_release(
        manifest_path=manifest,
        acceptance_path=acceptance,
        outcomes=outcomes,
    )
    second = evaluate_release(
        manifest_path=manifest,
        acceptance_path=acceptance,
        outcomes=outcomes,
    )
    first_path = tmp_path / "first.json"
    second_path = tmp_path / "second.json"
    write_report(first_path, first)
    write_report(second_path, second)

    assert first_path.read_bytes() == second_path.read_bytes()
    assert first["passed"] is True


def test_repository_acceptance_matches_approved_manifest() -> None:
    backend_root = Path(__file__).parents[2]

    report = evaluate_release(
        manifest_path=backend_root / "evaluation/data/approved_manifest.json",
        acceptance_path=backend_root / "evaluation/config/acceptance.yaml",
        outcomes=(successful_outcome(),),
    )

    assert report["dataset_id"] == "cms2567-approved-100-page-v1"
    assert report["passed"] is True
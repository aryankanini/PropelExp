"""Produce reproducible machine-readable AI release evidence."""

import hashlib
import json
from pathlib import Path
from typing import Any

from evaluation.scoring import AcceptanceThresholds, EvaluationOutcome, score_outcomes


def load_acceptance(path: Path) -> tuple[str, str, AcceptanceThresholds]:
    """Load the JSON-compatible YAML acceptance policy."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    dataset = payload["dataset"]
    thresholds = payload["thresholds"]
    return (
        dataset["id"],
        dataset["sha256"],
        AcceptanceThresholds(
            maximum_duration_seconds=thresholds["maximum_duration_seconds"],
            minimum_timing_rate=thresholds["minimum_timing_rate"],
            minimum_field_accuracy=thresholds["minimum_field_accuracy"],
        ),
    )


def evaluate_release(
    *,
    manifest_path: Path,
    acceptance_path: Path,
    outcomes: tuple[EvaluationOutcome, ...],
) -> dict[str, Any]:
    """Verify dataset identity and return deterministic release evidence."""
    dataset_id, expected_hash, thresholds = load_acceptance(acceptance_path)
    actual_hash = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    if actual_hash != expected_hash:
        raise ValueError("evaluation manifest does not match the approved identity")
    metrics = score_outcomes(outcomes, thresholds)
    return {
        "dataset_id": dataset_id,
        "dataset_sha256": actual_hash,
        "outcome_count": len(outcomes),
        "metrics": {
            "timing_rate": metrics.timing_rate,
            "provider_name_accuracy": metrics.provider_name_accuracy,
            "f_tag_accuracy": metrics.f_tag_accuracy,
            "complete_sod_accuracy": metrics.complete_sod_accuracy,
            "all_misses_uncertain": metrics.all_misses_uncertain,
            "unsupported_claims": metrics.unsupported_claims,
        },
        "passed": metrics.passed,
    }


def write_report(path: Path, report: dict[str, Any]) -> None:
    """Write stable JSON bytes for reproducible release evidence."""
    path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
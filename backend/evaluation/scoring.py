"""Calculate deterministic AIR-006 release acceptance metrics."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvaluationOutcome:
    duration_seconds: float
    documented_outage: bool
    provider_name_correct: bool
    f_tag_correct: bool
    complete_sod_correct: bool
    missed_fields: frozenset[str] = frozenset()
    uncertain_fields: frozenset[str] = frozenset()
    unsupported_claims: int = 0


@dataclass(frozen=True, slots=True)
class AcceptanceThresholds:
    maximum_duration_seconds: float
    minimum_timing_rate: float
    minimum_field_accuracy: float


@dataclass(frozen=True, slots=True)
class EvaluationMetrics:
    timing_rate: float
    provider_name_accuracy: float
    f_tag_accuracy: float
    complete_sod_accuracy: float
    all_misses_uncertain: bool
    unsupported_claims: int
    passed: bool


def score_outcomes(
    outcomes: tuple[EvaluationOutcome, ...],
    thresholds: AcceptanceThresholds,
) -> EvaluationMetrics:
    """Score timing and quality while limiting outage exclusion to timing."""
    if not outcomes:
        raise ValueError("at least one evaluation outcome is required")
    timing_outcomes = tuple(item for item in outcomes if not item.documented_outage)
    timing_rate = _rate(
        sum(
            item.duration_seconds <= thresholds.maximum_duration_seconds
            for item in timing_outcomes
        ),
        len(timing_outcomes),
    )
    total = len(outcomes)
    provider_accuracy = _rate(sum(item.provider_name_correct for item in outcomes), total)
    f_tag_accuracy = _rate(sum(item.f_tag_correct for item in outcomes), total)
    sod_accuracy = _rate(sum(item.complete_sod_correct for item in outcomes), total)
    all_misses_uncertain = all(
        item.missed_fields <= item.uncertain_fields for item in outcomes
    )
    unsupported_claims = sum(item.unsupported_claims for item in outcomes)
    passed = all(
        (
            timing_rate >= thresholds.minimum_timing_rate,
            provider_accuracy >= thresholds.minimum_field_accuracy,
            f_tag_accuracy >= thresholds.minimum_field_accuracy,
            sod_accuracy >= thresholds.minimum_field_accuracy,
            all_misses_uncertain,
            unsupported_claims == 0,
        )
    )
    return EvaluationMetrics(
        timing_rate=timing_rate,
        provider_name_accuracy=provider_accuracy,
        f_tag_accuracy=f_tag_accuracy,
        complete_sod_accuracy=sod_accuracy,
        all_misses_uncertain=all_misses_uncertain,
        unsupported_claims=unsupported_claims,
        passed=passed,
    )


def _rate(successes: int, total: int) -> float:
    return successes / total if total else 0.0
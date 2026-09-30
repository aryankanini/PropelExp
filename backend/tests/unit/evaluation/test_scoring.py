from evaluation.scoring import AcceptanceThresholds, EvaluationOutcome, score_outcomes


THRESHOLDS = AcceptanceThresholds(
    maximum_duration_seconds=300,
    minimum_timing_rate=0.95,
    minimum_field_accuracy=0.95,
)


def outcome(**changes: object) -> EvaluationOutcome:
    values: dict[str, object] = {
        "duration_seconds": 300,
        "documented_outage": False,
        "provider_name_correct": True,
        "f_tag_correct": True,
        "complete_sod_correct": True,
    }
    values.update(changes)
    return EvaluationOutcome(**values)


def test_threshold_boundaries_pass() -> None:
    outcomes = tuple(outcome() for _ in range(19)) + (
        outcome(duration_seconds=301),
    )

    metrics = score_outcomes(outcomes, THRESHOLDS)

    assert metrics.timing_rate == 0.95
    assert metrics.passed is True


def test_documented_outage_is_excluded_from_timing_only() -> None:
    outcomes = (
        outcome(),
        outcome(
            duration_seconds=900,
            documented_outage=True,
            provider_name_correct=False,
            missed_fields=frozenset({"provider_name"}),
            uncertain_fields=frozenset(),
        ),
    )

    metrics = score_outcomes(outcomes, THRESHOLDS)

    assert metrics.timing_rate == 1.0
    assert metrics.provider_name_accuracy == 0.5
    assert metrics.all_misses_uncertain is False
    assert metrics.passed is False


def test_unsupported_claim_fails_release() -> None:
    metrics = score_outcomes(
        (outcome(unsupported_claims=1),),
        THRESHOLDS,
    )

    assert metrics.unsupported_claims == 1
    assert metrics.passed is False
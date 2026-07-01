from soundcheck.metrics import LevelMetrics
from soundcheck.report_scores import calculate_report_scores
from soundcheck.speech_analyzer import SpeechClarityAnalysis, SpeechIssue
from soundcheck.speech_bands import BandMetrics


def test_report_scores_give_full_score_for_clean_speech_sample():
    scores = calculate_report_scores(
        metrics=_metrics(),
        bands=_bands(),
        speech_analysis=SpeechClarityAnalysis(band_scores={}, top_issues=[]),
    )

    assert scores.to_dict() == {
        "overall": 100,
        "level": 20,
        "clipping": 20,
        "speech_clarity": 20,
        "low_end_balance": 15,
        "harshness": 10,
        "noise": 10,
        "stereo": 5,
        "status": "GOOD",
    }


def test_report_scores_mark_clipping_as_danger():
    scores = calculate_report_scores(
        metrics=_metrics(peak_dbfs=-0.1, clipping_count=4, clipping_ratio=0.001),
        bands=_bands(),
    )

    assert scores.clipping == 0
    assert scores.status == "DANGER"


def test_report_scores_reduce_speech_and_harshness_scores_from_week_3_issues():
    scores = calculate_report_scores(
        metrics=_metrics(),
        bands=_bands(upper_mid=0.42),
        speech_analysis=SpeechClarityAnalysis(
            band_scores={},
            top_issues=[
                SpeechIssue(
                    code="weak_clarity",
                    priority_score=0.12,
                    band="clarity_2_5khz",
                    message="The voice may lack clarity.",
                    detail="Speech clarity energy is low.",
                ),
                SpeechIssue(
                    code="harsh_upper_mid",
                    priority_score=0.10,
                    band="harsh_6_8khz",
                    message="The voice may sound harsh.",
                    detail="Upper speech energy is elevated.",
                ),
            ],
        ),
    )

    assert scores.speech_clarity == 8
    assert scores.harshness == 4
    assert scores.status == "WARNING"


def _metrics(**overrides):
    values = {
        "duration_seconds": 1.0,
        "sample_rate": 16000,
        "channels": 1,
        "peak_dbfs": -6.0,
        "rms_dbfs": -18.0,
        "crest_factor_db": 12.0,
        "clipping_count": 0,
        "clipping_ratio": 0.0,
        "left_right_balance_db": 0.0,
        "noise_floor_dbfs": -60.0,
    }
    values.update(overrides)
    return LevelMetrics(**values)


def _bands(**overrides):
    relative_energy = {
        "low": 0.05,
        "low_mid": 0.15,
        "speech_mid": 0.55,
        "upper_mid": 0.20,
        "high": 0.05,
    }
    relative_energy.update(overrides)
    return BandMetrics(relative_energy=relative_energy, dominant_band="speech_mid")

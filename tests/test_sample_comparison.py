from soundcheck.judgments import Judgment
from soundcheck.metrics import LevelMetrics
from soundcheck.reports import AnalysisReport
from soundcheck.sample_comparison import (
    build_sample_comparison,
    sample_comparison_to_markdown,
)
from soundcheck.speech_analyzer import SpeechClarityAnalysis, SpeechIssue
from soundcheck.speech_bands import BandMetrics


def test_build_sample_comparison_returns_stable_week_3_rows():
    report = _report(
        path="samples/private/bad-01.wav",
        speech_analysis=SpeechClarityAnalysis(
            band_scores={
                "low_end_80_200hz": 0.10,
                "muddy_200_400hz": 0.42,
                "boxy_300_600hz": 0.18,
                "clarity_2_5khz": 0.12,
                "harsh_6_8khz": 0.18,
            },
            top_issues=[
                SpeechIssue(
                    code="muddy_low_mids",
                    priority_score=0.16,
                    band="muddy_200_400hz",
                    message="The voice may sound muddy or muffled.",
                    detail="Energy from 200-400Hz is elevated.",
                )
            ],
        ),
    )

    rows = build_sample_comparison([report], labels={"samples/private/bad-01.wav": "bad:P5"})

    assert len(rows) == 1
    assert rows[0].to_dict() == {
        "sample_id": "bad-01",
        "path": "samples/private/bad-01.wav",
        "expected_label": "bad:P5",
        "overall_status": "WARNING",
        "top_issue_codes": ["muddy_low_mids"],
        "dominant_speech_issue": "muddy_low_mids",
        "band_scores": {
            "low_end_80_200hz": 0.10,
            "muddy_200_400hz": 0.42,
            "boxy_300_600hz": 0.18,
            "clarity_2_5khz": 0.12,
            "harsh_6_8khz": 0.18,
        },
    }


def test_build_sample_comparison_handles_reports_without_speech_analysis():
    report = _report(path="good-01.wav", speech_analysis=None)

    rows = build_sample_comparison([report])

    assert rows[0].sample_id == "good-01"
    assert rows[0].expected_label == ""
    assert rows[0].top_issue_codes == []
    assert rows[0].dominant_speech_issue == ""
    assert rows[0].band_scores == {}


def test_sample_comparison_to_markdown_returns_readable_table():
    report = _report(
        path="samples/private/bad-02.wav",
        speech_analysis=SpeechClarityAnalysis(
            band_scores={"muddy_200_400hz": 0.36},
            top_issues=[
                SpeechIssue(
                    code="muddy_low_mids",
                    priority_score=0.10,
                    band="muddy_200_400hz",
                    message="The voice may sound muddy or muffled.",
                    detail="Energy from 200-400Hz is elevated.",
                ),
                SpeechIssue(
                    code="weak_clarity",
                    priority_score=0.08,
                    band="clarity_2_5khz",
                    message="Speech clarity may be weak.",
                    detail="Energy from 2-5kHz is low.",
                ),
            ],
        ),
    )
    rows = build_sample_comparison([report], labels={"samples/private/bad-02.wav": "bad"})

    table = sample_comparison_to_markdown(rows)

    assert table == "\n".join(
        [
            "| Sample | Expected label | Overall status | Dominant speech issue | Top issues | low_end_80_200hz | muddy_200_400hz | boxy_300_600hz | clarity_2_5khz | harsh_6_8khz |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            "| bad-02 | bad | WARNING | muddy_low_mids | muddy_low_mids, weak_clarity |  | 0.360 |  |  |  |",
        ]
    )


def _report(path, speech_analysis):
    return AnalysisReport(
        path=path,
        metrics=LevelMetrics(
            duration_seconds=1.0,
            sample_rate=16000,
            channels=1,
            peak_dbfs=-6.0,
            rms_dbfs=-18.0,
            crest_factor_db=12.0,
            clipping_count=0,
            clipping_ratio=0.0,
            left_right_balance_db=0.0,
            noise_floor_dbfs=-60.0,
        ),
        bands=BandMetrics(
            relative_energy={
                "low": 0.05,
                "low_mid": 0.45,
                "speech_mid": 0.25,
                "upper_mid": 0.20,
                "high": 0.05,
            },
            dominant_band="low_mid",
        ),
        judgments=[
            Judgment(
                code="muddy_low_mids",
                severity="info",
                message="The voice may sound muddy in the low-mid range.",
                detail="Low-mid energy dominates the measured energy.",
            )
        ],
        speech_analysis=speech_analysis,
    )

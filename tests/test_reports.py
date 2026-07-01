import json

import pytest

from soundcheck.judgments import Judgment
from soundcheck.metrics import LevelMetrics
from soundcheck.reports import AnalysisReport
from soundcheck.speech_analyzer import SpeechClarityAnalysis, SpeechIssue
from soundcheck.speech_bands import BandMetrics


def test_analysis_report_to_dict_uses_stable_schema():
    report = _example_report()

    report_data = report.to_dict()

    assert set(report_data) == {"path", "metrics", "bands", "judgments"}
    assert set(report_data["metrics"]) == {
        "duration_seconds",
        "sample_rate",
        "channels",
        "peak_dbfs",
        "rms_dbfs",
        "crest_factor_db",
        "clipping_count",
        "clipping_ratio",
        "left_right_balance_db",
        "noise_floor_dbfs",
    }
    assert set(report_data["bands"]) == {"relative_energy", "dominant_band"}
    assert set(report_data["judgments"][0]) == {"code", "severity", "message", "detail"}


def test_analysis_report_to_dict_is_json_serializable():
    report_data = _example_report().to_dict()

    encoded = json.dumps(report_data, sort_keys=True)
    decoded = json.loads(encoded)

    assert decoded["path"] == "speech.wav"
    assert decoded["metrics"]["sample_rate"] == 16000
    assert decoded["bands"]["dominant_band"] == "speech_mid"
    assert decoded["judgments"][0]["code"] == "no_major_issue"


def test_analysis_report_to_dict_includes_week_3_speech_clarity_analysis():
    report = AnalysisReport(
        path="speech.wav",
        metrics=_example_report().metrics,
        bands=_example_report().bands,
        judgments=_example_report().judgments,
        speech_analysis=SpeechClarityAnalysis(
            band_scores={
                "low_end_80_200hz": 0.05,
                "muddy_200_400hz": 0.10,
                "boxy_300_600hz": 0.12,
                "clarity_2_5khz": 0.45,
                "harsh_6_8khz": 0.28,
            },
            top_issues=[
                SpeechIssue(
                    code="harsh_upper_mid",
                    priority_score=0.08,
                    band="harsh_6_8khz",
                    message="The voice may sound harsh or sharp.",
                    detail="Energy from 6-8kHz is elevated compared with the speech reference bands.",
                )
            ],
        ),
    )

    report_data = report.to_dict()

    assert set(report_data) == {
        "path",
        "metrics",
        "bands",
        "judgments",
        "speech_clarity_analysis",
    }
    assert report_data["speech_clarity_analysis"]["band_scores"]["harsh_6_8khz"] == 0.28
    assert report_data["speech_clarity_analysis"]["top_issues"][0]["code"] == "harsh_upper_mid"
    assert report_data["speech_clarity_analysis"]["top_issues"][0]["band"] == "harsh_6_8khz"


def test_week_1_report_fields_map_stable_template_sections():
    report_fields = _example_report().to_week_1_report_fields()

    assert set(report_fields) == {
        "report_header",
        "overall_result",
        "top_issues",
        "beginner_summary",
        "engineer_details",
        "band_energy",
    }
    assert report_fields["report_header"]["report_title"] == "Church Audio Guard Speech Check"
    assert report_fields["report_header"]["analysis_date"] == ""
    assert report_fields["report_header"]["sample_id"] == ""
    assert report_fields["report_header"]["file_name_or_input_source"] == "speech.wav"
    assert report_fields["report_header"]["source_type"] == ""
    assert report_fields["report_header"]["reviewer"] == ""
    assert report_fields["overall_result"] == {
        "overall_status": "GOOD",
        "main_finding": "No major first-pass issue was detected.",
        "confidence": "Low",
        "usable_for_demo": "No",
    }
    assert report_fields["top_issues"] == []
    assert report_fields["engineer_details"]["duration"] == "1.00s"
    assert report_fields["engineer_details"]["channels"] == "Mono"
    assert report_fields["engineer_details"]["clipping_evidence"] == "None"
    assert report_fields["band_energy"]["dominant_band"] == "speech_mid"
    assert report_fields["band_energy"]["relative_energy"]["speech_mid"] == 0.55


def test_week_4_report_fields_include_score_breakdown():
    report_fields = _example_report().to_week_4_report_fields()

    assert set(report_fields) == {
        "report_header",
        "overall_result",
        "score_breakdown",
        "top_issues",
        "beginner_summary",
        "beginner_troubleshooting_guide",
        "baseline_recommendation",
        "engineer_details",
        "band_energy",
    }
    assert report_fields["overall_result"]["overall_score"] == 100
    assert report_fields["overall_result"]["overall_status"] == "GOOD"
    assert report_fields["score_breakdown"] == {
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
    assert report_fields["beginner_troubleshooting_guide"] == [
        "Play the sample through normal listening speakers or headphones.",
        "Confirm the speech is easy to understand before saving it as a reference.",
        "Keep the current gain and EQ settings unless the listening check finds a problem.",
    ]
    assert report_fields["baseline_recommendation"] == (
        "This sample can be considered as a baseline candidate after a listening check."
    )


def test_week_1_report_fields_map_problem_ids_and_danger_status():
    report = AnalysisReport(
        path="clipped.wav",
        metrics=LevelMetrics(
            duration_seconds=1.0,
            sample_rate=16000,
            channels=2,
            peak_dbfs=-0.1,
            rms_dbfs=-10.0,
            crest_factor_db=9.9,
            clipping_count=12,
            clipping_ratio=0.001,
            left_right_balance_db=8.0,
            noise_floor_dbfs=-40.0,
        ),
        bands=BandMetrics(
            relative_energy={
                "low": 0.4,
                "low_mid": 0.2,
                "speech_mid": 0.1,
                "upper_mid": 0.4,
                "high": 0.0,
            },
            dominant_band="upper_mid",
        ),
        judgments=[
            Judgment(
                code="possible_clipping",
                severity="warning",
                message="Possible clipping or digital overload was detected.",
                detail="Peaks are near full scale.",
            ),
            Judgment(
                code="balance_mismatch",
                severity="info",
                message="Left and right channels may be unbalanced.",
                detail="Stereo channel levels differ by more than 6 dB.",
            ),
        ],
    )

    report_fields = report.to_week_1_report_fields()

    assert report_fields["overall_result"]["overall_status"] == "DANGER"
    assert report_fields["top_issues"][0]["problem_id"] == "P3"
    assert report_fields["top_issues"][1]["problem_id"] == "P9"
    assert report_fields["engineer_details"]["channels"] == "Stereo"
    assert report_fields["engineer_details"]["clipping_evidence"] == "Clear"
    assert report_fields["engineer_details"]["low_end_balance"] == "Too much"
    assert report_fields["engineer_details"]["speech_clarity"] == "Harsh"
    assert report_fields["engineer_details"]["left_right_balance"] == "Mismatch"


def test_week_1_report_fields_map_muddy_low_mids_to_p5():
    report = AnalysisReport(
        path="muddy.wav",
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
                "low": 0.15,
                "low_mid": 0.42,
                "speech_mid": 0.25,
                "upper_mid": 0.12,
                "high": 0.06,
            },
            dominant_band="low_mid",
        ),
        judgments=[
            Judgment(
                code="muddy_low_mids",
                severity="info",
                message="The voice may sound muddy in the low-mid range.",
                detail="Low-mid energy dominates the measured energy.",
            ),
        ],
    )

    report_fields = report.to_week_1_report_fields()

    assert report_fields["overall_result"]["overall_status"] == "WARNING"
    assert report_fields["top_issues"][0]["problem_id"] == "P5"
    assert "low-mid" in report_fields["top_issues"][0]["suggested_next_action"]


def test_week_1_report_fields_map_high_noise_floor_to_p8():
    report = AnalysisReport(
        path="noisy.wav",
        metrics=LevelMetrics(
            duration_seconds=1.0,
            sample_rate=16000,
            channels=1,
            peak_dbfs=-12.0,
            rms_dbfs=-24.0,
            crest_factor_db=12.0,
            clipping_count=0,
            clipping_ratio=0.0,
            left_right_balance_db=0.0,
            noise_floor_dbfs=-38.0,
        ),
        bands=BandMetrics(
            relative_energy={
                "low": 0.05,
                "low_mid": 0.15,
                "speech_mid": 0.50,
                "upper_mid": 0.20,
                "high": 0.10,
            },
            dominant_band="speech_mid",
        ),
        judgments=[
            Judgment(
                code="high_noise_floor",
                severity="info",
                message="Background noise may be high compared with the speech level.",
                detail="Quiet passages are relatively loud.",
            ),
        ],
    )

    report_fields = report.to_week_1_report_fields()

    assert report_fields["overall_result"]["overall_status"] == "WARNING"
    assert report_fields["top_issues"][0]["problem_id"] == "P8"
    assert report_fields["engineer_details"]["noise_floor"] == "High"


def test_week_1_report_fields_limit_top_issues_to_first_three_problems():
    report = AnalysisReport(
        path="many-problems.wav",
        metrics=LevelMetrics(
            duration_seconds=1.0,
            sample_rate=16000,
            channels=1,
            peak_dbfs=-0.1,
            rms_dbfs=-10.0,
            crest_factor_db=9.9,
            clipping_count=12,
            clipping_ratio=0.001,
            left_right_balance_db=8.0,
            noise_floor_dbfs=-38.0,
        ),
        bands=BandMetrics(
            relative_energy={
                "low": 0.35,
                "low_mid": 0.25,
                "speech_mid": 0.10,
                "upper_mid": 0.45,
                "high": 0.05,
            },
            dominant_band="upper_mid",
        ),
        judgments=[
            Judgment(
                code="no_major_issue",
                severity="ok",
                message="No major first-pass issue was detected.",
                detail="Validate this result with listening checks.",
            ),
            Judgment(
                code="possible_clipping",
                severity="warning",
                message="Possible clipping or digital overload was detected.",
                detail="Peaks are near full scale.",
            ),
            Judgment(
                code="excess_low_end",
                severity="info",
                message="The sample may have too much low-frequency energy.",
                detail="Low energy is high compared with speech bands.",
            ),
            Judgment(
                code="harsh_upper_mid",
                severity="info",
                message="Speech may sound harsh in the upper-mid range.",
                detail="Upper-mid energy is elevated.",
            ),
            Judgment(
                code="high_noise_floor",
                severity="info",
                message="Background noise may be high compared with the speech level.",
                detail="Quiet passages are relatively loud.",
            ),
        ],
    )

    report_fields = report.to_week_1_report_fields()

    assert [issue["priority"] for issue in report_fields["top_issues"]] == [1, 2, 3]
    assert [issue["problem_id"] for issue in report_fields["top_issues"]] == ["P3", "P4", "P7"]


@pytest.mark.parametrize(
    ("judgment_code", "problem_id"),
    [
        ("too_quiet", "P1"),
        ("too_loud", "P2"),
        ("possible_clipping", "P3"),
        ("excess_low_end", "P4"),
        ("muddy_low_mids", "P5"),
        ("weak_clarity", "P6"),
        ("harsh_upper_mid", "P7"),
        ("high_noise_floor", "P8"),
        ("balance_mismatch", "P9"),
    ],
)
def test_week_1_report_fields_map_all_problem_ids(judgment_code, problem_id):
    report = AnalysisReport(
        path="problem.wav",
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
                "low_mid": 0.15,
                "speech_mid": 0.55,
                "upper_mid": 0.20,
                "high": 0.05,
            },
            dominant_band="speech_mid",
        ),
        judgments=[
            Judgment(
                code=judgment_code,
                severity="warning",
                message=f"{judgment_code} message",
                detail=f"{judgment_code} detail",
            ),
        ],
    )

    report_fields = report.to_week_1_report_fields()

    assert report_fields["top_issues"][0]["problem_id"] == problem_id
    assert report_fields["top_issues"][0]["suggested_next_action"]


def _example_report():
    return AnalysisReport(
        path="speech.wav",
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
                "low_mid": 0.15,
                "speech_mid": 0.55,
                "upper_mid": 0.2,
                "high": 0.05,
            },
            dominant_band="speech_mid",
        ),
        judgments=[
            Judgment(
                code="no_major_issue",
                severity="ok",
                message="No major first-pass issue was detected.",
                detail="Validate this result with listening checks.",
            )
        ],
    )

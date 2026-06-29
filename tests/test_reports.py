import json

from soundcheck.judgments import Judgment
from soundcheck.metrics import LevelMetrics
from soundcheck.reports import AnalysisReport
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

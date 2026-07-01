import pytest

from soundcheck.judgments import Judgment
from soundcheck.metrics import LevelMetrics
from soundcheck.pdf_report import write_week_4_pdf_report
from soundcheck.reports import AnalysisReport
from soundcheck.speech_bands import BandMetrics


pytest.importorskip("reportlab")


def test_write_week_4_pdf_report_creates_pdf(tmp_path):
    output_path = tmp_path / "reports" / "week-4.pdf"

    written_path = write_week_4_pdf_report(_example_report(), str(output_path))

    assert written_path == output_path
    assert output_path.read_bytes().startswith(b"%PDF")
    assert output_path.stat().st_size > 1000


def _example_report():
    return AnalysisReport(
        path="synthetic-demo-speech.wav",
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

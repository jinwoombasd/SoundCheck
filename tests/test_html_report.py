from soundcheck.html_report import render_week_4_html_report, write_week_4_html_report
from soundcheck.judgments import Judgment
from soundcheck.metrics import LevelMetrics
from soundcheck.reports import AnalysisReport
from soundcheck.speech_bands import BandMetrics


def test_render_week_4_html_report_contains_score_and_sections():
    html = render_week_4_html_report(_example_report())

    assert "<!doctype html>" in html
    assert "Church Audio Guard Speech Check" in html
    assert "100/100" in html
    assert "Score Breakdown" in html
    assert "Beginner Troubleshooting Guide" in html
    assert "Baseline:" in html
    assert "Engineer Details" in html
    assert "speech_mid" in html


def test_render_week_4_html_report_keeps_review_order_and_viewport():
    html = render_week_4_html_report(_example_report())

    assert '<meta name="viewport" content="width=device-width, initial-scale=1">' in html
    assert html.index('<section class="report-header">') < html.index("Score Breakdown")
    assert html.index("Score Breakdown") < html.index("Top Issues")
    assert html.index("Top Issues") < html.index("Beginner Troubleshooting Guide")
    assert html.index("Beginner Troubleshooting Guide") < html.index("Engineer Details")


def test_render_week_4_html_report_escapes_report_text():
    report = AnalysisReport(
        path='speech"<unsafe>.wav',
        metrics=_example_report().metrics,
        bands=_example_report().bands,
        judgments=[
            Judgment(
                code="too_quiet",
                severity="warning",
                message="Speech <level> is too low.",
                detail='Raise "gain" cautiously.',
            )
        ],
    )

    html = render_week_4_html_report(report)

    assert 'speech&quot;&lt;unsafe&gt;.wav' in html
    assert "Speech &lt;level&gt; is too low." in html
    assert "Raise &quot;gain&quot; cautiously." in html
    assert 'speech"<unsafe>.wav' not in html


def test_write_week_4_html_report_creates_parent_directories(tmp_path):
    output_path = tmp_path / "reports" / "week-4.html"

    written_path = write_week_4_html_report(_example_report(), str(output_path))

    assert written_path == output_path
    assert output_path.read_text(encoding="utf-8").startswith("<!doctype html>")


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

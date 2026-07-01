from html import escape
from pathlib import Path
from typing import Any, Dict

from .reports import AnalysisReport


def render_week_4_html_report(report: AnalysisReport) -> str:
    fields = report.to_week_4_report_fields()
    header = fields["report_header"]
    overall = fields["overall_result"]
    scores = fields["score_breakdown"]

    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{_text(header['report_title'])}</title>",
            "<style>",
            _stylesheet(),
            "</style>",
            "</head>",
            "<body>",
            "<main>",
            _header_html(header, overall),
            _score_summary_html(scores),
            _issues_html(fields),
            _beginner_guide_html(fields),
            _engineer_details_html(fields),
            "</main>",
            "</body>",
            "</html>",
        ]
    )


def write_week_4_html_report(report: AnalysisReport, output_path: str) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_week_4_html_report(report), encoding="utf-8")
    return path


def _header_html(header: Dict[str, Any], overall: Dict[str, Any]) -> str:
    return "\n".join(
        [
            "<section class=\"report-header\">",
            f"<h1>{_text(header['report_title'])}</h1>",
            f"<p>{_text(header['file_name_or_input_source'])}</p>",
            "<div class=\"status-row\">",
            f"<strong>{_text(overall['overall_status'])}</strong>",
            f"<span>{int(overall['overall_score'])}/100</span>",
            "</div>",
            f"<p>{_text(overall['main_finding'])}</p>",
            "</section>",
        ]
    )


def _score_summary_html(scores: Dict[str, Any]) -> str:
    rows = [
        ("Level", scores["level"], 20),
        ("Clipping", scores["clipping"], 20),
        ("Speech clarity", scores["speech_clarity"], 20),
        ("Low-end balance", scores["low_end_balance"], 15),
        ("Harshness", scores["harshness"], 10),
        ("Noise", scores["noise"], 10),
        ("Stereo", scores["stereo"], 5),
    ]
    table_rows = "\n".join(
        f"<tr><td>{_text(label)}</td><td>{int(value)}/{maximum}</td></tr>"
        for label, value, maximum in rows
    )
    return "\n".join(
        [
            "<section>",
            "<h2>Score Breakdown</h2>",
            "<table>",
            "<thead><tr><th>Check</th><th>Score</th></tr></thead>",
            f"<tbody>{table_rows}</tbody>",
            "</table>",
            "</section>",
        ]
    )


def _issues_html(fields: Dict[str, Any]) -> str:
    issues = fields["top_issues"]
    if not issues:
        content = "<p>No prioritized issue was detected in the first-pass analysis.</p>"
    else:
        content = "\n".join(
            "\n".join(
                [
                    "<article>",
                    f"<h3>{issue['priority']}. {_text(issue['problem_id'])}</h3>",
                    f"<p>{_text(issue['listener_facing_explanation'])}</p>",
                    f"<p><strong>Engineer note:</strong> {_text(issue['engineer_note'])}</p>",
                    f"<p><strong>Next action:</strong> {_text(issue['suggested_next_action'])}</p>",
                    "</article>",
                ]
            )
            for issue in issues
        )
    return "\n".join(["<section>", "<h2>Top Issues</h2>", content, "</section>"])


def _beginner_guide_html(fields: Dict[str, Any]) -> str:
    steps = "\n".join(
        f"<li>{_text(step)}</li>" for step in fields["beginner_troubleshooting_guide"]
    )
    return "\n".join(
        [
            "<section>",
            "<h2>Beginner Troubleshooting Guide</h2>",
            f"<p>{_text(fields['beginner_summary'])}</p>",
            f"<ol>{steps}</ol>",
            f"<p><strong>Baseline:</strong> {_text(fields['baseline_recommendation'])}</p>",
            "</section>",
        ]
    )


def _engineer_details_html(fields: Dict[str, Any]) -> str:
    details = fields["engineer_details"]
    band_energy = fields["band_energy"]
    rows = [
        ("Duration", details["duration"]),
        ("Channels", details["channels"]),
        ("Peak level", details["peak_level"]),
        ("RMS estimate", details["rms_or_loudness_estimate"]),
        ("Clipping evidence", details["clipping_evidence"]),
        ("Low-end balance", details["low_end_balance"]),
        ("Speech clarity", details["speech_clarity"]),
        ("Noise floor", details["noise_floor"]),
        ("Left/right balance", details["left_right_balance"]),
        ("Dominant band", band_energy["dominant_band"]),
    ]
    table_rows = "\n".join(
        f"<tr><td>{_text(label)}</td><td>{_text(value)}</td></tr>" for label, value in rows
    )
    return "\n".join(
        [
            "<section>",
            "<h2>Engineer Details</h2>",
            "<table>",
            "<tbody>",
            table_rows,
            "</tbody>",
            "</table>",
            "</section>",
        ]
    )


def _text(value: Any) -> str:
    return escape(str(value), quote=True)


def _stylesheet() -> str:
    return """
body {
  background: #f7f8fa;
  color: #1f2933;
  font-family: Arial, sans-serif;
  line-height: 1.5;
  margin: 0;
}
main {
  margin: 0 auto;
  max-width: 880px;
  padding: 32px 20px;
}
section {
  background: #ffffff;
  border: 1px solid #d9e2ec;
  border-radius: 8px;
  margin-bottom: 20px;
  padding: 20px;
}
h1, h2, h3, p {
  margin-top: 0;
}
.status-row {
  align-items: center;
  display: flex;
  gap: 12px;
  margin: 16px 0;
}
.status-row strong {
  background: #d9ead3;
  border-radius: 999px;
  padding: 6px 12px;
}
table {
  border-collapse: collapse;
  width: 100%;
}
td, th {
  border-top: 1px solid #d9e2ec;
  padding: 10px 8px;
  text-align: left;
}
article {
  border-top: 1px solid #d9e2ec;
  padding-top: 16px;
}
""".strip()

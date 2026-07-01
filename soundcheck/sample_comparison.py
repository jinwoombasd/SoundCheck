from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

from .reports import AnalysisReport
from .speech_analyzer import SPEECH_CLARITY_BANDS


BAND_SCORE_COLUMNS = list(SPEECH_CLARITY_BANDS.keys())


@dataclass(frozen=True)
class SampleComparisonRow:
    sample_id: str
    path: str
    expected_label: str
    overall_status: str
    top_issue_codes: List[str]
    dominant_speech_issue: str
    band_scores: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sample_id": self.sample_id,
            "path": self.path,
            "expected_label": self.expected_label,
            "overall_status": self.overall_status,
            "top_issue_codes": self.top_issue_codes,
            "dominant_speech_issue": self.dominant_speech_issue,
            "band_scores": self.band_scores,
        }


def build_sample_comparison(
    reports: Iterable[AnalysisReport],
    labels: Optional[Mapping[str, str]] = None,
) -> List[SampleComparisonRow]:
    label_map = labels or {}
    return [_comparison_row(report, label_map.get(report.path, "")) for report in reports]


def sample_comparison_to_markdown(rows: Iterable[SampleComparisonRow]) -> str:
    headers = [
        "Sample",
        "Expected label",
        "Overall status",
        "Dominant speech issue",
        "Top issues",
        *BAND_SCORE_COLUMNS,
    ]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]

    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    _escape_markdown_cell(row.sample_id),
                    _escape_markdown_cell(row.expected_label),
                    _escape_markdown_cell(row.overall_status),
                    _escape_markdown_cell(row.dominant_speech_issue),
                    _escape_markdown_cell(", ".join(row.top_issue_codes)),
                    *[_format_score(row.band_scores.get(column)) for column in BAND_SCORE_COLUMNS],
                ]
            )
            + " |"
        )

    return "\n".join(lines)


def _comparison_row(report: AnalysisReport, expected_label: str) -> SampleComparisonRow:
    speech_analysis = report.speech_analysis
    top_issues = speech_analysis.top_issues if speech_analysis is not None else []
    band_scores = speech_analysis.band_scores if speech_analysis is not None else {}
    top_issue_codes = [issue.code for issue in top_issues]

    return SampleComparisonRow(
        sample_id=Path(report.path).stem,
        path=report.path,
        expected_label=expected_label,
        overall_status=report.to_week_1_report_fields()["overall_result"]["overall_status"],
        top_issue_codes=top_issue_codes,
        dominant_speech_issue=top_issue_codes[0] if top_issue_codes else "",
        band_scores=band_scores,
    )


def _escape_markdown_cell(value: str) -> str:
    return value.replace("|", "\\|")


def _format_score(value: Optional[float]) -> str:
    if value is None:
        return ""
    return f"{value:.3f}"

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from .reports import AnalysisReport


def write_week_4_pdf_report(report: AnalysisReport, output_path: str) -> Path:
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            PageBreak,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )
    except ImportError as exc:
        raise ImportError(
            "PDF export requires reportlab. Install it with `python3 -m pip install '.[pdf]'`."
        ) from exc

    fields = report.to_week_4_report_fields()
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            fontSize=13,
            leading=16,
            spaceBefore=14,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallBody",
            parent=styles["BodyText"],
            fontSize=9,
            leading=12,
        )
    )

    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title=fields["report_header"]["report_title"],
    )
    story = _build_story(fields, styles, colors, Table, TableStyle, Paragraph, Spacer, PageBreak)
    doc.build(story)
    return path


def _build_story(
    fields: Dict[str, Any],
    styles: Any,
    colors: Any,
    table_cls: Any,
    table_style_cls: Any,
    paragraph_cls: Any,
    spacer_cls: Any,
    page_break_cls: Any,
) -> List[Any]:
    header = fields["report_header"]
    overall = fields["overall_result"]
    scores = fields["score_breakdown"]
    story: List[Any] = [
        paragraph_cls(header["report_title"], styles["Title"]),
        paragraph_cls(f"Source: {header['file_name_or_input_source']}", styles["SmallBody"]),
        spacer_cls(1, 10),
        _table(
            table_cls,
            table_style_cls,
            paragraph_cls,
            styles,
            colors,
            [
                ("Overall status", overall["overall_status"]),
                ("Overall score", f"{overall['overall_score']}/100"),
                ("Main finding", overall["main_finding"]),
                ("Baseline recommendation", fields["baseline_recommendation"]),
            ],
            column_widths=(150, 340),
        ),
        paragraph_cls("Score Breakdown", styles["SectionTitle"]),
        _table(
            table_cls,
            table_style_cls,
            paragraph_cls,
            styles,
            colors,
            _score_rows(scores),
            column_widths=(220, 120),
        ),
        paragraph_cls("Top Issues", styles["SectionTitle"]),
    ]

    if fields["top_issues"]:
        story.append(
            _table(
                table_cls,
                table_style_cls,
                paragraph_cls,
                styles,
                colors,
                _issue_rows(fields["top_issues"]),
                column_widths=(55, 115, 320),
            )
        )
    else:
        story.append(paragraph_cls("No prioritized issue was detected in the first-pass analysis.", styles["BodyText"]))

    story.extend(
        [
            paragraph_cls("Beginner Troubleshooting Guide", styles["SectionTitle"]),
            paragraph_cls(fields["beginner_summary"], styles["BodyText"]),
            _table(
                table_cls,
                table_style_cls,
                paragraph_cls,
                styles,
                colors,
                [(str(index + 1), step) for index, step in enumerate(fields["beginner_troubleshooting_guide"])],
                column_widths=(35, 455),
            ),
            page_break_cls(),
            paragraph_cls("Engineer Details", styles["SectionTitle"]),
            _table(
                table_cls,
                table_style_cls,
                paragraph_cls,
                styles,
                colors,
                _engineer_rows(fields),
                column_widths=(175, 315),
            ),
        ]
    )
    return story


def _table(
    table_cls: Any,
    table_style_cls: Any,
    paragraph_cls: Any,
    styles: Any,
    colors: Any,
    rows: Iterable[Tuple[str, Any]],
    column_widths: Tuple[int, ...],
) -> Any:
    if len(column_widths) == 3:
        data = [
            [
                paragraph_cls(str(first), styles["SmallBody"]),
                paragraph_cls(str(second), styles["SmallBody"]),
                paragraph_cls(str(third), styles["SmallBody"]),
            ]
            for first, second, third in rows
        ]
    else:
        data = [
            [
                paragraph_cls(str(left), styles["SmallBody"]),
                paragraph_cls(str(right), styles["SmallBody"]),
            ]
            for left, right in rows
        ]

    table = table_cls(data, colWidths=list(column_widths), hAlign="LEFT")
    table.setStyle(
        table_style_cls(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef2f7")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def _score_rows(scores: Dict[str, Any]) -> List[Tuple[str, str]]:
    return [
        ("Check", "Score"),
        ("Level", f"{scores['level']}/20"),
        ("Clipping", f"{scores['clipping']}/20"),
        ("Speech clarity", f"{scores['speech_clarity']}/20"),
        ("Low-end balance", f"{scores['low_end_balance']}/15"),
        ("Harshness", f"{scores['harshness']}/10"),
        ("Noise", f"{scores['noise']}/10"),
        ("Stereo", f"{scores['stereo']}/5"),
    ]


def _issue_rows(issues: List[Dict[str, Any]]) -> List[Tuple[str, str, str]]:
    rows = [("Priority", "Problem", "Finding and next action")]
    for issue in issues:
        rows.append(
            (
                str(issue["priority"]),
                issue["problem_id"],
                f"{issue['listener_facing_explanation']} Next: {issue['suggested_next_action']}",
            )
        )
    return rows


def _engineer_rows(fields: Dict[str, Any]) -> List[Tuple[str, Any]]:
    details = fields["engineer_details"]
    band_energy = fields["band_energy"]
    rows: List[Tuple[str, Any]] = [
        ("Metric", "Value"),
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
    rows.extend(
        (f"Band energy: {band}", f"{value:.3f}")
        for band, value in band_energy["relative_energy"].items()
    )
    return rows

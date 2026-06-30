from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from .judgments import Judgment
from .metrics import LevelMetrics
from .speech_bands import BandMetrics


@dataclass(frozen=True)
class AnalysisReport:
    path: str
    metrics: LevelMetrics
    bands: BandMetrics
    judgments: List[Judgment]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "metrics": asdict(self.metrics),
            "bands": asdict(self.bands),
            "judgments": [asdict(judgment) for judgment in self.judgments],
        }

    def to_week_1_report_fields(self) -> Dict[str, Any]:
        top_judgments = [judgment for judgment in self.judgments if judgment.code != "no_major_issue"][:3]
        main_judgment = self.judgments[0] if self.judgments else None
        return {
            "report_header": {
                "report_title": "Church Audio Guard Speech Check",
                "analysis_date": "",
                "sample_id": "",
                "file_name_or_input_source": self.path,
                "source_type": "",
                "reviewer": "",
            },
            "overall_result": {
                "overall_status": _overall_status(self.judgments),
                "main_finding": main_judgment.message if main_judgment else "",
                "confidence": "Low",
                "usable_for_demo": "No",
            },
            "top_issues": [
                {
                    "priority": index + 1,
                    "problem_id": _problem_id_for(judgment.code),
                    "listener_facing_explanation": judgment.message,
                    "engineer_note": judgment.detail,
                    "suggested_next_action": _suggested_next_action(judgment.code),
                }
                for index, judgment in enumerate(top_judgments)
            ],
            "beginner_summary": _beginner_summary(self.judgments),
            "engineer_details": {
                "duration": f"{self.metrics.duration_seconds:.2f}s",
                "channels": "Mono" if self.metrics.channels == 1 else "Stereo",
                "peak_level": f"{self.metrics.peak_dbfs:.1f} dBFS",
                "rms_or_loudness_estimate": f"{self.metrics.rms_dbfs:.1f} dBFS",
                "clipping_evidence": _clipping_evidence(self.metrics),
                "low_end_balance": _low_end_balance(self.bands),
                "speech_clarity": _speech_clarity(self.bands),
                "noise_floor": "High" if self.metrics.noise_floor_dbfs > -45.0 else "OK",
                "left_right_balance": "Mismatch" if abs(self.metrics.left_right_balance_db) > 6.0 else "OK",
            },
            "band_energy": {
                "dominant_band": self.bands.dominant_band,
                "relative_energy": self.bands.relative_energy,
            },
        }


_PROBLEM_IDS = {
    "too_quiet": "P1",
    "too_loud": "P2",
    "possible_clipping": "P3",
    "excess_low_end": "P4",
    "muddy_low_mids": "P5",
    "weak_clarity": "P6",
    "harsh_upper_mid": "P7",
    "high_noise_floor": "P8",
    "balance_mismatch": "P9",
}

_NEXT_ACTIONS = {
    "too_quiet": "Check the speech microphone level before changing EQ.",
    "too_loud": "Lower the source level before adding downstream gain.",
    "possible_clipping": "Lower the source gain before raising downstream output level.",
    "excess_low_end": "Review microphone placement and high-pass filter settings.",
    "muddy_low_mids": "Compare microphone placement and low-mid EQ against a known good reference.",
    "weak_clarity": "Compare this sample against a known good reference from the same room.",
    "harsh_upper_mid": "Compare the speech tone with a known good reference before changing EQ.",
    "high_noise_floor": "Check room, fan, hum, and input noise before applying processing.",
    "balance_mismatch": "Check stereo routing and pan settings.",
}


def _overall_status(judgments: List[Judgment]) -> str:
    if any(judgment.code == "possible_clipping" for judgment in judgments):
        return "DANGER"
    if any(judgment.severity in {"warning", "info"} for judgment in judgments):
        return "WARNING"
    return "GOOD"


def _problem_id_for(code: str) -> str:
    return _PROBLEM_IDS.get(code, "")


def _suggested_next_action(code: str) -> str:
    return _NEXT_ACTIONS.get(code, "Validate this result with listening checks.")


def _beginner_summary(judgments: List[Judgment]) -> str:
    if not judgments:
        return ""
    if judgments[0].code == "no_major_issue":
        return "The speech sample has no major first-pass issue. Confirm the result with a listening check."
    return f"{judgments[0].message} Confirm this result with a listening check before making changes."


def _clipping_evidence(metrics: LevelMetrics) -> str:
    if metrics.clipping_count > 0 or metrics.clipping_ratio > 0.0005:
        return "Clear"
    if metrics.peak_dbfs > -1.0:
        return "Possible"
    return "None"


def _low_end_balance(bands: BandMetrics) -> str:
    low_energy = bands.relative_energy.get("low", 0.0) + bands.relative_energy.get("low_mid", 0.0)
    if low_energy > 0.50:
        return "Too much"
    return "OK"


def _speech_clarity(bands: BandMetrics) -> str:
    if bands.relative_energy.get("upper_mid", 0.0) > 0.35:
        return "Harsh"
    if bands.relative_energy.get("speech_mid", 0.0) < 0.18:
        return "Weak"
    return "OK"

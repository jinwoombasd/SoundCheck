from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple

from .audio_data import AudioData
from .speech_bands import calculate_relative_energy


SPEECH_CLARITY_BANDS: Dict[str, Tuple[float, float]] = {
    "low_end_80_200hz": (80.0, 200.0),
    "muddy_200_400hz": (200.0, 400.0),
    "boxy_300_600hz": (300.0, 600.0),
    "clarity_2_5khz": (2000.0, 5000.0),
    "harsh_6_8khz": (6000.0, 8000.0),
}


@dataclass(frozen=True)
class SpeechIssue:
    code: str
    priority_score: float
    band: str
    message: str
    detail: str


@dataclass(frozen=True)
class SpeechClarityAnalysis:
    band_scores: Dict[str, float]
    top_issues: List[SpeechIssue]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "band_scores": self.band_scores,
            "top_issues": [asdict(issue) for issue in self.top_issues],
        }


def analyze_speech_clarity(audio: AudioData) -> SpeechClarityAnalysis:
    band_scores = calculate_relative_energy(audio, SPEECH_CLARITY_BANDS)
    issues = _build_speech_issues(band_scores)
    return SpeechClarityAnalysis(band_scores=band_scores, top_issues=issues[:3])


def _build_speech_issues(band_scores: Dict[str, float]) -> List[SpeechIssue]:
    candidates = [
        _high_band_issue(
            band_scores,
            "excess_low_end",
            "low_end_80_200hz",
            0.28,
            "The voice may have too much low-end weight.",
            "Energy from 80-200Hz is elevated compared with the speech reference bands.",
        ),
        _high_band_issue(
            band_scores,
            "muddy_low_mids",
            "muddy_200_400hz",
            0.26,
            "The voice may sound muddy or muffled.",
            "Energy from 200-400Hz is elevated compared with the speech reference bands.",
        ),
        _high_band_issue(
            band_scores,
            "boxy_low_mids",
            "boxy_300_600hz",
            0.24,
            "The voice may sound boxy or closed-in.",
            "Energy from 300-600Hz is elevated compared with the speech reference bands.",
        ),
        _low_band_issue(
            band_scores,
            "weak_clarity",
            "clarity_2_5khz",
            0.16,
            "Speech clarity may be weak.",
            "Energy from 2-5kHz is low compared with the measured problem bands.",
        ),
        _high_band_issue(
            band_scores,
            "harsh_upper_mid",
            "harsh_6_8khz",
            0.20,
            "The voice may sound harsh or sharp.",
            "Energy from 6-8kHz is elevated compared with the speech reference bands.",
        ),
    ]
    issues = [issue for issue in candidates if issue is not None]
    return sorted(issues, key=lambda issue: issue.priority_score, reverse=True)


def _high_band_issue(
    band_scores: Dict[str, float],
    code: str,
    band: str,
    threshold: float,
    message: str,
    detail: str,
) -> Optional[SpeechIssue]:
    score = band_scores.get(band, 0.0)
    if score <= threshold:
        return None
    return SpeechIssue(code, round(score - threshold, 6), band, message, detail)


def _low_band_issue(
    band_scores: Dict[str, float],
    code: str,
    band: str,
    threshold: float,
    message: str,
    detail: str,
) -> Optional[SpeechIssue]:
    score = band_scores.get(band, 0.0)
    if score >= threshold:
        return None
    return SpeechIssue(code, round(threshold - score, 6), band, message, detail)

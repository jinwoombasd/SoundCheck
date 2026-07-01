from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from .metrics import LevelMetrics
from .speech_analyzer import SpeechClarityAnalysis
from .speech_bands import BandMetrics


@dataclass(frozen=True)
class ReportScores:
    overall: int
    level: int
    clipping: int
    speech_clarity: int
    low_end_balance: int
    harshness: int
    noise: int
    stereo: int
    status: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def calculate_report_scores(
    metrics: LevelMetrics,
    bands: BandMetrics,
    speech_analysis: Optional[SpeechClarityAnalysis] = None,
) -> ReportScores:
    level = _level_score(metrics)
    clipping = _clipping_score(metrics)
    speech_clarity = _speech_clarity_score(bands, speech_analysis)
    low_end_balance = _low_end_balance_score(bands)
    harshness = _harshness_score(bands, speech_analysis)
    noise = _noise_score(metrics)
    stereo = _stereo_score(metrics)
    overall = level + clipping + speech_clarity + low_end_balance + harshness + noise + stereo

    return ReportScores(
        overall=overall,
        level=level,
        clipping=clipping,
        speech_clarity=speech_clarity,
        low_end_balance=low_end_balance,
        harshness=harshness,
        noise=noise,
        stereo=stereo,
        status=_status(overall, clipping),
    )


def _level_score(metrics: LevelMetrics) -> int:
    if -24.0 <= metrics.rms_dbfs <= -12.0 and metrics.peak_dbfs <= -1.0:
        return 20
    if -30.0 <= metrics.rms_dbfs < -24.0 or -12.0 < metrics.rms_dbfs <= -6.0:
        return 15
    return 8


def _clipping_score(metrics: LevelMetrics) -> int:
    if metrics.clipping_count > 0 or metrics.clipping_ratio > 0.0005:
        return 0
    if metrics.peak_dbfs > -1.0:
        return 10
    return 20


def _speech_clarity_score(
    bands: BandMetrics,
    speech_analysis: Optional[SpeechClarityAnalysis],
) -> int:
    if speech_analysis is not None:
        issue_codes = {issue.code for issue in speech_analysis.top_issues}
        if "weak_clarity" in issue_codes:
            return 8
        if issue_codes.intersection({"muddy_low_mids", "boxy_low_mids"}):
            return 12
    if bands.relative_energy.get("speech_mid", 0.0) < 0.18:
        return 8
    return 20


def _low_end_balance_score(bands: BandMetrics) -> int:
    low_energy = bands.relative_energy.get("low", 0.0) + bands.relative_energy.get("low_mid", 0.0)
    if low_energy > 0.60:
        return 5
    if low_energy > 0.50:
        return 10
    return 15


def _harshness_score(
    bands: BandMetrics,
    speech_analysis: Optional[SpeechClarityAnalysis],
) -> int:
    if speech_analysis is not None and any(issue.code == "harsh_upper_mid" for issue in speech_analysis.top_issues):
        return 4
    if bands.relative_energy.get("upper_mid", 0.0) > 0.35:
        return 4
    return 10


def _noise_score(metrics: LevelMetrics) -> int:
    if metrics.noise_floor_dbfs > -45.0:
        return 4
    return 10


def _stereo_score(metrics: LevelMetrics) -> int:
    if abs(metrics.left_right_balance_db) > 6.0:
        return 2
    return 5


def _status(overall: int, clipping: int) -> str:
    if clipping == 0 or overall < 50:
        return "DANGER"
    if overall < 90:
        return "WARNING"
    return "GOOD"

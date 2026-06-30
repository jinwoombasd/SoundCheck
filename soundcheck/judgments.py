from dataclasses import dataclass
from typing import List

from .metrics import LevelMetrics
from .speech_bands import BandMetrics


@dataclass(frozen=True)
class Judgment:
    code: str
    severity: str
    message: str
    detail: str


def build_judgments(metrics: LevelMetrics, bands: BandMetrics) -> List[Judgment]:
    judgments: List[Judgment] = []

    if metrics.rms_dbfs < -35.0:
        judgments.append(_warn("too_quiet", "The speech level appears too quiet.", "RMS is below -35 dBFS."))
    elif metrics.rms_dbfs > -12.0:
        judgments.append(_warn("too_loud", "The speech level appears too loud.", "RMS is above -12 dBFS."))

    if metrics.peak_dbfs > -1.0 or metrics.clipping_ratio > 0.0005:
        judgments.append(
            _warn("possible_clipping", "Possible clipping or digital overload was detected.", "Peaks are near full scale.")
        )

    if metrics.noise_floor_dbfs > -45.0 and metrics.rms_dbfs < -20.0:
        judgments.append(
            _info("high_noise_floor", "Background noise may be high compared with the speech level.", "Quiet passages are relatively loud.")
        )

    energy = bands.relative_energy
    low_energy = energy.get("low", 0.0)
    low_mid_energy = energy.get("low_mid", 0.0)
    if low_energy + low_mid_energy > 0.50:
        if low_mid_energy > low_energy:
            judgments.append(_info("muddy_low_mids", "The voice may sound muddy in the low-mid range.", "Low-mid energy dominates the measured energy."))
        else:
            judgments.append(_info("excess_low_end", "The sound may have too much low energy.", "Low bands dominate the measured energy."))

    if energy.get("speech_mid", 0.0) < 0.18:
        judgments.append(_info("weak_clarity", "Speech clarity may be weak.", "Speech-mid energy is low compared with other bands."))

    if energy.get("upper_mid", 0.0) > 0.35:
        judgments.append(_info("harsh_upper_mid", "The sound may be harsh in the upper-mid range.", "Upper-mid energy is elevated."))

    if abs(metrics.left_right_balance_db) > 6.0:
        judgments.append(_info("balance_mismatch", "Left and right channels may be unbalanced.", "Stereo channel levels differ by more than 6 dB."))

    if not judgments:
        judgments.append(_ok("no_major_issue", "No major first-pass issue was detected.", "Validate this result with listening checks."))

    return judgments


def _ok(code: str, message: str, detail: str) -> Judgment:
    return Judgment(code, "ok", message, detail)


def _info(code: str, message: str, detail: str) -> Judgment:
    return Judgment(code, "info", message, detail)


def _warn(code: str, message: str, detail: str) -> Judgment:
    return Judgment(code, "warning", message, detail)

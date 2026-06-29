import math
from dataclasses import dataclass
from typing import List

from .audio_data import AudioData


CLIPPING_THRESHOLD = 0.999
NOISE_FLOOR_WINDOW_SECONDS = 0.05


@dataclass(frozen=True)
class LevelMetrics:
    duration_seconds: float
    sample_rate: int
    channels: int
    peak_dbfs: float
    rms_dbfs: float
    crest_factor_db: float
    clipping_count: int
    clipping_ratio: float
    left_right_balance_db: float
    noise_floor_dbfs: float


def calculate_metrics(audio: AudioData) -> LevelMetrics:
    mono = audio.mono()
    flattened = [sample for frame in audio.samples for sample in frame]
    peak = max(abs(sample) for sample in flattened)
    rms = math.sqrt(sum(sample * sample for sample in flattened) / len(flattened))
    clipping_count = sum(1 for sample in flattened if abs(sample) >= CLIPPING_THRESHOLD)
    clipping_ratio = clipping_count / len(flattened)
    crest_factor_db = _db(peak / rms) if rms > 0 else 0.0

    return LevelMetrics(
        duration_seconds=audio.duration_seconds,
        sample_rate=audio.sample_rate,
        channels=audio.channels,
        peak_dbfs=_dbfs(peak),
        rms_dbfs=_dbfs(rms),
        crest_factor_db=crest_factor_db,
        clipping_count=clipping_count,
        clipping_ratio=clipping_ratio,
        left_right_balance_db=_left_right_balance(audio.samples),
        noise_floor_dbfs=_estimate_noise_floor(mono, audio.sample_rate),
    )


def _left_right_balance(samples: List[List[float]]) -> float:
    if not samples or len(samples[0]) < 2:
        return 0.0

    left_rms = _rms([frame[0] for frame in samples])
    right_rms = _rms([frame[1] for frame in samples])
    if left_rms == 0 and right_rms == 0:
        return 0.0
    return _db((left_rms + 1e-12) / (right_rms + 1e-12))


def _estimate_noise_floor(mono: List[float], sample_rate: int) -> float:
    window_size = max(1, int(sample_rate * NOISE_FLOOR_WINDOW_SECONDS))
    if len(mono) <= window_size:
        return _dbfs(_rms(mono))

    windows = [
        _rms(mono[index : index + window_size])
        for index in range(0, len(mono) - window_size + 1, window_size)
    ]
    quietest = min(windows) if windows else 0.0
    return _dbfs(quietest)


def _rms(values: List[float]) -> float:
    if not values:
        return 0.0
    return math.sqrt(sum(value * value for value in values) / len(values))


def _dbfs(value: float) -> float:
    if value <= 0:
        return -120.0
    return max(-120.0, _db(value))


def _db(ratio: float) -> float:
    if ratio <= 0:
        return -120.0
    return 20.0 * math.log10(ratio)

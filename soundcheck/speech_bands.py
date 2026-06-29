import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

from .audio_data import AudioData


BANDS: Dict[str, Tuple[float, float]] = {
    "low": (80.0, 250.0),
    "low_mid": (250.0, 500.0),
    "speech_mid": (500.0, 2500.0),
    "upper_mid": (2500.0, 5000.0),
    "high": (5000.0, 10000.0),
}

MAX_ANALYSIS_SAMPLES = 12000
POINTS_PER_BAND = 6


@dataclass(frozen=True)
class BandMetrics:
    relative_energy: Dict[str, float]
    dominant_band: str


def calculate_band_metrics(audio: AudioData) -> BandMetrics:
    mono = _trim_or_stride(audio.mono(), MAX_ANALYSIS_SAMPLES)
    if not mono:
        return BandMetrics(relative_energy={name: 0.0 for name in BANDS}, dominant_band="unknown")

    windowed = _apply_hann_window(mono)
    energies = {
        band: _band_energy(windowed, audio.sample_rate, low, high)
        for band, (low, high) in BANDS.items()
    }
    total = sum(energies.values()) or 1.0
    relative = {band: energy / total for band, energy in energies.items()}
    dominant = max(relative, key=relative.get)
    return BandMetrics(relative_energy=relative, dominant_band=dominant)


def _band_energy(samples: List[float], sample_rate: int, low: float, high: float) -> float:
    frequencies = list(_band_frequencies(low, min(high, sample_rate / 2.0 - 1.0)))
    if not frequencies:
        return 0.0
    return sum(_goertzel_power(samples, sample_rate, frequency) for frequency in frequencies) / len(frequencies)


def _band_frequencies(low: float, high: float) -> Iterable[float]:
    if high <= low:
        return []
    if POINTS_PER_BAND == 1:
        return [(low + high) / 2.0]
    ratio = high / low
    return [low * (ratio ** (index / (POINTS_PER_BAND - 1))) for index in range(POINTS_PER_BAND)]


def _goertzel_power(samples: List[float], sample_rate: int, frequency: float) -> float:
    omega = 2.0 * math.pi * frequency / sample_rate
    coefficient = 2.0 * math.cos(omega)
    previous = 0.0
    previous2 = 0.0

    for sample in samples:
        current = sample + coefficient * previous - previous2
        previous2 = previous
        previous = current

    return previous2 * previous2 + previous * previous - coefficient * previous * previous2


def _trim_or_stride(samples: List[float], max_samples: int) -> List[float]:
    if len(samples) <= max_samples:
        return samples
    step = math.ceil(len(samples) / max_samples)
    return samples[::step][:max_samples]


def _apply_hann_window(samples: List[float]) -> List[float]:
    if len(samples) <= 1:
        return samples
    last = len(samples) - 1
    return [
        sample * (0.5 - 0.5 * math.cos(2.0 * math.pi * index / last))
        for index, sample in enumerate(samples)
    ]

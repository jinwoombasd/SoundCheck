import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

from .audio_data import AudioData


BANDS: Dict[str, Tuple[float, float]] = {
    "low": (80.0, 200.0),
    "low_mid": (200.0, 500.0),
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
    relative = calculate_relative_energy(audio, BANDS)
    return BandMetrics(relative_energy=relative, dominant_band=_dominant_band(relative))


def calculate_relative_energy(audio: AudioData, bands: Dict[str, Tuple[float, float]]) -> Dict[str, float]:
    mono = _trim(audio.mono(), MAX_ANALYSIS_SAMPLES)
    if not mono:
        return {name: 0.0 for name in bands}

    windowed = _apply_hann_window(mono)
    energies = {
        band: _band_energy(windowed, audio.sample_rate, low, high)
        for band, (low, high) in bands.items()
    }
    total = sum(energies.values()) or 1.0
    return {band: energy / total for band, energy in energies.items()}


def _dominant_band(relative_energy: Dict[str, float]) -> str:
    if not relative_energy:
        return "unknown"
    return max(relative_energy, key=relative_energy.get)


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
    step = (high - low) / (POINTS_PER_BAND - 1)
    return [low + (step * index) for index in range(POINTS_PER_BAND)]


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


def _trim(samples: List[float], max_samples: int) -> List[float]:
    if len(samples) <= max_samples:
        return samples
    return samples[:max_samples]


def _apply_hann_window(samples: List[float]) -> List[float]:
    if len(samples) <= 1:
        return samples
    last = len(samples) - 1
    return [
        sample * (0.5 - 0.5 * math.cos(2.0 * math.pi * index / last))
        for index, sample in enumerate(samples)
    ]

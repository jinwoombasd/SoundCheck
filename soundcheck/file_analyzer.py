from pathlib import Path

from .audio_data import AudioData
from .judgments import build_judgments
from .loaders import load_audio_file
from .metrics import calculate_metrics
from .reports import AnalysisReport
from .speech_analyzer import analyze_speech_clarity
from .speech_bands import calculate_band_metrics


MIN_DURATION_SECONDS = 0.25


def analyze_file(path: str) -> AnalysisReport:
    audio = load_audio_file(path)
    _validate_audio(audio)

    metrics = calculate_metrics(audio)
    bands = calculate_band_metrics(audio)
    speech_analysis = analyze_speech_clarity(audio)
    judgments = build_judgments(metrics, bands)

    return AnalysisReport(
        path=str(Path(path)),
        metrics=metrics,
        bands=bands,
        speech_analysis=speech_analysis,
        judgments=judgments,
    )


def _validate_audio(audio: AudioData) -> None:
    if audio.sample_rate <= 0:
        raise ValueError("Audio sample rate must be greater than zero.")
    if audio.channels <= 0:
        raise ValueError("Audio must contain at least one channel.")
    if not audio.samples:
        raise ValueError("Audio file contains no samples.")
    if audio.duration_seconds < MIN_DURATION_SECONDS:
        raise ValueError(
            f"Audio file is too short for analysis; minimum is {MIN_DURATION_SECONDS:.2f} seconds."
        )

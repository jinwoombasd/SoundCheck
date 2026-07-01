from soundcheck.audio_data import AudioData
from soundcheck.speech_analyzer import analyze_speech_clarity


def test_speech_clarity_analysis_reports_week_3_band_scores():
    audio = AudioData(
        path="speech.wav",
        sample_rate=16000,
        channels=1,
        samples=[[0.2 if index % 2 == 0 else -0.2] for index in range(16000)],
    )

    analysis = analyze_speech_clarity(audio)

    assert set(analysis.band_scores) == {
        "low_end_80_200hz",
        "muddy_200_400hz",
        "boxy_300_600hz",
        "clarity_2_5khz",
        "harsh_6_8khz",
    }
    assert len(analysis.top_issues) <= 3


def test_speech_clarity_analysis_prioritizes_harsh_band():
    audio = _sine_audio(7000.0)

    analysis = analyze_speech_clarity(audio)

    assert analysis.top_issues
    assert analysis.top_issues[0].code == "harsh_upper_mid"
    assert analysis.top_issues[0].band == "harsh_6_8khz"


def test_speech_clarity_analysis_prioritizes_muddy_band():
    audio = _sine_audio(250.0)

    analysis = analyze_speech_clarity(audio)

    codes = [issue.code for issue in analysis.top_issues]
    assert "muddy_low_mids" in codes


def _sine_audio(frequency, sample_rate=16000, duration=1.0):
    import math

    frames = []
    for index in range(int(sample_rate * duration)):
        value = 0.2 * math.sin(2.0 * math.pi * frequency * index / sample_rate)
        frames.append([value])
    return AudioData("speech.wav", sample_rate, 1, frames)

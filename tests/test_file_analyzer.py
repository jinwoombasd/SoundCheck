import json
import math
import struct
import wave

import pytest

import soundcheck.file_analyzer as file_analyzer
from soundcheck import loaders
from soundcheck.audio_data import AudioData
from soundcheck.cli import main
from soundcheck.file_analyzer import analyze_file


def test_analyze_normal_mono_wav(tmp_path):
    path = tmp_path / "speech.wav"
    _write_sine_wav(path, frequency=1000.0, amplitude=0.2, duration=1.0)

    report = analyze_file(str(path))

    assert report.metrics.duration_seconds == pytest.approx(1.0)
    assert report.metrics.sample_rate == 16000
    assert report.metrics.channels == 1
    assert report.metrics.rms_dbfs == pytest.approx(-17.0, abs=1.0)
    assert report.metrics.clipping_count == 0
    assert "speech_mid" in report.bands.relative_energy
    assert report.judgments


def test_report_output_contains_week_1_template_fields(tmp_path):
    path = tmp_path / "speech.wav"
    _write_sine_wav(path, frequency=1000.0, amplitude=0.2, duration=1.0)

    report_data = analyze_file(str(path)).to_dict()

    assert report_data["path"] == str(path)
    assert {
        "duration_seconds",
        "sample_rate",
        "channels",
        "peak_dbfs",
        "rms_dbfs",
        "clipping_count",
        "clipping_ratio",
        "left_right_balance_db",
        "noise_floor_dbfs",
    }.issubset(report_data["metrics"])
    assert {"relative_energy", "dominant_band"}.issubset(report_data["bands"])
    assert report_data["judgments"]
    assert {"code", "severity", "message", "detail"}.issubset(report_data["judgments"][0])


def test_clipped_wav_produces_warning(tmp_path):
    path = tmp_path / "clipped.wav"
    _write_sine_wav(path, frequency=800.0, amplitude=1.2, duration=1.0)

    report = analyze_file(str(path))

    codes = {judgment.code for judgment in report.judgments}
    assert "possible_clipping" in codes
    assert report.metrics.clipping_count > 0


def test_very_quiet_wav_produces_warning(tmp_path):
    path = tmp_path / "quiet.wav"
    _write_sine_wav(path, frequency=1000.0, amplitude=0.005, duration=1.0)

    report = analyze_file(str(path))

    codes = {judgment.code for judgment in report.judgments}
    assert "too_quiet" in codes


def test_stereo_balance_warning(tmp_path):
    path = tmp_path / "stereo.wav"
    _write_stereo_wav(path, left_amplitude=0.3, right_amplitude=0.03, duration=1.0)

    report = analyze_file(str(path))

    codes = {judgment.code for judgment in report.judgments}
    assert "balance_mismatch" in codes


def test_low_mid_heavy_wav_produces_muddy_warning(tmp_path):
    path = tmp_path / "muddy.wav"
    _write_sine_wav(path, frequency=250.0, amplitude=0.2, duration=1.0)

    report = analyze_file(str(path))

    codes = {judgment.code for judgment in report.judgments}
    assert report.bands.dominant_band == "low_mid"
    assert "muddy_low_mids" in codes


def test_upper_mid_heavy_wav_produces_harsh_warning(tmp_path):
    path = tmp_path / "harsh.wav"
    _write_sine_wav(path, frequency=3500.0, amplitude=0.2, duration=1.0)

    report = analyze_file(str(path))

    codes = {judgment.code for judgment in report.judgments}
    assert report.bands.relative_energy["upper_mid"] > 0.35
    assert "harsh_upper_mid" in codes


def test_too_short_file_fails_clearly(tmp_path):
    path = tmp_path / "short.wav"
    _write_sine_wav(path, frequency=1000.0, amplitude=0.2, duration=0.1)

    with pytest.raises(ValueError, match="too short"):
        analyze_file(str(path))


def test_zero_sample_rate_fails_clearly(monkeypatch):
    def load_stub(source):
        return AudioData(str(source), 0, 1, [[0.1], [0.1], [0.1]])

    monkeypatch.setattr(file_analyzer, "load_audio_file", load_stub)

    with pytest.raises(ValueError, match="sample rate"):
        analyze_file("invalid.wav")


def test_zero_channels_fails_clearly(monkeypatch):
    def load_stub(source):
        return AudioData(str(source), 16000, 0, [[0.1], [0.1], [0.1]])

    monkeypatch.setattr(file_analyzer, "load_audio_file", load_stub)

    with pytest.raises(ValueError, match="at least one channel"):
        analyze_file("invalid.wav")


def test_empty_audio_fails_clearly(monkeypatch):
    def load_stub(source):
        return AudioData(str(source), 16000, 1, [])

    monkeypatch.setattr(file_analyzer, "load_audio_file", load_stub)

    with pytest.raises(ValueError, match="contains no samples"):
        analyze_file("empty.wav")


def test_missing_file_fails_clearly(tmp_path):
    path = tmp_path / "missing.wav"

    with pytest.raises(FileNotFoundError, match="Audio file not found"):
        analyze_file(str(path))


def test_unsupported_file_type_fails_clearly(tmp_path):
    path = tmp_path / "speech.aiff"
    path.write_bytes(b"not-a-supported-audio-file")

    with pytest.raises(ValueError, match="Unsupported audio format"):
        analyze_file(str(path))


def test_corrupt_wav_fails_clearly(tmp_path):
    path = tmp_path / "corrupt.wav"
    path.write_bytes(b"not-a-valid-wav")

    with pytest.raises(ValueError, match="WAV loading failed"):
        analyze_file(str(path))


def test_mp3_dispatch_can_analyze_loaded_audio(tmp_path, monkeypatch):
    path = tmp_path / "speech.mp3"
    path.write_bytes(b"placeholder-mp3-data")

    def load_stub(source):
        return AudioData(str(source), 16000, 1, _sine_frames(1000.0, 0.2, 1.0))

    monkeypatch.setattr(loaders, "_load_mp3", load_stub)

    report = analyze_file(str(path))

    assert report.path == str(path)
    assert report.metrics.duration_seconds == pytest.approx(1.0)
    assert report.metrics.sample_rate == 16000


def test_cli_json_outputs_parseable_report(tmp_path, capsys):
    path = tmp_path / "speech.wav"
    _write_sine_wav(path, frequency=1000.0, amplitude=0.2, duration=1.0)

    exit_code = main([str(path), "--json"])

    captured = capsys.readouterr()
    report_data = json.loads(captured.out)
    assert exit_code == 0
    assert report_data["path"] == str(path)
    assert "metrics" in report_data
    assert "bands" in report_data
    assert "judgments" in report_data


def test_cli_accepts_mp3_sample_path(tmp_path, monkeypatch, capsys):
    path = tmp_path / "sample.mp3"
    path.write_bytes(b"placeholder-mp3-data")

    def load_stub(source):
        return AudioData(str(source), 16000, 1, _sine_frames(1000.0, 0.2, 1.0))

    monkeypatch.setattr(loaders, "_load_mp3", load_stub)

    exit_code = main([str(path), "--json"])

    captured = capsys.readouterr()
    report_data = json.loads(captured.out)
    assert exit_code == 0
    assert report_data["path"] == str(path)
    assert report_data["metrics"]["duration_seconds"] == pytest.approx(1.0)


def test_cli_week_1_json_outputs_template_fields(tmp_path, capsys):
    path = tmp_path / "speech.wav"
    _write_sine_wav(path, frequency=1000.0, amplitude=0.2, duration=1.0)

    exit_code = main([str(path), "--week-1-json"])

    captured = capsys.readouterr()
    report_data = json.loads(captured.out)
    assert exit_code == 0
    assert report_data["report_header"]["file_name_or_input_source"] == str(path)
    assert "overall_result" in report_data
    assert "top_issues" in report_data
    assert "engineer_details" in report_data


def test_cli_missing_file_returns_clean_error(tmp_path, capsys):
    path = tmp_path / "missing.wav"

    exit_code = main([str(path), "--json"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "Audio file not found" in captured.err
    assert "Traceback" not in captured.err


def _sine_frames(frequency, amplitude, duration, sample_rate=16000):
    frames = []
    frame_count = int(duration * sample_rate)
    for index in range(frame_count):
        value = amplitude * math.sin(2.0 * math.pi * frequency * index / sample_rate)
        frames.append([value])
    return frames


def _write_sine_wav(path, frequency, amplitude, duration, sample_rate=16000):
    _write_pcm16(path, _sine_frames(frequency, amplitude, duration, sample_rate), sample_rate)


def _write_stereo_wav(path, left_amplitude, right_amplitude, duration, sample_rate=16000):
    frames = []
    frame_count = int(duration * sample_rate)
    for index in range(frame_count):
        left = left_amplitude * math.sin(2.0 * math.pi * 1000.0 * index / sample_rate)
        right = right_amplitude * math.sin(2.0 * math.pi * 1000.0 * index / sample_rate)
        frames.append([left, right])
    _write_pcm16(path, frames, sample_rate)


def _write_pcm16(path, frames, sample_rate):
    channel_count = len(frames[0])
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(channel_count)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for frame in frames:
            for sample in frame:
                clipped = max(-1.0, min(1.0, sample))
                wav.writeframes(struct.pack("<h", int(clipped * 32767)))

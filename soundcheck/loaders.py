import struct
import wave
from pathlib import Path
from typing import List

from .audio_data import AudioData


SUPPORTED_EXTENSIONS = {".wav", ".mp3"}


def load_audio_file(path: str) -> AudioData:
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Audio file not found: {source}")

    extension = source.suffix.lower()
    if extension == ".wav":
        return _load_wav(source)
    if extension == ".mp3":
        return _load_mp3(source)

    supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
    raise ValueError(f"Unsupported audio format '{extension}'. Supported formats: {supported}.")


def _load_wav(path: Path) -> AudioData:
    try:
        with wave.open(str(path), "rb") as wav:
            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            sample_rate = wav.getframerate()
            frames = wav.getnframes()
            raw = wav.readframes(frames)
    except wave.Error as exc:
        raise ValueError(f"WAV loading failed: {exc}") from exc

    if sample_width not in (1, 2, 3, 4):
        raise ValueError(f"Unsupported WAV sample width: {sample_width} bytes.")

    decoded = _decode_pcm(raw, sample_width, channels)
    return AudioData(
        path=str(path),
        sample_rate=sample_rate,
        channels=channels,
        samples=decoded,
    )


def _load_mp3(path: Path) -> AudioData:
    try:
        return _load_with_soundfile(path)
    except ImportError:
        pass
    except Exception as exc:
        soundfile_error = exc
    else:
        soundfile_error = None

    try:
        return _load_with_pydub(path)
    except ImportError as exc:
        raise ImportError(
            "MP3 analysis requires the optional 'soundfile' or 'pydub' dependency."
        ) from exc
    except Exception as exc:
        if "soundfile_error" in locals() and soundfile_error is not None:
            raise ValueError(f"MP3 loading failed: {soundfile_error}; {exc}") from exc
        raise


def _load_with_soundfile(path: Path) -> AudioData:
    import soundfile as sf

    data, sample_rate = sf.read(str(path), always_2d=True, dtype="float32")
    samples = [[float(value) for value in frame] for frame in data]
    channels = len(samples[0]) if samples else 0
    return AudioData(str(path), int(sample_rate), channels, samples)


def _load_with_pydub(path: Path) -> AudioData:
    from pydub import AudioSegment

    segment = AudioSegment.from_file(str(path), format="mp3")
    channels = segment.channels
    sample_rate = segment.frame_rate
    sample_width = segment.sample_width
    raw_values = segment.get_array_of_samples()
    max_value = float(1 << (sample_width * 8 - 1))

    samples: List[List[float]] = []
    for index in range(0, len(raw_values), channels):
        frame = [
            _clamp(float(raw_values[index + channel]) / max_value)
            for channel in range(channels)
        ]
        samples.append(frame)

    return AudioData(str(path), sample_rate, channels, samples)


def _decode_pcm(raw: bytes, sample_width: int, channels: int) -> List[List[float]]:
    values = []
    if sample_width == 1:
        values = [(byte - 128) / 128.0 for byte in raw]
    elif sample_width == 2:
        count = len(raw) // 2
        values = [sample / 32768.0 for sample in struct.unpack(f"<{count}h", raw)]
    elif sample_width == 3:
        values = [_decode_24_bit(raw[index : index + 3]) for index in range(0, len(raw), 3)]
    elif sample_width == 4:
        count = len(raw) // 4
        values = [sample / 2147483648.0 for sample in struct.unpack(f"<{count}i", raw)]

    samples = []
    for index in range(0, len(values), channels):
        frame = values[index : index + channels]
        if len(frame) == channels:
            samples.append([_clamp(value) for value in frame])
    return samples


def _decode_24_bit(chunk: bytes) -> float:
    sign_extension = b"\xff" if chunk[2] & 0x80 else b"\x00"
    value = int.from_bytes(chunk + sign_extension, byteorder="little", signed=True)
    return value / 8388608.0


def _clamp(value: float) -> float:
    return max(-1.0, min(1.0, value))

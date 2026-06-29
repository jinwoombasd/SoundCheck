from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class AudioData:
    path: str
    sample_rate: int
    channels: int
    samples: List[List[float]]

    @property
    def frame_count(self) -> int:
        return len(self.samples)

    @property
    def duration_seconds(self) -> float:
        if self.sample_rate <= 0:
            return 0.0
        return self.frame_count / self.sample_rate

    def mono(self) -> List[float]:
        if self.channels == 1:
            return [frame[0] for frame in self.samples]
        return [sum(frame) / len(frame) for frame in self.samples]

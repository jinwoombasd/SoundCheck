from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from .judgments import Judgment
from .metrics import LevelMetrics
from .speech_bands import BandMetrics


@dataclass(frozen=True)
class AnalysisReport:
    path: str
    metrics: LevelMetrics
    bands: BandMetrics
    judgments: List[Judgment]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "metrics": asdict(self.metrics),
            "bands": asdict(self.bands),
            "judgments": [asdict(judgment) for judgment in self.judgments],
        }

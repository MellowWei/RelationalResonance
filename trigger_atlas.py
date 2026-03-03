from __future__ import annotations
from typing import Dict, Any, Tuple, List
import json
from .utils import clamp, safe_list

def load_trigger_atlas(path: str) -> Dict[str, float]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {str(k): float(v) for k, v in data.items()}

def save_trigger_atlas(path: str, atlas: Dict[str, float]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(atlas, f, ensure_ascii=False, indent=2)

def trigger_score_and_update(event: Dict[str, Any], atlas: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
    motifs = safe_list(event, "motifs")
    markers = set(x.lower() for x in safe_list(event, "language_markers"))
    delta = 0.02 if ("vibration" in markers or "deeper" in markers) else 0.005

    weights: List[float] = []
    new_atlas = dict(atlas)

    for m in motifs:
        old = float(new_atlas.get(m, 0.50))
        weights.append(old)
        new_atlas[m] = clamp(old + delta)

    score = clamp(sum(weights) / len(weights)) if weights else 0.0
    return score, new_atlas

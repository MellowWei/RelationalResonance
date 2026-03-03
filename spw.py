from __future__ import annotations
from typing import Dict, Any
from .utils import clamp, safe_get, safe_list

MYTH_WORDS = {"god", "fate", "destiny", "heaven", "hell", "soul"}

def spw_score(event: Dict[str, Any]) -> float:
    """Sacred Projection Window (SPW).
    SPW = clamp(0.35*awe + 0.25*safety + 0.20*depth + 0.10*neptune_like + 0.10*myth_language)
    """
    awe = safe_get(event, ["affect", "awe"])
    safety = safe_get(event, ["affect", "safety"])
    depth = safe_get(event, ["affect", "depth"])
    neptune_like = safe_get(event, ["context", "neptune_like"], default=0.7)
    markers = set(x.lower() for x in safe_list(event, "language_markers"))
    myth_language = 1.0 if len(MYTH_WORDS.intersection(markers)) > 0 else 0.0
    return clamp(0.35*awe + 0.25*safety + 0.20*depth + 0.10*neptune_like + 0.10*myth_language)

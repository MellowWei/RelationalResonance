from __future__ import annotations
from typing import Dict, Any
from .utils import clamp, safe_get, safe_list

MYTH_WORDS = {"god", "fate", "destiny", "heaven", "hell", "soul"}

def mdi_score(event: Dict[str, Any]) -> float:
    """Meaning Density Index: 0.4*awe + 0.3*depth + 0.2*myth_language + 0.1*novelty"""
    awe = safe_get(event, ["affect", "awe"])
    depth = safe_get(event, ["affect", "depth"])
    novelty = safe_get(event, ["context", "novelty"])
    markers = set(x.lower() for x in safe_list(event, "language_markers"))
    myth_language = 1.0 if len(MYTH_WORDS.intersection(markers)) > 0 else 0.0
    return clamp(0.4*awe + 0.3*depth + 0.2*myth_language + 0.1*novelty)

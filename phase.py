from __future__ import annotations
from typing import Dict, Any
from .utils import safe_get, safe_list

MYTH_WORDS = {"god", "fate", "destiny", "heaven", "hell", "soul"}

def phase(event: Dict[str, Any]) -> str:
    """Phase Machine: P0, P1, P2, P3"""
    depth = safe_get(event, ["affect", "depth"])
    safety = safe_get(event, ["affect", "safety"])
    awe = safe_get(event, ["affect", "awe"])
    gap_days = safe_get(event, ["context", "gap_days"])
    markers = set(x.lower() for x in safe_list(event, "language_markers"))
    myth_language = 1.0 if len(MYTH_WORDS.intersection(markers)) > 0 else 0.0

    if myth_language == 1.0 and depth > 0.6:
        return "P2"
    if safety > 0.6 and awe > 0.5:
        return "P1"
    if gap_days > 7:
        return "P3"
    return "P0"

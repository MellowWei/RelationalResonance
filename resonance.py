from __future__ import annotations
from typing import Dict, Any
from .utils import clamp, safe_get

def resonance_score(event: Dict[str, Any]) -> float:
    """(awe + safety + depth) / 3"""
    awe = safe_get(event, ["affect", "awe"])
    safety = safe_get(event, ["affect", "safety"])
    depth = safe_get(event, ["affect", "depth"])
    return clamp((awe + safety + depth) / 3.0)

from __future__ import annotations
from typing import Dict, Any
from .utils import clamp, safe_get

def witness_score(event: Dict[str, Any]) -> float:
    """Witness = clamp(0.45*depth + 0.25*awe + 0.20*non_control + 0.10*return_pattern)"""
    depth = safe_get(event, ["affect", "depth"])
    awe = safe_get(event, ["affect", "awe"])
    non_control = safe_get(event, ["context", "non_control"])
    return_pattern = safe_get(event, ["context", "return_pattern"])
    return clamp(0.45*depth + 0.25*awe + 0.20*non_control + 0.10*return_pattern)

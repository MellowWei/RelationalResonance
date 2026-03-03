from __future__ import annotations
from typing import Dict, Any
from .utils import clamp, safe_get
from .mdi import mdi_score

def tc_score(event: Dict[str, Any]) -> float:
    """Temporal Compression: TC = clamp(0.5*MDI + 0.3*safety + 0.2*identity_shift)"""
    mdi = mdi_score(event)
    safety = safe_get(event, ["affect", "safety"])
    identity_shift = safe_get(event, ["context", "identity_shift"])
    return clamp(0.5*mdi + 0.3*safety + 0.2*identity_shift)

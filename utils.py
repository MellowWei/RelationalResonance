from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import math

def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))

def sigmoid(x: float) -> float:
    # numerically stable sigmoid
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    else:
        z = math.exp(x)
        return z / (1.0 + z)

def safe_get(d: Dict[str, Any], path: List[str], default: float = 0.0) -> float:
    cur: Any = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    if isinstance(cur, (int, float)):
        return float(cur)
    return default

def safe_list(d: Dict[str, Any], key: str) -> List[str]:
    v = d.get(key, [])
    if isinstance(v, list):
        return [str(x) for x in v]
    return []

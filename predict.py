from __future__ import annotations
import json
from pathlib import Path
import math
import statistics

from models.utils import sigmoid

ROOT = Path(__file__).resolve().parents[1]
SCORES_JSON = ROOT / "analysis" / "_scores.json"
EVENTS_PATH = ROOT / "data" / "events.jsonl"

def main() -> None:
    if not SCORES_JSON.exists():
        raise SystemExit("Run: python analysis/run_all.py first (it generates analysis/_scores.json).")

    scores = json.loads(SCORES_JSON.read_text(encoding="utf-8"))

    # Recent windows
    recent = scores[-3:] if len(scores) >= 3 else scores
    if not recent:
        raise SystemExit("No events found.")

    mdi_recent = sum(r["scores"]["mdi"] for r in recent) / len(recent)
    resonance_recent = sum(r["scores"]["resonance"] for r in recent) / len(recent)
    awe_recent = sum(_load_affect(r["event_id"]).get("awe",0.0) for r in recent) / len(recent)
    depth_recent = sum(_load_affect(r["event_id"]).get("depth",0.0) for r in recent) / len(recent)
    myth_recent = sum(_load_myth(r["event_id"]) for r in recent) / len(recent)
    cannabis_recent = sum(_load_cannabis(r["event_id"]) for r in recent) / len(recent)

    gap_days = _last_gap_days()

    # Approx stability proxies
    phases = [r.get("phase","P0") for r in scores]
    phase_num = [{"P0":0,"P1":1,"P2":2,"P3":3}.get(p,0) for p in phases]
    phase_std = statistics.pstdev(phase_num) if len(phase_num) > 1 else 0.0
    consistency = max(0.0, 1.0 - min(1.0, phase_std / 1.5))  # normalize roughly

    vol_list = []
    for r in recent:
        a = _load_affect(r["event_id"]).get("awe",0.0)
        s = _load_affect(r["event_id"]).get("safety",0.0)
        d = _load_affect(r["event_id"]).get("depth",0.0)
        vol_list.extend([a,s,d])
    volatility = statistics.pstdev(vol_list) if len(vol_list) > 1 else 0.0

    sacred_count = sum(1 for r in scores if _load_myth(r["event_id"]) > 0)

    # Probabilities (as you specified)
    P2_next_7d  = sigmoid(-0.6 + 1.2*mdi_recent + 0.8*resonance_recent + 0.5*sacred_count - 0.7*gap_days)
    SPW_next_7d = sigmoid(-0.7 + 1.0*awe_recent + 0.6*depth_recent + 0.4*myth_recent + 0.3*cannabis_recent)
    Stability_30d = sigmoid(-0.3 + 0.9*_safety_avg(scores) + 0.6*consistency - 0.8*volatility)

    drivers = sorted([
        ("mdi_recent", mdi_recent),
        ("resonance_recent", resonance_recent),
        ("sacred_count", float(sacred_count)),
        ("gap_days", gap_days),
        ("awe_recent", awe_recent),
        ("depth_recent", depth_recent),
        ("myth_recent", myth_recent),
        ("cannabis_recent", cannabis_recent),
        ("consistency", consistency),
        ("volatility", volatility),
    ], key=lambda x: abs(x[1]), reverse=True)[:3]

    out = {
        "P2_next_7d": float(P2_next_7d),
        "SPW_next_7d": float(SPW_next_7d),
        "Stability_30d": float(Stability_30d),
        "drivers": {k: float(v) for k,v in drivers},
        "note": "Reality-safe: projection/神性语言是体验窗口，不等于客观事实判断。"
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

def _load_events():
    events = []
    with open(EVENTS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))
    return events

def _event_by_id(eid: str):
    for e in _load_events():
        if e.get("event_id") == eid:
            return e
    return {}

def _load_affect(eid: str):
    e = _event_by_id(eid)
    return e.get("affect", {}) if isinstance(e.get("affect", {}), dict) else {}

def _load_myth(eid: str) -> float:
    e = _event_by_id(eid)
    markers = [str(x).lower() for x in (e.get("language_markers", []) or [])]
    myth = any(m in markers for m in ["god","fate","destiny","heaven","hell","soul"])
    return 1.0 if myth else 0.0

def _load_cannabis(eid: str) -> float:
    e = _event_by_id(eid)
    ctx = e.get("context", {}) if isinstance(e.get("context", {}), dict) else {}
    return 1.0 if str(ctx.get("substance","")).lower() == "cannabis" else 0.0

def _last_gap_days() -> float:
    evs = _load_events()
    if not evs:
        return 0.0
    ctx = evs[-1].get("context", {}) if isinstance(evs[-1].get("context", {}), dict) else {}
    return float(ctx.get("gap_days", 0.0) or 0.0)

def _safety_avg(scores_rows) -> float:
    evs = _load_events()
    safeties = []
    for e in evs:
        aff = e.get("affect", {}) if isinstance(e.get("affect", {}), dict) else {}
        s = aff.get("safety", None)
        if isinstance(s, (int,float)):
            safeties.append(float(s))
    return sum(safeties)/len(safeties) if safeties else 0.0

if __name__ == "__main__":
    main()

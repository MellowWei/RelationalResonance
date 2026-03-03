from __future__ import annotations
import json
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
SCORES_JSON = ROOT / "analysis" / "_scores.json"
OUTDIR = ROOT / "analysis" / "_out"
OUTDIR.mkdir(exist_ok=True)

def _parse_time(s: str) -> datetime:
    # ISO-8601 with offset is okay; matplotlib can accept datetime
    return datetime.fromisoformat(s)

def main() -> None:
    if not SCORES_JSON.exists():
        raise SystemExit("Run: python analysis/run_all.py first (it generates analysis/_scores.json).")

    data = json.loads(SCORES_JSON.read_text(encoding="utf-8"))

    times = []
    resonance = []
    spw = []
    mdi = []
    witness = []
    tc = []
    trigger = []
    phases = []

    for row in data:
        t = row.get("time")
        times.append(_parse_time(t) if t else None)
        s = row["scores"]
        resonance.append(s["resonance"])
        spw.append(s["spw"])
        mdi.append(s["mdi"])
        witness.append(s["witness"])
        tc.append(s["tc"])
        trigger.append(s["trigger"])
        phases.append(row.get("phase", "P0"))

    # 1) Timeline plot
    plt.figure()
    plt.plot(times, resonance, label="resonance")
    plt.plot(times, spw, label="spw")
    plt.plot(times, mdi, label="mdi")
    plt.plot(times, witness, label="witness")
    plt.plot(times, tc, label="tc")
    plt.plot(times, trigger, label="trigger")
    plt.legend()
    plt.xlabel("time")
    plt.ylabel("score")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(OUTDIR / "timeline_scores.png", dpi=200)
    plt.close()

    # 2) Phase timeline (categorical)
    plt.figure()
    plt.plot(times, [ {"P0":0,"P1":1,"P2":2,"P3":3}.get(p,0) for p in phases ])
    plt.yticks([0,1,2,3], ["P0","P1","P2","P3"])
    plt.xlabel("time")
    plt.ylabel("phase")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(OUTDIR / "phase_timeline.png", dpi=200)
    plt.close()

    # 3) Heatmap-like matrix: events x scores
    import numpy as np
    M = np.array(list(zip(resonance, spw, mdi, witness, tc, trigger)))
    plt.figure()
    plt.imshow(M, aspect="auto")
    plt.yticks(range(len(data)), [row.get("event_id","") for row in data])
    plt.xticks(range(6), ["resonance","spw","mdi","witness","tc","trigger"], rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(OUTDIR / "heatmap_events_scores.png", dpi=200)
    plt.close()

    print(str(OUTDIR))

if __name__ == "__main__":
    main()

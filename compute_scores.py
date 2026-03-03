from __future__ import annotations
import json
from pathlib import Path

from models.resonance import resonance_score
from models.mdi import mdi_score
from models.spw import spw_score
from models.phase import phase
from models.witness import witness_score
from models.temporal_compression import tc_score
from models.trigger_atlas import load_trigger_atlas, trigger_score_and_update, save_trigger_atlas

ROOT = Path(__file__).resolve().parents[1]
EVENTS_PATH = ROOT / "data" / "events.jsonl"
ATLAS_PATH = ROOT / "data" / "trigger_atlas.json"

def main() -> None:
    atlas = load_trigger_atlas(str(ATLAS_PATH))
    out = []

    with open(EVENTS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            event = json.loads(line)
            trig, atlas = trigger_score_and_update(event, atlas)

            row = {
                "event_id": event.get("event_id"),
                "time": event.get("time"),
                "phase": phase(event),
                "scores": {
                    "resonance": resonance_score(event),
                    "mdi": mdi_score(event),
                    "spw": spw_score(event),
                    "witness": witness_score(event),
                    "tc": tc_score(event),
                    "trigger": trig,
                },
            }
            out.append(row)

    save_trigger_atlas(str(ATLAS_PATH), atlas)
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

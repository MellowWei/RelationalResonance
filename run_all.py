from __future__ import annotations
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORES_JSON = ROOT / "analysis" / "_scores.json"

def main() -> None:
    # Compute scores and persist
    p = subprocess.run(["python", str(ROOT/"analysis"/"compute_scores.py")], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(p.stderr)
    data = json.loads(p.stdout)
    SCORES_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # Make plots
    p2 = subprocess.run(["python", str(ROOT/"analysis"/"plots.py")], capture_output=True, text=True)
    if p2.returncode != 0:
        raise SystemExit(p2.stderr)

    # Predict
    p3 = subprocess.run(["python", str(ROOT/"analysis"/"predict.py")], capture_output=True, text=True)
    if p3.returncode != 0:
        raise SystemExit(p3.stderr)
    (ROOT/"analysis"/"_prediction.json").write_text(p3.stdout, encoding="utf-8")

    print("OK")
    print("Scores:", str(SCORES_JSON))
    print("Plots:", str(ROOT/"analysis"/"_out"))
    print("Prediction:", str(ROOT/"analysis"/"_prediction.json"))

if __name__ == "__main__":
    main()

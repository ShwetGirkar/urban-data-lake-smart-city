import json
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def save_json(output_dir, filename, data):
    ensure_dir(output_dir)
    path = Path(output_dir) / filename
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")


def append_csv(output_dir, filename, row):
    ensure_dir(output_dir)
    path = Path(output_dir) / filename
    df = pd.DataFrame([row])
    if path.exists():
        df.to_csv(path, mode="a", header=False, index=False)
    else:
        df.to_csv(path, mode="w", header=True, index=False)

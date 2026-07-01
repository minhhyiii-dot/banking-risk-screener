from __future__ import annotations

import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR / "src"))

from banking_risk_pipeline.rmp_specs import extract_rmp_specs
from banking_risk_pipeline.train_new1 import run_new1


if __name__ == "__main__":
    extract_rmp_specs()
    run_new1()


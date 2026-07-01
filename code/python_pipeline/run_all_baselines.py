from __future__ import annotations

import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR / "src"))

from banking_risk_pipeline.rmp_specs import extract_rmp_specs
from banking_risk_pipeline.train_new1 import run_new1
from banking_risk_pipeline.train_new2 import run_new2
from banking_risk_pipeline.train_old import run_old_models


def main() -> None:
    extract_rmp_specs()
    run_old_models()
    run_new1()
    run_new2("validation")
    run_new2("test")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(THIS_DIR / "src"))

from banking_risk_pipeline.rmp_specs import extract_rmp_specs
from banking_risk_pipeline.train_new2 import run_new2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=["validation", "test", "both"], default="both")
    args = parser.parse_args()

    extract_rmp_specs()
    if args.kind in {"validation", "both"}:
        run_new2("validation")
    if args.kind in {"test", "both"}:
        run_new2("test")


if __name__ == "__main__":
    main()


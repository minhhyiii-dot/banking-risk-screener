from __future__ import annotations

from pathlib import Path


def find_project_root(start: Path | None = None) -> Path:
    """Find the project root from any file inside the repo-like folder."""
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "data").exists() and (candidate / "code" / "Models").exists():
            return candidate
    raise FileNotFoundError("Could not find project root containing data/ and code/Models/.")


PROJECT_ROOT = find_project_root()
DATA_DIR = PROJECT_ROOT / "data"
OLD_MASTER_PATH = DATA_DIR / "old master dataset" / "master_ml_training.csv"
COMMON_MASTER_PATH = DATA_DIR / "new master dataset" / "common_master.csv"
PQ_TEST_PATH = DATA_DIR / "new master dataset" / "pq087_prequential.csv"
PQ_VALIDATION_PATH = DATA_DIR / "new master dataset" / "pq087_validation_prequential.csv"
MODELS_DIR = PROJECT_ROOT / "code" / "Models"
SPEC_DIR = PROJECT_ROOT / "code" / "python_migration_specs"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "python_baseline"


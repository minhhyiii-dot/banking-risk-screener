from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from .paths import MODELS_DIR, SPEC_DIR


RMP_SEPARATOR_PATTERN = re.compile(r"\u241e|\||;|\n|\r|\t")


def normalize_column_name(name: str) -> str:
    """Normalize column names exported from RapidMiner XML."""
    return name.replace("ï»¿", "").replace("\ufeff", "").strip()


def parse_select_subset(raw: str | None) -> list[str]:
    if not raw:
        return []
    return [normalize_column_name(x) for x in RMP_SEPARATOR_PATTERN.split(raw) if x.strip()]


def extract_rmp_specs(output_dir: Path = SPEC_DIR) -> dict[str, list[dict[str, Any]]]:
    """Extract useful RapidMiner operator specs into JSON for reproducibility."""
    output_dir.mkdir(parents=True, exist_ok=True)
    all_specs: dict[str, list[dict[str, Any]]] = {}

    for rmp_path in sorted(MODELS_DIR.rglob("*.rmp")):
        tree = ET.parse(rmp_path)
        operators: list[dict[str, Any]] = []

        for index, operator in enumerate(tree.iter("operator")):
            name = operator.attrib.get("name")
            klass = operator.attrib.get("class")
            params = {
                p.attrib.get("key"): p.attrib.get("value")
                for p in operator.findall("parameter")
                if p.attrib.get("key") is not None
            }
            lists: dict[str, list[dict[str, str | None]]] = {}
            for list_node in operator.findall("list"):
                list_key = list_node.attrib.get("key") or "list"
                lists[list_key] = [
                    {"key": child.attrib.get("key"), "value": child.attrib.get("value")}
                    for child in list_node.findall("parameter")
                ]

            text = f"{name} {klass}".lower()
            keep = any(
                term in text
                for term in [
                    "select_attributes",
                    "set_role",
                    "gradient_boosted",
                    "random_forest",
                    "decision_tree",
                    "split_data",
                    "filter_examples",
                    "generate_attributes",
                    "performance",
                    "multiply",
                    "join",
                    "apply_model",
                    "cartesian",
                    "aggregate",
                    "retrieve",
                    "read_csv",
                    "write_csv",
                ]
            )
            if not keep:
                continue

            normalized = dict(params)
            subset = parse_select_subset(normalized.get("select_subset"))
            if subset:
                normalized["select_subset_count"] = len(subset)
                normalized["select_subset_parsed"] = subset

            operators.append(
                {
                    "index": index,
                    "name": name,
                    "class": klass,
                    "parameters": normalized,
                    "lists": lists,
                }
            )

        relative = str(rmp_path.relative_to(MODELS_DIR.parent.parent))
        all_specs[relative] = operators
        safe_name = relative.replace("\\", "__").replace("/", "__").replace(":", "").replace(".rmp", ".json")
        (output_dir / safe_name).write_text(
            json.dumps({"source_rmp": relative, "operators": operators}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    (output_dir / "ALL_RMP_MODEL_SPECS.json").write_text(
        json.dumps(all_specs, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return all_specs


def load_rmp_specs() -> dict[str, list[dict[str, Any]]]:
    spec_path = SPEC_DIR / "ALL_RMP_MODEL_SPECS.json"
    if not spec_path.exists():
        return extract_rmp_specs()
    return json.loads(spec_path.read_text(encoding="utf-8"))


def find_operator(specs: list[dict[str, Any]], name: str) -> dict[str, Any]:
    for operator in specs:
        if operator.get("name") == name:
            return operator
    raise KeyError(f"Operator not found: {name}")


def operator_subset(specs: list[dict[str, Any]], name: str) -> list[str]:
    operator = find_operator(specs, name)
    return operator["parameters"].get("select_subset_parsed", [])


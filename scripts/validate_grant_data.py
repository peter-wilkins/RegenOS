#!/usr/bin/env python3
"""Validate the lightweight RegenOS grant YAML records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - depends on local environment
    raise SystemExit("Missing dependency: install PyYAML to validate grant YAML files.") from exc


ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_RULE_KINDS = {"site_fact", "human_confirmation", "human_or_gis_confirmation"}
SUPPORTED_OPERATORS = {
    "between",
    "less_than",
    "less_than_or_equal",
    "greater_than",
    "greater_than_or_equal",
    "equals",
}
EVIDENCE_KEYS = {"id", "phase", "evidence_type", "description"}
EXAMPLE_KEYS = {
    "id",
    "title",
    "location",
    "source_urls",
    "media_types",
    "related_intervention_templates",
    "likely_relevant_options",
    "learnings",
}


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not contain a YAML object")
    return data


def require_string(record: dict[str, Any], field: str, where: str, errors: list[str]) -> None:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{where}: missing string field `{field}`")


def validate_programme(path: Path, programme: dict[str, Any], errors: list[str]) -> None:
    require_string(programme, "id", str(path), errors)
    option_ids: set[str] = set()
    for option in programme.get("options", []):
        where = f"{path}:{option.get('id', '<missing option id>')}"
        require_string(option, "id", where, errors)
        if option.get("id") in option_ids:
            errors.append(f"{where}: duplicate option id")
        option_ids.add(option.get("id"))
        if not option.get("intervention_templates"):
            errors.append(f"{where}: missing intervention_templates")
        payment = option.get("payment", {})
        if not isinstance(payment, dict) or "type" not in payment or "unit" not in payment:
            errors.append(f"{where}: payment must include type and unit")

        rule_ids: set[str] = set()
        for rule in option.get("eligibility_rules", []):
            rule_where = f"{where}:rule:{rule.get('id', '<missing rule id>')}"
            require_string(rule, "id", rule_where, errors)
            if rule.get("id") in rule_ids:
                errors.append(f"{rule_where}: duplicate rule id")
            rule_ids.add(rule.get("id"))
            if rule.get("kind") not in SUPPORTED_RULE_KINDS:
                errors.append(f"{rule_where}: unsupported kind `{rule.get('kind')}`")
            if rule.get("kind") == "site_fact" and rule.get("operator") not in SUPPORTED_OPERATORS:
                errors.append(f"{rule_where}: unsupported operator `{rule.get('operator')}`")

        evidence_ids: set[str] = set()
        for evidence in option.get("evidence_requirements", []):
            evidence_where = f"{where}:evidence:{evidence.get('id', '<missing evidence id>')}"
            extra_keys = set(evidence) - EVIDENCE_KEYS
            if extra_keys:
                errors.append(f"{evidence_where}: unexpected keys {sorted(extra_keys)}")
            require_string(evidence, "id", evidence_where, errors)
            require_string(evidence, "phase", evidence_where, errors)
            require_string(evidence, "evidence_type", evidence_where, errors)
            require_string(evidence, "description", evidence_where, errors)
            if evidence.get("id") in evidence_ids:
                errors.append(f"{evidence_where}: duplicate evidence id")
            evidence_ids.add(evidence.get("id"))


def validate_examples(path: Path, record: dict[str, Any], errors: list[str]) -> None:
    example_ids: set[str] = set()
    for example in record.get("examples", []):
        where = f"{path}:example:{example.get('id', '<missing example id>')}"
        extra_keys = set(example) - EXAMPLE_KEYS
        if extra_keys:
            errors.append(f"{where}: unexpected keys {sorted(extra_keys)}")
        require_string(example, "id", where, errors)
        require_string(example, "title", where, errors)
        if example.get("id") in example_ids:
            errors.append(f"{where}: duplicate example id")
        example_ids.add(example.get("id"))
        if not example.get("source_urls"):
            errors.append(f"{where}: missing source_urls")
        if not example.get("learnings"):
            errors.append(f"{where}: missing learnings")


def main() -> None:
    errors: list[str] = []
    for path in sorted((ROOT / "data/grants").glob("**/*.yaml")):
        data = load_yaml(path)
        if "options" in data:
            validate_programme(path, data, errors)
        if "examples" in data:
            validate_examples(path, data, errors)

    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print("grant data ok")


if __name__ == "__main__":
    main()

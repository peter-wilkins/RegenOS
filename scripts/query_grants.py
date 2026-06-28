#!/usr/bin/env python3
"""Query draft grant records by intervention and known site facts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - depends on local environment
    raise SystemExit("Missing dependency: install PyYAML to query grant YAML files.") from exc


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not contain a YAML object")
    return data


def dot_get(record: dict[str, Any], dotted_key: str) -> Any:
    current: Any = record
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def evaluate_rule(rule: dict[str, Any], facts: dict[str, Any]) -> dict[str, str]:
    kind = rule.get("kind")
    if kind not in {"site_fact", "human_confirmation", "human_or_gis_confirmation"}:
        return {"state": "unknown", "reason": "unsupported rule kind"}

    if kind != "site_fact":
        return {"state": "needs_human", "reason": rule.get("description", "needs human confirmation")}

    fact_name = rule.get("fact")
    value = dot_get(facts, str(fact_name))
    if value is None:
        return {"state": "unknown", "reason": f"missing fact: {fact_name}"}

    operator = rule.get("operator")
    expected = rule.get("value")
    passed = False
    if operator == "between" and isinstance(expected, dict):
        passed = expected.get("min") <= value <= expected.get("max")
    elif operator == "less_than":
        passed = value < expected
    elif operator == "less_than_or_equal":
        passed = value <= expected
    elif operator == "greater_than":
        passed = value > expected
    elif operator == "greater_than_or_equal":
        passed = value >= expected
    elif operator == "equals":
        passed = value == expected
    else:
        return {"state": "unknown", "reason": f"unsupported operator: {operator}"}

    return {
        "state": "pass" if passed else "fail",
        "reason": f"{fact_name}={value} {operator} {expected}",
    }


def load_programmes() -> list[dict[str, Any]]:
    return [load_yaml(path) for path in sorted((ROOT / "data/grants").glob("**/*.yaml"))]


def candidate_options(intervention: str, facts: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for programme in load_programmes():
        for option in programme.get("options", []):
            if intervention not in option.get("intervention_templates", []):
                continue
            rule_results = [
                {"id": rule.get("id"), **evaluate_rule(rule, facts)}
                for rule in option.get("eligibility_rules", [])
            ]
            candidates.append(
                {
                    "programme_id": programme.get("id"),
                    "programme_name": programme.get("name"),
                    "option": option,
                    "rule_results": rule_results,
                }
            )
    return candidates


def render_markdown(candidates: list[dict[str, Any]]) -> str:
    if not candidates:
        return "No candidate grant options found.\n"

    lines = ["# Candidate grant options", ""]
    for candidate in candidates:
        option = candidate["option"]
        payment = option.get("payment", {})
        amount = payment.get("amount")
        if payment.get("type") == "percent_actual_cost" and amount is not None:
            payment_text = f"{amount}% of actual costs"
        else:
            payment_text = (
                f"{amount} {payment.get('currency', '')} per {payment.get('unit', '')}".strip()
                if amount is not None
                else f"{payment.get('type', 'unknown')} payment"
            )
        lines.extend(
            [
                f"## {option.get('name')}",
                "",
                f"- Programme: {candidate.get('programme_name')} ({candidate.get('programme_id')})",
                f"- Status: {option.get('status')} / confidence: {option.get('confidence')}",
                f"- Payment: {payment_text}",
                "- Source: " + ", ".join(option.get("source_urls", [])),
                "",
                "### Eligibility",
            ]
        )
        for result in candidate["rule_results"]:
            lines.append(f"- `{result['state']}` {result.get('id')}: {result.get('reason')}")
        lines.extend(["", "### Evidence prompts"])
        for evidence in option.get("evidence_requirements", []):
            lines.append(
                f"- `{evidence.get('phase')}` {evidence.get('evidence_type')}: {evidence.get('description')}"
            )
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("intervention", help="Intervention template id, for example pond or check-dam")
    parser.add_argument("--facts", default="{}", help="Known site facts as JSON")
    parser.add_argument("--json", action="store_true", help="Print raw JSON")
    args = parser.parse_args()

    facts = json.loads(args.facts)
    candidates = candidate_options(args.intervention, facts)
    if args.json:
        print(json.dumps(candidates, indent=2))
    else:
        print(render_markdown(candidates))


if __name__ == "__main__":
    main()

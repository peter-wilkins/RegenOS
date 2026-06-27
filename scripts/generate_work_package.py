#!/usr/bin/env python3
"""Generate a draft RegenOS -> JobDone work package from grant records."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - depends on local environment
    raise SystemExit("Missing dependency: install PyYAML to generate work packages.") from exc


ROOT = Path(__file__).resolve().parents[1]


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not contain a YAML object")
    return data


def load_intervention(template_id: str) -> dict[str, Any]:
    path = ROOT / "data/interventions" / f"{template_id}.yaml"
    if not path.exists():
        raise SystemExit(f"Unknown intervention template: {template_id}")
    return load_yaml(path)


def find_option(option_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    for path in sorted((ROOT / "data/grants").glob("**/*.yaml")):
        programme = load_yaml(path)
        for option in programme.get("options", []):
            if option.get("id") == option_id:
                return programme, option
    raise SystemExit(f"Unknown funding option: {option_id}")


def task_title(evidence: dict[str, Any], intervention: dict[str, Any]) -> str:
    phase = str(evidence.get("phase", "evidence")).replace("_", " ")
    evidence_type = str(evidence.get("evidence_type", "evidence")).replace("_", " ")
    return f"{phase.title()}: collect {evidence_type} for {intervention['name']}"


def build_work_package(
    project_id: str,
    intervention_id: str,
    template_id: str,
    option_id: str,
    title: str | None,
) -> dict[str, Any]:
    programme, option = find_option(option_id)
    intervention = load_intervention(template_id)
    if template_id not in option.get("intervention_templates", []):
        raise SystemExit(f"Funding option {option_id} is not linked to template {template_id}")

    work_package_id = slug(title or f"{project_id}-{intervention_id}-{option['name']}")
    evidence_types = []
    for evidence in option.get("evidence_requirements", []):
        evidence_type = evidence.get("evidence_type")
        if evidence_type not in evidence_types:
            evidence_types.append(evidence_type)

    jobs: list[dict[str, Any]] = []
    for index, evidence in enumerate(option.get("evidence_requirements", []), start=1):
        jobs.append(
            {
                "id": f"task-{index:03d}",
                "intervention_id": intervention_id,
                "title": task_title(evidence, intervention),
                "description": evidence.get("description"),
                "phase": evidence.get("phase"),
                "assignee": None,
                "location": None,
                "evidence_required": [
                    {
                        "type": evidence.get("evidence_type"),
                        "source_requirement_id": evidence.get("id"),
                        "notes": evidence.get("description"),
                    }
                ],
                "completion_criteria": [
                    "Evidence captured or explicitly marked not applicable.",
                    "Location/time metadata present where relevant.",
                ],
            }
        )

    for index, maintenance in enumerate(intervention.get("maintenance", []), start=1):
        jobs.append(
            {
                "id": f"maintenance-{index:03d}",
                "intervention_id": intervention_id,
                "title": f"Maintenance: {maintenance}",
                "description": f"Follow-up maintenance for {intervention['name']}: {maintenance}.",
                "phase": "maintenance",
                "assignee": None,
                "location": None,
                "evidence_required": [{"type": "inspection_note"}],
                "completion_criteria": ["Inspection note recorded."],
            }
        )

    return {
        "work_package": {
            "id": work_package_id,
            "project_id": project_id,
            "title": title or f"{intervention['name']} funded by {option['name']}",
            "status": "draft",
            "caution": "Draft planning aid only. Grant eligibility and approval must be checked with official guidance or an adviser.",
        },
        "funding": {
            "programme_id": programme.get("id"),
            "programme_name": programme.get("name"),
            "funding_option_id": option.get("id"),
            "funding_option_name": option.get("name"),
            "source_urls": option.get("source_urls", []),
            "confidence": option.get("confidence"),
        },
        "interventions": [
            {
                "id": intervention_id,
                "template": template_id,
                "title": intervention.get("name"),
                "description": intervention.get("description"),
                "location": None,
                "evidence_required": evidence_types,
            }
        ],
        "eligibility_questions": [
            {
                "id": rule.get("id"),
                "kind": rule.get("kind"),
                "description": rule.get("description"),
                "fact": rule.get("fact"),
            }
            for rule in option.get("eligibility_rules", [])
        ],
        "jobs": jobs,
        "export": {
            "target": "JobDone",
            "format": "yaml",
            "version": "draft-0.2",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--intervention-id", required=True)
    parser.add_argument("--template", required=True, help="Intervention template id")
    parser.add_argument("--funding-option", required=True, help="Funding option id")
    parser.add_argument("--title")
    parser.add_argument("--output", help="Write YAML to this path instead of stdout")
    args = parser.parse_args()

    package = build_work_package(
        project_id=args.project_id,
        intervention_id=args.intervention_id,
        template_id=args.template,
        option_id=args.funding_option,
        title=args.title,
    )
    output = yaml.safe_dump(package, sort_keys=False, allow_unicode=True)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()

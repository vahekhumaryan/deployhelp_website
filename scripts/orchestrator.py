#!/usr/bin/env python3
"""Multi-agent orchestration helper for DEPLOYHELP LLC.

This script loads the agent roster, persona definitions, and backlog items to
assist Mission Control with coordination tasks such as:

- Listing agents and their responsibilities
- Generating standup prompts and reminders
- Summarising backlog tickets and ownership
- Producing starter conversation agendas for new initiatives

Usage examples:

```
python scripts/orchestrator.py list-agents
python scripts/orchestrator.py show-agent mission_control
python scripts/orchestrator.py standup --date 2025-11-01
python scripts/orchestrator.py ticket-digest
```

Dependencies:
    pip install pyyaml rich (optional, rich enables colored CLI output)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

try:
    import yaml  # type: ignore
except ImportError as exc:
    raise SystemExit(
        "PyYAML is required. Install with `pip install pyyaml` and retry."
    ) from exc

try:
    from rich.console import Console  # type: ignore
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    Console = None  # type: ignore
    Table = None  # type: ignore
    RICH_AVAILABLE = False


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = REPO_ROOT / "agents"
BACKLOG_DIR = REPO_ROOT / "backlog"


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Expected YAML file missing: {path}")
    with path.open("r", encoding="utf-8") as stream:
        return yaml.safe_load(stream) or {}


@dataclass
class AgentPersona:
    id: str
    name: str
    description: str
    mission_focus: List[str] = field(default_factory=list)
    responsibilities: Dict[str, List[str]] = field(default_factory=dict)
    communication_style: Dict[str, Any] = field(default_factory=dict)
    collaborates_with: List[str] = field(default_factory=list)
    hand_off_protocol: List[str] = field(default_factory=list)
    message_templates: Dict[str, str] = field(default_factory=dict)
    success_metrics: List[str] = field(default_factory=list)
    escalation_policy: List[str] = field(default_factory=list)
    tools: List[Dict[str, str]] = field(default_factory=list)

    @classmethod
    def from_yaml(cls, path: Path, roster_entry: Dict[str, Any]) -> "AgentPersona":
        payload = _load_yaml(path)
        if not payload:
            raise ValueError(f"Agent YAML is empty: {path}")

        data = dict(payload)
        data.setdefault("id", roster_entry.get("id"))
        data.setdefault("name", roster_entry.get("name"))

        # Normalise optional fields
        for key, default in (
            ("mission_focus", []),
            ("responsibilities", {}),
            ("communication_style", {}),
            ("collaborates_with", []),
            ("hand_off_protocol", []),
            ("message_templates", {}),
            ("success_metrics", []),
            ("escalation_policy", []),
            ("tools", []),
        ):
            data.setdefault(key, default)

        return cls(
            id=data["id"],
            name=data.get("name", roster_entry.get("name", data["id"])),
            description=data.get("description", ""),
            mission_focus=list(data.get("mission_focus", [])),
            responsibilities=dict(data.get("responsibilities", {})),
            communication_style=dict(data.get("communication_style", {})),
            collaborates_with=list(data.get("collaborates_with", [])),
            hand_off_protocol=list(data.get("hand_off_protocol", [])),
            message_templates=dict(data.get("message_templates", {})),
            success_metrics=list(data.get("success_metrics", [])),
            escalation_policy=list(data.get("escalation_policy", [])),
            tools=list(data.get("tools", [])),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "mission_focus": self.mission_focus,
            "responsibilities": self.responsibilities,
            "communication_style": self.communication_style,
            "collaborates_with": self.collaborates_with,
            "hand_off_protocol": self.hand_off_protocol,
            "message_templates": self.message_templates,
            "success_metrics": self.success_metrics,
            "escalation_policy": self.escalation_policy,
            "tools": self.tools,
        }


class MultiAgentOrchestrator:
    def __init__(self, repo_root: Path = REPO_ROOT) -> None:
        self.repo_root = repo_root
        self._roster = _load_yaml(repo_root / "agents" / "roster.yaml")
        self._agents: Dict[str, AgentPersona] = {}
        self._load_agents()

    @property
    def roster(self) -> Dict[str, Any]:
        return self._roster

    @property
    def agents(self) -> Dict[str, AgentPersona]:
        return self._agents

    def _load_agents(self) -> None:
        agents_meta = self._roster.get("agents", [])
        for entry in agents_meta:
            persona_path = AGENTS_DIR / entry["persona_file"]
            agent = AgentPersona.from_yaml(persona_path, entry)
            self._agents[agent.id] = agent

    # ------------------------------------------------------------------
    # Presentation helpers

    def list_agents(self) -> List[Dict[str, str]]:
        payload = []
        for entry in self._roster.get("agents", []):
            payload.append(
                {
                    "id": entry["id"],
                    "name": entry.get("name", entry["id"]),
                    "purpose": entry.get("purpose", ""),
                }
            )
        return payload

    def get_agent(self, agent_id: str) -> AgentPersona:
        try:
            return self._agents[agent_id]
        except KeyError as exc:
            raise SystemExit(f"Unknown agent id: {agent_id}") from exc

    def generate_standup_prompt(self, on: Optional[str] = None) -> Dict[str, Any]:
        ref_date = dt.date.fromisoformat(on) if on else dt.date.today()
        cadence = self._roster.get("cadence", {})
        host_time = cadence.get("standup_time", "09:00 Europe/Tallinn")
        summary = {
            "standup_date": ref_date.isoformat(),
            "host_time": host_time,
            "mission_control_prompt": textwrap.dedent(
                f"""
                [Mission Control Standup]
                Date: {ref_date.isoformat()} ({host_time})
                Reminder: Share RAG status, key metrics movement, blockers, and next focus.
                """
            ).strip(),
            "agent_prompts": {},
        }
        for agent in self._agents.values():
            focus = ", ".join(agent.mission_focus[:2]) if agent.mission_focus else "core responsibilities"
            summary["agent_prompts"][agent.id] = textwrap.dedent(
                f"""
                [Standup Prompt for {agent.name}]
                - Status (Green/Amber/Red):
                - Highlights: What moved within {focus}?
                - Metrics pulse: Any notable changes?
                - Blockers or asks for peers?
                - Next steps before next check-in?
                """
            ).strip()
        return summary

    def backlog_digest(self) -> List[Dict[str, Any]]:
        tickets: List[Dict[str, Any]] = []
        if not BACKLOG_DIR.exists():
            return tickets
        for path in sorted(BACKLOG_DIR.glob("*.yaml")):
            ticket = _load_yaml(path)
            ticket["path"] = str(path.relative_to(self.repo_root))
            tickets.append(ticket)
        return tickets

    def agenda_for_initiative(self, ticket_id: str) -> str:
        target = None
        for ticket in self.backlog_digest():
            if ticket.get("id") == ticket_id:
                target = ticket
                break
        if not target:
            raise SystemExit(f"Ticket not found in backlog: {ticket_id}")

        owner = target.get("owner")
        contributors = target.get("contributors", [])
        owner_agent = self._agents.get(owner)
        contributor_names = [self._agents[c].name for c in contributors if c in self._agents]
        lines = [
            f"[Initiative Kickoff] {target.get('title')}",
            f"Owner: {owner_agent.name if owner_agent else owner}",
            f"Contributors: {', '.join(contributor_names) if contributor_names else 'n/a'}",
            "Agenda:",
            "1. Restate objective and success metrics",
            "2. Review current context and dependencies",
            "3. Outline workplan, milestones, and checkpoints",
            "4. Identify risks, mitigation, and decision gates",
            "5. Confirm next actions and owners",
        ]
        return "\n".join(lines)


def _print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _print_table(rows: Iterable[Dict[str, str]], headers: List[str]) -> None:
    if RICH_AVAILABLE and Console and Table:  # pragma: no cover - CLI nicety
        console = Console()
        table = Table(show_header=True, header_style="bold")
        for header in headers:
            table.add_column(header)
        for row in rows:
            table.add_row(*(row.get(h, "") for h in headers))
        console.print(table)
    else:
        print(" | ".join(headers))
        for row in rows:
            print(" | ".join(row.get(h, "") for h in headers))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Utilities for coordinating DEPLOYHELP multi-agent workflows."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-agents", help="List agents in the roster")

    show_agent = subparsers.add_parser("show-agent", help="Display full agent profile")
    show_agent.add_argument("agent_id", help="Agent identifier (e.g., mission_control)")

    standup = subparsers.add_parser("standup", help="Generate standup prompts")
    standup.add_argument("--date", help="ISO date (YYYY-MM-DD), defaults to today")
    standup.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON instead of formatted text",
    )

    subparsers.add_parser("ticket-digest", help="Summarise backlog tickets")

    agenda = subparsers.add_parser(
        "agenda", help="Produce kickoff agenda for a specific ticket"
    )
    agenda.add_argument("ticket_id", help="Backlog ticket id")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    orchestrator = MultiAgentOrchestrator()

    if args.command == "list-agents":
        _print_table(orchestrator.list_agents(), ["id", "name", "purpose"])
        return

    if args.command == "show-agent":
        agent = orchestrator.get_agent(args.agent_id)
        _print_json(agent.to_dict())
        return

    if args.command == "standup":
        payload = orchestrator.generate_standup_prompt(on=args.date)
        if args.json:
            _print_json(payload)
        else:
            print(payload["mission_control_prompt"])
            print()
            for agent_id, prompt in payload["agent_prompts"].items():
                agent_name = orchestrator.agents[agent_id].name
                separator = f"{'-' * 8} {agent_name} {'-' * 8}"
                print(separator)
                print(prompt)
                print()
        return

    if args.command == "ticket-digest":
        tickets = orchestrator.backlog_digest()
        if not tickets:
            print("No backlog tickets found.")
            return
        headers = ["id", "status", "priority", "owner", "due", "path"]
        rows = []
        for ticket in tickets:
            rows.append({key: str(ticket.get(key, "")) for key in headers})
        _print_table(rows, headers)
        return

    if args.command == "agenda":
        print(orchestrator.agenda_for_initiative(args.ticket_id))
        return

    parser.error(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    main()

# DEPLOYHELP LLC Multi-Agent Orchestrator

This repository now contains an orchestration framework for coordinating a
specialist group of AI (or human-in-the-loop) agents working on DEPLOYHELP
LLC?s website and broader online presence.

## Repository Structure

- `docs/multi_agent_orchestration_plan.md` ? strategic blueprint and operating
  playbook for the orchestrated team.
- `agents/` ? machine-readable persona definitions and the roster manifest used
  by the orchestrator.
- `backlog/` ? seed work items in YAML format; each ticket captures objectives,
  owners, milestones, and risks.
- `reports/week-01.md` ? template for weekly status reporting from Mission
  Control.
- `scripts/orchestrator.py` ? CLI helper that loads the above artifacts to help
  facilitate conversations, standups, and kickoffs.
- `index.html` ? existing marketing landing page for DEPLOYHELP.

## Using the Orchestrator CLI

Install optional dependencies:

```bash
pip install pyyaml rich
```

Run helpers from the repository root:

```bash
# List agents and their purposes
python scripts/orchestrator.py list-agents

# Inspect a detailed persona definition
python scripts/orchestrator.py show-agent mission_control

# Generate the daily standup prompt (pretty or JSON)
python scripts/orchestrator.py standup --date 2025-11-01
python scripts/orchestrator.py standup --json

# Summarise the backlog or craft a kickoff agenda
python scripts/orchestrator.py ticket-digest
python scripts/orchestrator.py agenda website-refresh-q4-hero
```

## Next Steps

- Expand the backlog with additional initiatives (content calendar, lead magnet
  funnel, analytics automation) following the provided schema.
- Commit brand, voice, and research artifacts under `docs/` to power agent
  decisions.
- Integrate the CLI into a higher-level multi-agent runtime (e.g., via LangChain
  or Autogen) for conversational execution if desired.

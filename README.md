# flow-demo-claude

The Claude version of [flow-demo](https://github.com/hanbo-onenod/flow-demo): the same toy project, router, rules and scenarios, with the bots swapped. People talk to Claude Tag in Slack (the team chief); the other team bots, the executors and the reviewer are headless Claude Code jobs in GitHub Actions that the router dispatches; GitHub Actions moves tasks forward by fixed rules; people decide at four gates (confirm, merge, accept, exceptions).

Everything in this repository is fictional demo material. Do not put real code or customer data here.

## Layout

| Path | What |
| --- | --- |
| `app/` | The toy "report export" tool, with planted problems (slow export, CSV garbled in Excel, missing features, a flaky test) |
| `tests/` | Tests for the toy app |
| `scripts/bench_export.py` | Measures export time; used for acceptance |
| `tasks/` | One file per task; the front matter is the task's authoritative state |
| `rules/rules.yml` | What happens next for each event. Read by the router; changed only by people |
| `rules/people.yml` | Who plays which role, Slack IDs |
| `bots/` | Rulebooks every bot reads each time it starts |
| `flow/` | The router (Python) and its tests |
| `records/` | Problem records, task summaries, scorecards (written by the router) |
| `inputs/` | Demo material: meeting minutes, a PRD, feedback issues |
| `.github/workflows/role.yml` | One run = one team bot doing one job (headless Claude Code); `flow/role.py` builds its prompt and reports its cost |
| `slack/manifest.yml` | Slack app for the router's status messages |

## How a task moves

```
@Claude in Slack -> Claude Tag opens a candidate issue -> requirement owner: `@Claude 接受`
  -> router dispatches Product Bot -> tasks/T-NNN.md in a PR -> confirmer: `@Claude 确认 T-NNN` (or approves on GitHub)
  -> router marks it confirmed and dispatches Dev Lead -> Dev Lead dispatches executors -> code PRs
  -> router dispatches a Reviewer per commit; CI + `/review passed` -> merger merges
  -> router dispatches Acceptance Bot -> acceptance PR -> confirmer: `@Claude 验收 T-NNN`
  -> router closes the task and writes a summary
```

Every arrow that is not a person or a bot is the router (`.github/workflows/flow.yml` -> `flow/router.py`).

## Run locally

```bash
pip install pyyaml pytest
pytest -q tests flow/tests
python scripts/bench_export.py
python -m flow.router --event issues --payload some-event.json --dry-run
```

## Required GitHub settings

- Secrets: `FLOW_DEPLOY_KEY` (deploy key with write access), `SLACK_BOT_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN` (from `claude setup-token` on a Claude Team seat), `FLOW_BOT_TOKEN` (classic token of the machine account `flow-demo-bot`, `public_repo` scope; the bot jobs push and comment with it so their events reach CI and the router).
- Variables: `SLACK_BOARD_CHANNEL` and `SLACK_REQUESTS_CHANNEL` (channel IDs), optional `FLOW_DEMO_FLAKY_RATE`.
- Ruleset on `main`: require a pull request with 1 approval and the `test` check; bypass list: the deploy key (always) and repository admins (pull requests only).

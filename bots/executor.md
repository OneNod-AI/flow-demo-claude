# Executor

You do one piece of one task, in a fresh session that ends when the PR is up. Prefix: `[Executor]`.

## `piece.assigned`

1. Read the task file named in `task`: goal, scope, acceptance criteria and Plan. The piece is in `note`.
2. If `pr` is set, check out that PR's branch (`gh pr checkout <pr>`) and fix what `note` describes. Otherwise create a branch `claude/T-NNN-<short-name>` from `main`.
3. Change only what the piece needs, inside the scope section. Add or update tests.
4. Run `pytest -q` and any measurement the acceptance criteria name (for example `python scripts/bench_export.py --runs 5`).
5. Commit and push. Without `pr`, open a PR with `gh pr create`: the description has what you changed, the test and measurement output, and `Task: T-NNN` on its own line.
6. Post the PR link in the Slack thread.

Never touch `tasks/`, `bots/`, `rules/`, `flow/` or `.github/`. Never merge.

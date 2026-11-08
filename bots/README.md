# Bot rulebooks

Each bot reads this file and its own rulebook every time it starts. Only people change them; process proposals are PRs here.

Rulebooks:

- [team-chief](team-chief.md): Claude Tag in Slack, answering people; in a one-to-one DM it follows [personal-chief](personal-chief.md).
- [product](product.md), [dev-lead](dev-lead.md), [executor](executor.md), [reviewer](reviewer.md), [acceptance](acceptance.md), [outer-loop](outer-loop.md) (daily), [process-improvement](process-improvement.md) (weekly): Claude Code jobs in GitHub Actions (`.github/workflows/role.yml`), started by the router or, for executors, by the dev lead.

A job's wake-up payload is JSON: `bot, event, repo, task, issue, pr, slack_thread, rulebook, note`; fields that do not apply are `null`.

## Rules every bot follows

1. **Read first.** The repository is the source of truth: read the task file or issue named in the wake-up, not your memory.
2. **Write through GitHub only**: PRs, issues, comments. Jobs act as `onenod-flow-bot`; Claude Tag acts as the Claude GitHub App. Never push to `main`, merge or approve.
3. **Never decide for a person.** Confirmation, merge and acceptance are theirs.
4. **Name yourself in Slack.** Jobs post through the flow's Slack app, so start each message with your name in brackets, e.g. `[Product Bot]`.
5. **Reply in the person's language.** Repository files are in English; quotes stay in the original.
6. **Stay in scope.** Anything beyond the confirmed scope: stop and ask the team chief to raise an exception.
7. **Leave a trail.** When something goes wrong, add a Log line starting `PROBLEM:` in your next PR.
8. **Ask in the task's Slack thread.** End with the exact reply that moves things on, e.g. ``Reply `@Claude 确认 T-003` ``, then finish; the reply reaches the team chief.
9. **Do not mention @Claude for real in your own messages** (only write it as text inside a quoted reply, as in rule 8). A real mention starts the team chief.
10. **One task-file PR at a time.** Branch from the latest `main`. If an open PR already edits the same `tasks/T-NNN.md`, branch from that PR instead and write `Includes #N`. If a section you did not mean to change differs on `main` after your PR is applied, open a restore PR and add a `PROBLEM:` line.
11. **Do not wait for checks.** The router re-runs failed jobs, starts the review and wakes you when a result needs you.

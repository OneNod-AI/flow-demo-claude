"""Start another team-bot job. The dev lead uses it to start one executor per piece.

Usage: python scripts/dispatch.py executor --task T-001 --slack-thread <link> --note "piece 1: ..."
Needs FLOW_DISPATCH_TOKEN (the workflow token; it may start workflow_dispatch runs).
"""
import argparse
import json
import os
import sys
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("bot", choices=["executor", "reviewer"])
parser.add_argument("--task", required=True)
parser.add_argument("--slack-thread", default="")
parser.add_argument("--pr", default=None)
parser.add_argument("--note", required=True)
parser.add_argument("--raise-model", action="store_true", help="one step up the model ladder, when the code is harder than the task's risk suggests")
args = parser.parse_args()

repo = os.environ["GITHUB_REPOSITORY"]
payload = {"bot": args.bot, "event": "piece.assigned" if args.bot == "executor" else "code_pr.opened",
           "repo": repo, "task": args.task, "issue": None, "pr": args.pr,
           "slack_thread": args.slack_thread or None, "rulebook": f"bots/{args.bot}.md", "note": args.note,
           "raise_model": args.raise_model}
req = urllib.request.Request(
    f"https://api.github.com/repos/{repo}/actions/workflows/role.yml/dispatches",
    data=json.dumps({"ref": "main", "inputs": {"bot": args.bot, "payload": json.dumps(payload, ensure_ascii=False)}}).encode(),
    method="POST",
    headers={"Authorization": f"Bearer {os.environ['FLOW_DISPATCH_TOKEN']}", "Accept": "application/vnd.github+json"},
)
urllib.request.urlopen(req, timeout=30)
print(f"dispatched {args.bot} for {args.task}")

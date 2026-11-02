"""Post one message to a task's Slack thread (or the board if there is no thread).

Usage: python scripts/slack_say.py "<slack thread permalink or empty>" "[Bot Name] message"
Used by the team-bot jobs; needs SLACK_BOT_TOKEN and SLACK_BOARD_CHANNEL.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flow.effects import LiveEffects  # noqa: E402

if len(sys.argv) != 3:
    sys.exit(__doc__)
LiveEffects(".", os.environ.get("GITHUB_REPOSITORY", "")).slack_thread(sys.argv[1], sys.argv[2])

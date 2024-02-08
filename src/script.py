import asyncio
import re
import subprocess
import sys
from urllib.parse import urljoin

import aiofiles
import httpx

from config import get_settings
from jira_client import JIRAClient

settings = get_settings()
BASE_URL = "https://api.tempo.io/4"


async def get_commit_message():
    async with aiofiles.open(".git/COMMIT_EDITMSG", "r") as file:
        commit_message = await file.read()
    return commit_message.strip()


class APIClient:

    async def add_worklog(self):
        c = JIRAClient(email="d.igissinov@globerce.capital")

        payload = {
            "attributes": [],
            "authorAccountId": c.get_account_id(),
            "billableSeconds": None,
            "description": "feat: implement new endpoint",
            "issueId": int(c.get_issue_id("COLBANK-1937")),
            "remainingEstimateSeconds": None,
            "startDate": "2024-02-08",
            "startTime": "17:06:00",
            "timeSpentSeconds": 3600,
        }

        headers = {"Authorization": f"Bearer {settings.tempo_api_token}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/worklogs", json=payload, headers=headers
            )
            response.raise_for_status()


async def main():
    # Get the commit message asynchronously
    commit_message = await get_commit_message()

    # Validate commit message format
    pattern = r"^[A-Z]+-[0-9]+ [A-Za-z]+: .+$"
    if not re.match(pattern, commit_message):
        print("Invalid commit message format. Commit aborted.")
        sys.exit(1)

    # Extract Jira issue number and commit message
    jira_issue, commit_msg = commit_message.split(" ", 1)
    git_prefix, commit_msg = commit_msg.split(": ", 1)

    print("Jira Issue:", jira_issue)
    print("Git Prefix:", git_prefix)
    print("Commit Message:", commit_msg)

    print("All checks passed. Proceeding with commit.")
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())

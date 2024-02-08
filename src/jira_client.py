from config import get_settings

from jira import JIRA

settings = get_settings()


class JIRAClient:
    """
    https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html
    """

    def __init__(self, email: str) -> None:
        self.jira = JIRA(
            server=settings.jira_url, basic_auth=(email, settings.jira_api_token)
        )

    def get_issue_id(self, issue_number: str):
        return self.jira.issue(issue_number).id

    def get_account_id(self):
        myself = self.jira.myself()
        return myself.get("accountId")


if __name__ == "__main__":
    c = JIRAClient(email="d.igissinov@globerce.capital")
    print(c.get_account_id())

"""
JIRA Data Models

Type-safe representations of JIRA integration data.
"""

from pydantic import BaseModel
from typing import List, Optional


class JiraIssue(BaseModel):
    """JIRA issue representation"""
    id: str
    key: str
    summary: str
    status: str
    type: str  # 'RFE' or 'Bug'
    priority: str
    assignee: str = "Unassigned"
    created: str
    updated: str


class JiraMismatch(BaseModel):
    """Status mismatch between report and JIRA"""
    issue_key: str
    issue_summary: str
    report_status: str
    jira_status: str
    action_needed: str


class JiraCheckResult(BaseModel):
    """Result of JIRA status check"""
    customer_id: str
    total_issues: int
    mismatches: List[JiraMismatch]
    last_checked: str


class JiraUpdateRequest(BaseModel):
    """Update report from JIRA"""
    dry_run: bool = False


class JiraUpdateResult(BaseModel):
    """Result of report update"""
    customer_id: str
    issues_updated: int
    report_path: str
    backup_path: Optional[str] = None



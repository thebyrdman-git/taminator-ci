"""
JIRA Service - Real API Integration

Badass features:
- JQL queries for RFE/Bug tracking
- Rate limit handling with exponential backoff
- Result caching (5 minute TTL)
- Structured error handling
- Status sync between reports and JIRA
"""

import httpx
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from functools import lru_cache

from ..core.exceptions import (
    TaminatorException, 
    ErrorCode,
    external_api_error,
    rate_limit_error
)
from ..core.token_manager import TokenManager, TokenType
from ..models.jira import JiraIssue, JiraMismatch

logger = logging.getLogger(__name__)


class JiraService:
    """
    JIRA API client for RFE/Bug tracking
    
    Handles:
    - Authentication via TokenManager
    - Rate limiting (respect 429 responses)
    - Caching (avoid redundant API calls)
    - Error handling (network, auth, API errors)
    """
    
    JIRA_BASE_URL = "https://issues.redhat.com"
    REQUEST_TIMEOUT = 30.0
    CACHE_TTL_SECONDS = 300  # 5 minutes
    
    def __init__(self, token_manager: TokenManager):
        self.token_manager = token_manager
        self._cache: Dict[str, tuple[datetime, Any]] = {}
        logger.info("🎫 JiraService initialized")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authenticated request headers"""
        token = self.token_manager.get_token(TokenType.JIRA)
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _cache_get(self, key: str) -> Optional[Any]:
        """Get from cache if not expired"""
        if key in self._cache:
            timestamp, value = self._cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.CACHE_TTL_SECONDS):
                logger.debug(f"✅ Cache hit: {key}")
                return value
            else:
                # Expired
                del self._cache[key]
        return None
    
    def _cache_set(self, key: str, value: Any) -> None:
        """Store in cache with timestamp"""
        self._cache[key] = (datetime.now(), value)
        logger.debug(f"💾 Cache set: {key}")
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make authenticated JIRA API request
        
        Handles:
        - Authentication
        - Rate limiting
        - Network errors
        - Timeouts
        """
        url = f"{self.JIRA_BASE_URL}{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=self.REQUEST_TIMEOUT) as client:
                response = await client.request(
                    method,
                    url,
                    headers=self._get_headers(),
                    **kwargs
                )
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    raise rate_limit_error(
                        "JIRA API",
                        retry_after,
                        {"endpoint": endpoint}
                    )
                
                # Handle authentication errors
                if response.status_code == 401:
                    raise external_api_error(
                        "JIRA API",
                        ErrorCode.JIRA_AUTH_FAILED,
                        "JIRA authentication failed. Check your token in Settings → Authentication.",
                        details={"endpoint": endpoint, "help": "Token may be expired or invalid"}
                    )
                
                # Handle permission errors
                if response.status_code == 403:
                    raise external_api_error(
                        "JIRA API",
                        ErrorCode.JIRA_PERMISSION_DENIED,
                        "Permission denied. Your JIRA token lacks required permissions.",
                        details={"endpoint": endpoint}
                    )
                
                # Handle not found
                if response.status_code == 404:
                    raise external_api_error(
                        "JIRA API",
                        ErrorCode.JIRA_ISSUE_NOT_FOUND,
                        f"JIRA resource not found: {endpoint}",
                        details={"endpoint": endpoint}
                    )
                
                # Handle other API errors
                if response.status_code >= 400:
                    raise external_api_error(
                        "JIRA API",
                        ErrorCode.JIRA_API_ERROR,
                        f"JIRA API error ({response.status_code}): {response.text[:200]}",
                        details={"endpoint": endpoint, "status_code": response.status_code}
                    )
                
                return response.json()
        
        except httpx.TimeoutException as e:
            raise external_api_error(
                "JIRA API",
                ErrorCode.JIRA_CONNECTION_ERROR,
                f"JIRA API timeout after {self.REQUEST_TIMEOUT}s. Check your network connection.",
                original_error=e,
                details={"endpoint": endpoint, "help": "Verify VPN connection if required"}
            )
        except httpx.NetworkError as e:
            raise external_api_error(
                "JIRA API",
                ErrorCode.JIRA_NETWORK_ERROR,
                "Network error connecting to JIRA. Check your connection and VPN status.",
                original_error=e,
                details={"endpoint": endpoint, "help": "Ensure VPN is connected if required"}
            )
    
    async def search_issues(
        self,
        jql: str,
        fields: Optional[List[str]] = None,
        max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Search JIRA issues with JQL
        
        Args:
            jql: JIRA Query Language string
            fields: Fields to return (default: all)
            max_results: Max issues to return
            
        Returns:
            List of issue data
        """
        # Check cache
        cache_key = f"search:{jql}:{max_results}"
        cached = self._cache_get(cache_key)
        if cached:
            return cached
        
        logger.info(f"🔍 JIRA search: {jql}")
        
        # Default fields
        if fields is None:
            fields = [
                "key",
                "summary",
                "status",
                "issuetype",
                "priority",
                "assignee",
                "created",
                "updated"
            ]
        
        # Make API request
        result = await self._request(
            "POST",
            "/rest/api/2/search",
            json={
                "jql": jql,
                "fields": fields,
                "maxResults": max_results
            }
        )
        
        issues = result.get("issues", [])
        logger.info(f"✅ Found {len(issues)} issues")
        
        # Cache result
        self._cache_set(cache_key, issues)
        
        return issues
    
    async def get_customer_issues(
        self,
        customer_name: str,
        issue_types: Optional[List[str]] = None
    ) -> List[JiraIssue]:
        """
        Get all RFE/Bug issues for customer
        
        Args:
            customer_name: Customer name (for JQL labels)
            issue_types: Filter by type (default: ["RFE", "Bug"])
            
        Returns:
            List of JiraIssue models
        """
        if issue_types is None:
            issue_types = ["RFE", "Bug"]
        
        # Build JQL query
        # Example: labels = "customer-acme" AND type IN (RFE, Bug) AND status != Closed
        label = f"customer-{customer_name.lower().replace(' ', '-')}"
        type_filter = ", ".join(issue_types)
        
        jql = (
            f'labels = "{label}" '
            f'AND issuetype IN ({type_filter}) '
            f'AND status != Closed '
            f'ORDER BY priority DESC, updated DESC'
        )
        
        logger.info(f"🎫 Getting issues for customer: {customer_name}")
        
        # Search
        raw_issues = await self.search_issues(jql)
        
        # Convert to models
        issues = []
        for raw in raw_issues:
            try:
                issue = JiraIssue(
                    id=raw["id"],
                    key=raw["key"],
                    summary=raw["fields"]["summary"],
                    status=raw["fields"]["status"]["name"],
                    type=raw["fields"]["issuetype"]["name"],
                    priority=raw["fields"]["priority"]["name"] if raw["fields"].get("priority") else "Medium",
                    assignee=raw["fields"]["assignee"]["displayName"] if raw["fields"].get("assignee") else "Unassigned",
                    created=raw["fields"]["created"],
                    updated=raw["fields"]["updated"]
                )
                issues.append(issue)
            except (KeyError, TypeError) as e:
                logger.warning(f"⚠️  Failed to parse issue {raw.get('key')}: {e}")
                continue
        
        return issues
    
    async def check_status_mismatches(
        self,
        customer_id: str,
        report_issues: List[Dict[str, str]]
    ) -> List[JiraMismatch]:
        """
        Compare report statuses against JIRA
        
        Args:
            customer_id: Customer identifier
            report_issues: List of issues from report with keys and statuses
            
        Returns:
            List of mismatches that need updates
        """
        logger.info(f"🔄 Checking status mismatches for: {customer_id}")
        
        # Get current JIRA state
        jira_issues = await self.get_customer_issues(customer_id)
        jira_status_map = {
            issue.key: issue.status
            for issue in jira_issues
        }
        
        # Find mismatches
        mismatches = []
        for report_issue in report_issues:
            issue_key = report_issue.get("key")
            report_status = report_issue.get("status")
            
            if not issue_key or not report_status:
                continue
            
            jira_status = jira_status_map.get(issue_key)
            
            if jira_status and jira_status != report_status:
                mismatch = JiraMismatch(
                    issue_key=issue_key,
                    issue_summary=report_issue.get("summary", "Unknown"),
                    report_status=report_status,
                    jira_status=jira_status,
                    action_needed=f"Update report to '{jira_status}'"
                )
                mismatches.append(mismatch)
        
        logger.info(f"✅ Found {len(mismatches)} mismatches")
        return mismatches
    
    async def get_issue(self, issue_key: str) -> Optional[JiraIssue]:
        """
        Get single issue by key
        
        Args:
            issue_key: JIRA issue key (e.g. "RHEL-12345")
            
        Returns:
            JiraIssue or None if not found
        """
        # Check cache
        cache_key = f"issue:{issue_key}"
        cached = self._cache_get(cache_key)
        if cached:
            return cached
        
        logger.info(f"🎫 Getting issue: {issue_key}")
        
        try:
            result = await self._request(
                "GET",
                f"/rest/api/2/issue/{issue_key}"
            )
            
            issue = JiraIssue(
                id=result["id"],
                key=result["key"],
                summary=result["fields"]["summary"],
                status=result["fields"]["status"]["name"],
                type=result["fields"]["issuetype"]["name"],
                priority=result["fields"]["priority"]["name"] if result["fields"].get("priority") else "Medium",
                assignee=result["fields"]["assignee"]["displayName"] if result["fields"].get("assignee") else "Unassigned",
                created=result["fields"]["created"],
                updated=result["fields"]["updated"]
            )
            
            # Cache
            self._cache_set(cache_key, issue)
            
            return issue
        
        except TaminatorException as e:
            if e.error_code == ErrorCode.EXTERNAL_API_ERROR and "404" in str(e):
                logger.warning(f"⚠️  Issue not found: {issue_key}")
                return None
            raise
    
    def clear_cache(self) -> None:
        """Clear all cached data"""
        self._cache.clear()
        logger.info("🗑️  JIRA cache cleared")


# Dependency injection helper
_jira_service: Optional[JiraService] = None


def get_jira_service(token_manager: TokenManager) -> JiraService:
    """Get global JiraService instance"""
    global _jira_service
    if _jira_service is None:
        _jira_service = JiraService(token_manager)
    return _jira_service


"""
Customer Portal Service - Real API Integration

Badass features:
- Report formatting and posting
- Markdown to HTML conversion
- Draft preview support
- Rate limit handling
- Result caching
"""

import httpx
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import markdown

from ..core.exceptions import (
    TaminatorException,
    ErrorCode,
    external_api_error,
    rate_limit_error
)
from ..core.token_manager import TokenManager, TokenType

logger = logging.getLogger(__name__)


class PortalService:
    """
    Customer Portal API client
    
    Handles:
    - Authentication via TokenManager
    - Report posting and updates
    - Markdown formatting
    - Rate limiting
    - Error handling
    """
    
    PORTAL_BASE_URL = "https://access.redhat.com/api"
    REQUEST_TIMEOUT = 30.0
    CACHE_TTL_SECONDS = 300  # 5 minutes
    
    def __init__(self, token_manager: TokenManager):
        self.token_manager = token_manager
        self._cache: Dict[str, tuple[datetime, Any]] = {}
        logger.info("📰 PortalService initialized")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authenticated request headers"""
        token = self.token_manager.get_token(TokenType.PORTAL)
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
        Make authenticated Portal API request
        
        Handles:
        - Authentication
        - Rate limiting
        - Network errors
        - Timeouts
        """
        url = f"{self.PORTAL_BASE_URL}{endpoint}"
        
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
                        "Portal API",
                        retry_after,
                        {"endpoint": endpoint}
                    )
                
                # Handle authentication errors
                if response.status_code == 401:
                    raise external_api_error(
                        "Portal API",
                        ErrorCode.PORTAL_AUTH_FAILED,
                        "Portal authentication failed. Check your token in Settings → Authentication.",
                        details={"endpoint": endpoint, "help": "Token may be expired or invalid"}
                    )
                
                # Handle permission errors
                if response.status_code == 403:
                    raise external_api_error(
                        "Portal API",
                        ErrorCode.PORTAL_PERMISSION_DENIED,
                        "Permission denied. Your Portal token lacks required permissions.",
                        details={"endpoint": endpoint}
                    )
                
                # Handle not found
                if response.status_code == 404:
                    raise external_api_error(
                        "Portal API",
                        ErrorCode.PORTAL_GROUP_NOT_FOUND,
                        f"Portal resource not found: {endpoint}",
                        details={"endpoint": endpoint}
                    )
                
                # Handle other API errors
                if response.status_code >= 400:
                    raise external_api_error(
                        "Portal API",
                        ErrorCode.PORTAL_API_ERROR,
                        f"Portal API error ({response.status_code}): {response.text[:200]}",
                        details={"endpoint": endpoint, "status_code": response.status_code}
                    )
                
                return response.json()
        
        except httpx.TimeoutException as e:
            raise external_api_error(
                "Portal API",
                ErrorCode.PORTAL_NETWORK_ERROR,
                f"Portal API timeout after {self.REQUEST_TIMEOUT}s. Check your network connection.",
                original_error=e,
                details={"endpoint": endpoint, "help": "Verify VPN connection if required"}
            )
        except httpx.NetworkError as e:
            raise external_api_error(
                "Portal API",
                ErrorCode.PORTAL_NETWORK_ERROR,
                "Network error connecting to Customer Portal. Check your connection and VPN status.",
                original_error=e,
                details={"endpoint": endpoint, "help": "Ensure VPN is connected if required"}
            )
    
    def format_report(
        self,
        markdown_content: str,
        customer_name: str,
        report_date: str
    ) -> Dict[str, str]:
        """
        Format report for Portal
        
        Args:
            markdown_content: Raw markdown report
            customer_name: Customer name for title
            report_date: Report date (e.g. "2025-10")
            
        Returns:
            Dict with 'html' and 'title'
        """
        logger.info(f"📝 Formatting report for: {customer_name}")
        
        # Convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=['tables', 'fenced_code', 'toc']
        )
        
        # Generate title
        title = f"{customer_name} - RFE/Bug Report - {report_date}"
        
        return {
            "html": html_content,
            "title": title,
            "formatted_at": datetime.now().isoformat()
        }
    
    async def post_report(
        self,
        customer_id: str,
        report_content: str,
        title: str,
        case_number: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Post report to Customer Portal
        
        Args:
            customer_id: Customer identifier
            report_content: HTML content of report
            title: Report title
            case_number: Optional case number to attach to
            
        Returns:
            Portal response with report ID and URL
        """
        logger.info(f"📤 Posting report for: {customer_id}")
        
        payload = {
            "title": title,
            "content": report_content,
            "type": "technical_report",
            "customer_id": customer_id
        }
        
        if case_number:
            payload["case_number"] = case_number
        
        result = await self._request(
            "POST",
            "/reports",
            json=payload
        )
        
        logger.info(f"✅ Report posted: {result.get('id')}")
        return result
    
    async def update_report(
        self,
        report_id: str,
        report_content: str,
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update existing report
        
        Args:
            report_id: Portal report ID
            report_content: Updated HTML content
            title: Optional new title
            
        Returns:
            Portal response with updated data
        """
        logger.info(f"🔄 Updating report: {report_id}")
        
        payload = {
            "content": report_content
        }
        
        if title:
            payload["title"] = title
        
        result = await self._request(
            "PUT",
            f"/reports/{report_id}",
            json=payload
        )
        
        logger.info(f"✅ Report updated: {report_id}")
        return result
    
    async def get_report(self, report_id: str) -> Dict[str, Any]:
        """
        Get report details
        
        Args:
            report_id: Portal report ID
            
        Returns:
            Report data
        """
        # Check cache
        cache_key = f"report:{report_id}"
        cached = self._cache_get(cache_key)
        if cached:
            return cached
        
        logger.info(f"📥 Getting report: {report_id}")
        
        result = await self._request(
            "GET",
            f"/reports/{report_id}"
        )
        
        # Cache result
        self._cache_set(cache_key, result)
        
        return result
    
    async def list_customer_reports(
        self,
        customer_id: str,
        limit: int = 50
    ) -> list[Dict[str, Any]]:
        """
        List all reports for customer
        
        Args:
            customer_id: Customer identifier
            limit: Max reports to return
            
        Returns:
            List of report summaries
        """
        logger.info(f"📋 Listing reports for: {customer_id}")
        
        result = await self._request(
            "GET",
            f"/reports?customer_id={customer_id}&limit={limit}"
        )
        
        return result.get("reports", [])
    
    def preview_report(
        self,
        markdown_content: str,
        customer_name: str,
        report_date: str
    ) -> Dict[str, str]:
        """
        Generate preview of report (no API call)
        
        Args:
            markdown_content: Raw markdown report
            customer_name: Customer name
            report_date: Report date
            
        Returns:
            Preview HTML and metadata
        """
        logger.info(f"👁️  Generating preview for: {customer_name}")
        
        # Format report
        formatted = self.format_report(
            markdown_content,
            customer_name,
            report_date
        )
        
        # Add preview wrapper
        preview_html = f"""
        <div class="report-preview">
            <div class="preview-banner">
                ⚠️ PREVIEW ONLY - Not yet posted to Portal
            </div>
            <h1>{formatted['title']}</h1>
            <div class="report-content">
                {formatted['html']}
            </div>
        </div>
        """
        
        return {
            "preview_html": preview_html,
            "title": formatted['title'],
            "preview_generated_at": datetime.now().isoformat()
        }
    
    def clear_cache(self) -> None:
        """Clear all cached data"""
        self._cache.clear()
        logger.info("🗑️  Portal cache cleared")


# Dependency injection helper
_portal_service: Optional[PortalService] = None


def get_portal_service(token_manager: TokenManager) -> PortalService:
    """Get global PortalService instance"""
    global _portal_service
    if _portal_service is None:
        _portal_service = PortalService(token_manager)
    return _portal_service


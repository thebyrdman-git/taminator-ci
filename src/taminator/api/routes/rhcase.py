"""
RHCase API Routes
Endpoints for rhcase bot functionality
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from ...services.rhcase_service import RhcaseService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/rhcase", tags=["rhcase"])

# Initialize service
rhcase_service = RhcaseService()


# Request Models
class RhcaseExecuteRequest(BaseModel):
    """Request to execute rhcase command"""
    command: str
    timeout: Optional[int] = 60


class RhcaseAnalyzeRequest(BaseModel):
    """Request to analyze a case"""
    case_id: str


class RhcaseListRequest(BaseModel):
    """Request to list cases"""
    account: Optional[str] = None


class RhcaseKCSSearchRequest(BaseModel):
    """Request to search KCS"""
    query: str
    product: Optional[str] = None
    version: Optional[str] = None
    limit: Optional[int] = 10


class RhcaseJiraSearchRequest(BaseModel):
    """Request to search JIRA"""
    query: str


class RhcaseCVERequest(BaseModel):
    """Request to lookup CVE"""
    cve_id: str


# Routes
@router.get("/health")
async def rhcase_health():
    """
    Check rhcase availability and health
    
    Returns:
        Rhcase installation info and health status
    """
    try:
        info = rhcase_service.get_info()
        
        return {
            "available": info["available"],
            "path": info["path"],
            "version": info["version"],
            "bundled": info["bundled"]
        }
    except Exception as e:
        logger.error(f"❌ rhcase health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute")
async def execute_command(request: RhcaseExecuteRequest):
    """
    Execute arbitrary rhcase command
    
    Args:
        request: Command to execute
        
    Returns:
        Command output and status
    """
    try:
        result = await rhcase_service.execute(
            request.command,
            timeout=request.timeout
        )
        
        return result
        
    except RuntimeError as e:
        logger.error(f"❌ rhcase execution failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze")
async def analyze_case(request: RhcaseAnalyzeRequest):
    """
    Analyze a specific support case
    
    Args:
        request: Case ID to analyze
        
    Returns:
        Case analysis results
    """
    try:
        result = await rhcase_service.analyze_case(request.case_id)
        return result
    except Exception as e:
        logger.error(f"❌ Case analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/list")
async def list_cases(request: RhcaseListRequest):
    """
    List support cases for an account
    
    Args:
        request: Account name (optional)
        
    Returns:
        List of cases
    """
    try:
        result = await rhcase_service.list_cases(request.account)
        return result
    except Exception as e:
        logger.error(f"❌ Case listing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/kcs/search")
async def search_kcs(request: RhcaseKCSSearchRequest):
    """
    Search Red Hat KCS articles
    
    Args:
        request: Search parameters
        
    Returns:
        KCS search results
    """
    try:
        # Build search command with options
        command = f"kcs search {request.query}"
        
        if request.product:
            command += f" --product '{request.product}'"
        
        if request.version:
            command += f" --version '{request.version}'"
        
        if request.limit:
            command += f" --limit {request.limit}"
        
        result = await rhcase_service.execute(command)
        return result
    except Exception as e:
        logger.error(f"❌ KCS search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/kcs/fetch/{kcs_id}")
async def fetch_kcs(kcs_id: str):
    """
    Fetch a specific KCS article
    
    Args:
        kcs_id: KCS article ID
        
    Returns:
        KCS article content (markdown)
    """
    try:
        result = await rhcase_service.execute(f"kcs fetch {kcs_id}")
        return result
    except Exception as e:
        logger.error(f"❌ KCS fetch failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/jira/search")
async def search_jira(request: RhcaseJiraSearchRequest):
    """
    Search JIRA issues via rhcase
    
    Args:
        request: Search query (JQL or text)
        
    Returns:
        JIRA search results
    """
    try:
        result = await rhcase_service.execute(f"jira search {request.query}")
        return result
    except Exception as e:
        logger.error(f"❌ JIRA search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jira/fetch/{issue_id}")
async def fetch_jira(issue_id: str):
    """
    Fetch a specific JIRA issue
    
    Args:
        issue_id: JIRA issue ID (e.g., RFE-8101)
        
    Returns:
        JIRA issue details
    """
    try:
        result = await rhcase_service.execute(f"jira fetch {issue_id}")
        return result
    except Exception as e:
        logger.error(f"❌ JIRA fetch failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jira/projects")
async def list_jira_projects():
    """
    List all accessible JIRA projects
    
    Returns:
        List of JIRA projects
    """
    try:
        result = await rhcase_service.execute("jira projects")
        return result
    except Exception as e:
        logger.error(f"❌ JIRA projects listing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cve")
async def lookup_cve(request: RhcaseCVERequest):
    """
    Lookup CVE information
    
    Args:
        request: CVE ID (e.g., CVE-2023-5366)
        
    Returns:
        CVE details
    """
    try:
        result = await rhcase_service.execute(f"cve {request.cve_id}")
        return result
    except Exception as e:
        logger.error(f"❌ CVE lookup failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/doctor")
async def run_doctor():
    """
    Run rhcase health diagnostics
    
    Returns:
        Diagnostic results
    """
    try:
        result = await rhcase_service.health_check()
        return result
    except Exception as e:
        logger.error(f"❌ rhcase doctor failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


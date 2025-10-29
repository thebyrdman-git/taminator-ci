"""
Intelligence API Routes

Endpoints for AI-augmented case analysis
"""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from ...core.intelligence_engine import get_intelligence_engine, CaseIntelligence

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/intelligence", tags=["intelligence"])


# ============================================================================
# Request/Response Models
# ============================================================================

class AnalyzeEmailRequest(BaseModel):
    """Request to analyze email thread"""
    email_text: str
    tags: Optional[List[str]] = None  # ["case_number", "customer", "contacts", "issue", "urgency", "all"]


class AnalyzeEmailResponse(BaseModel):
    """Response with extracted intelligence"""
    success: bool
    intelligence: dict
    confidence_level: str
    confidence_score: float
    message: str


# ============================================================================
# Routes
# ============================================================================

@router.post("/analyze-email", response_model=AnalyzeEmailResponse)
async def analyze_email(request: AnalyzeEmailRequest):
    """
    Analyze email thread and extract intelligence
    
    This is the core AI-augmented feature:
    - Paste email thread
    - Get structured case intelligence
    - Confidence scoring
    - Action recommendations
    
    Example:
    ```
    POST /intelligence/analyze-email
    {
        "email_text": "...",
        "tags": ["all"]  // or ["case_number", "customer"] for quick extraction
    }
    ```
    """
    try:
        logger.info("📧 Analyzing email thread...")
        
        # Get intelligence engine
        engine = get_intelligence_engine()
        
        # Analyze email
        intelligence = engine.analyze_email(
            email_text=request.email_text,
            tags=request.tags
        )
        
        # Get confidence
        confidence_level, confidence_score = intelligence.get_overall_confidence()
        
        logger.info(f"✅ Analysis complete. Confidence: {confidence_level.value} ({confidence_score:.2f})")
        
        return AnalyzeEmailResponse(
            success=True,
            intelligence=intelligence.to_dict(),
            confidence_level=confidence_level.value,
            confidence_score=confidence_score,
            message=f"Intelligence extracted with {confidence_level.value} confidence"
        )
    
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_status():
    """Get intelligence engine status"""
    try:
        engine = get_intelligence_engine()
        
        return {
            "success": True,
            "status": "operational",
            "engine": "IntelligenceEngine v1.0",
            "features": [
                "Email analysis",
                "Issue classification",
                "Urgency assessment",
                "Contact extraction",
                "Action recommendations"
            ]
        }
    
    except Exception as e:
        logger.error(f"❌ Status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


"""
Taminator Intelligence Engine

Core intelligence extraction and analysis system.
Follows the "Geerling Pattern": Leverage proven libraries, write thin wrappers.

Architecture:
- Email Analysis: Extract structured data from unstructured text
- Issue Classification: Categorize issues (licensing, technical, guidance, strategic)
- Risk Assessment: Evaluate urgency, impact, complexity
- Contact Extraction: Identify people, roles, organizations
- Confidence Scoring: Measure analysis reliability
- Action Recommendation: Suggest next steps

Design Philosophy:
- 75% proven libraries (spaCy, transformers, etc.)
- 25% TAM-specific logic
- Progressive enhancement (tag-based extraction)
- Self-healing (feedback loop for improvement)
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================================
# Data Models
# ============================================================================

class IssueType(str, Enum):
    """Issue classification types"""
    LICENSING = "licensing"
    TECHNICAL = "technical"
    GUIDANCE = "guidance"
    STRATEGIC = "strategic"
    UNKNOWN = "unknown"


class UrgencyLevel(str, Enum):
    """Urgency levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class ConfidenceLevel(str, Enum):
    """Confidence levels for analysis"""
    HIGH = "high"  # >= 0.8
    MEDIUM = "medium"  # 0.5 - 0.8
    LOW = "low"  # < 0.5


@dataclass
class Contact:
    """Extracted contact information"""
    name: str
    email: Optional[str] = None
    title: Optional[str] = None
    organization: Optional[str] = None
    role: Optional[str] = None  # "decision_maker", "technical_contact", "stakeholder"
    phone: Optional[str] = None


@dataclass
class CustomerInfo:
    """Customer identification"""
    name: str
    account_number: Optional[str] = None
    detected_from: str = "email_domain"  # "email_domain", "signature", "manual"
    confidence: float = 0.0


@dataclass
class IssueClassification:
    """Issue type and details"""
    primary_type: IssueType
    subtype: Optional[str] = None
    product: Optional[str] = None
    application: Optional[str] = None
    confidence: float = 0.0
    reasoning: str = ""
    keywords: List[str] = field(default_factory=list)


@dataclass
class UrgencyAssessment:
    """Urgency evaluation"""
    level: UrgencyLevel
    deadline: Optional[datetime] = None
    days_remaining: Optional[int] = None
    indicators: List[str] = field(default_factory=list)
    score: float = 0.0


@dataclass
class ActionRecommendation:
    """Recommended next steps"""
    primary_action: str
    reasoning: str
    escalation_targets: List[str] = field(default_factory=list)
    immediate_actions: List[str] = field(default_factory=list)
    short_term_actions: List[str] = field(default_factory=list)
    long_term_actions: List[str] = field(default_factory=list)


@dataclass
class CaseIntelligence:
    """Complete intelligence package"""
    # Core identification
    case_number: Optional[str] = None
    customer: Optional[CustomerInfo] = None
    contacts: List[Contact] = field(default_factory=list)
    
    # Analysis
    issue: Optional[IssueClassification] = None
    urgency: Optional[UrgencyAssessment] = None
    recommended_actions: Optional[ActionRecommendation] = None
    
    # Metadata
    source: str = "email"  # "email", "case_system", "manual"
    extracted_at: datetime = field(default_factory=datetime.now)
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
    def get_overall_confidence(self) -> Tuple[ConfidenceLevel, float]:
        """Calculate overall confidence score"""
        if not self.confidence_scores:
            return ConfidenceLevel.LOW, 0.0
        
        avg_confidence = sum(self.confidence_scores.values()) / len(self.confidence_scores)
        
        if avg_confidence >= 0.8:
            return ConfidenceLevel.HIGH, avg_confidence
        elif avg_confidence >= 0.5:
            return ConfidenceLevel.MEDIUM, avg_confidence
        else:
            return ConfidenceLevel.LOW, avg_confidence


# ============================================================================
# Intelligence Engine
# ============================================================================

class IntelligenceEngine:
    """
    Core intelligence extraction engine
    
    Thin wrapper around proven NLP techniques:
    - Regex patterns for structured data (case numbers, emails, phones)
    - Keyword matching for classification
    - Rule-based urgency detection
    - Pattern recognition for contacts
    
    Future: Integrate spaCy for entity extraction, transformers for classification
    """
    
    # Regex patterns for structured data extraction
    PATTERNS = {
        "case_number": [
            r"case[#\s]*(\d{8})",  # "case# 04293185", "case 04293185"
            r"case\s+number[:\s]*(\d{8})",  # "case number: 04293185"
            r"\b(\d{8})\b",  # Standalone 8-digit number
        ],
        "email": r"[\w\.-]+@[\w\.-]+\.\w+",
        "phone": r"(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
        "account_number": r"account[#\s]*(\d{6,7})",
    }
    
    # Issue classification keywords
    ISSUE_KEYWORDS = {
        IssueType.LICENSING: [
            "subscription", "renewal", "license", "entitlement",
            "expires", "expiration", "renew", "allocate", "allocation"
        ],
        IssueType.TECHNICAL: [
            "error", "failure", "not working", "broken", "crash",
            "issue", "problem", "bug", "outage", "down"
        ],
        IssueType.GUIDANCE: [
            "how to", "best practice", "recommendation", "advice",
            "guidance", "help", "assist", "configure", "setup"
        ],
        IssueType.STRATEGIC: [
            "upgrade", "migration", "expansion", "roadmap",
            "planning", "architecture", "design", "roi"
        ]
    }
    
    # Urgency indicators
    URGENCY_INDICATORS = {
        "high": [
            "urgent", "critical", "emergency", "asap", "immediately",
            "cannot afford", "production", "outage", "down"
        ],
        "medium": [
            "important", "soon", "needed", "required", "deadline"
        ],
        "low": [
            "when possible", "future", "planning", "eventually"
        ]
    }
    
    # Product/application patterns
    PRODUCTS = {
        "Ansible Automation Platform": ["ansible", "aap", "automation platform", "tower", "awx"],
        "OpenShift": ["openshift", "ocp", "kubernetes", "k8s"],
        "RHEL": ["rhel", "red hat enterprise linux", "enterprise linux"],
    }
    
    def __init__(self):
        """Initialize intelligence engine"""
        logger.info("🧠 Intelligence Engine initialized")
    
    def analyze_email(self, email_text: str, tags: Optional[List[str]] = None) -> CaseIntelligence:
        """
        Extract intelligence from email thread
        
        Args:
            email_text: Raw email content
            tags: Optional list of extraction tags for incremental analysis
                  ["case_number", "customer", "contacts", "issue", "urgency", "all"]
        
        Returns:
            CaseIntelligence object with extracted data
        """
        logger.info("📧 Analyzing email thread...")
        
        # Default to full analysis
        if not tags:
            tags = ["all"]
        
        intelligence = CaseIntelligence(source="email")
        
        # Tag-based extraction (incremental intelligence)
        if "all" in tags or "case_number" in tags:
            intelligence.case_number = self._extract_case_number(email_text)
            intelligence.confidence_scores["case_number"] = 0.95 if intelligence.case_number else 0.0
        
        if "all" in tags or "customer" in tags:
            intelligence.customer = self._extract_customer(email_text)
            if intelligence.customer:
                intelligence.confidence_scores["customer"] = intelligence.customer.confidence
        
        if "all" in tags or "contacts" in tags:
            intelligence.contacts = self._extract_contacts(email_text)
            intelligence.confidence_scores["contacts"] = 0.8 if intelligence.contacts else 0.0
        
        if "all" in tags or "issue" in tags:
            intelligence.issue = self._classify_issue(email_text)
            if intelligence.issue:
                intelligence.confidence_scores["issue"] = intelligence.issue.confidence
        
        if "all" in tags or "urgency" in tags:
            intelligence.urgency = self._assess_urgency(email_text)
            if intelligence.urgency:
                intelligence.confidence_scores["urgency"] = intelligence.urgency.score
        
        if "all" in tags or "actions" in tags:
            intelligence.recommended_actions = self._recommend_actions(intelligence)
        
        logger.info(f"✅ Analysis complete. Confidence: {intelligence.get_overall_confidence()}")
        return intelligence
    
    def _extract_case_number(self, text: str) -> Optional[str]:
        """Extract case number from text"""
        text_lower = text.lower()
        
        for pattern in self.PATTERNS["case_number"]:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                # Return first 8-digit number found
                case_num = matches[0] if isinstance(matches[0], str) else matches[0][0]
                logger.debug(f"📋 Found case number: {case_num}")
                return case_num
        
        return None
    
    def _extract_customer(self, text: str) -> Optional[CustomerInfo]:
        """Extract customer information from email"""
        # Extract email domain
        emails = re.findall(self.PATTERNS["email"], text, re.IGNORECASE)
        
        if not emails:
            return None
        
        # Get domain from first email
        domain = emails[0].split('@')[1].lower()
        
        # Map common domains to customer names
        customer_map = {
            "jpmchase.com": ("JP Morgan Chase", "334224"),
            "wellsfargo.com": ("Wells Fargo", "838043"),
            "fanniemae.com": ("Fannie Mae", "1460290"),
            "td.com": ("TD Bank", "1912101"),
            "tdbank.com": ("TD Bank", "1912101"),
        }
        
        if domain in customer_map:
            name, account = customer_map[domain]
            logger.debug(f"🏢 Identified customer: {name} ({account})")
            return CustomerInfo(
                name=name,
                account_number=account,
                detected_from="email_domain",
                confidence=0.92
            )
        
        # Unknown domain - extract company name from domain
        company_name = domain.split('.')[0].title()
        logger.debug(f"🏢 Unknown customer domain: {domain} → {company_name}")
        return CustomerInfo(
            name=company_name,
            detected_from="email_domain",
            confidence=0.5
        )
    
    def _extract_contacts(self, text: str) -> List[Contact]:
        """Extract contact information from email"""
        contacts = []
        
        # Extract emails
        emails = re.findall(self.PATTERNS["email"], text, re.IGNORECASE)
        
        # Extract phones
        phones = re.findall(self.PATTERNS["phone"], text, re.IGNORECASE)
        
        # Simple name extraction (lines with common title patterns)
        name_patterns = [
            r"([A-Z][a-z]+ [A-Z][a-z]+)[,\s]+([A-Z][A-Z]+)",  # "John Doe, VP"
            r"([A-Z][a-z]+ [A-Z][a-z]+)\s*\|",  # "John Doe |"
            r"From:\s*([A-Z][a-z]+ [A-Z][a-z]+)",  # "From: John Doe"
        ]
        
        for pattern in name_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                name = match[0] if isinstance(match, tuple) else match
                
                # Try to find associated email
                email = None
                for e in emails:
                    if name.lower().replace(' ', '.') in e.lower() or \
                       name.lower().replace(' ', '') in e.lower():
                        email = e
                        break
                
                # Determine role based on title keywords
                role = "technical_contact"  # default
                if any(title in text.lower() for title in ["vp", "vice president", "director"]):
                    role = "decision_maker"
                
                contacts.append(Contact(
                    name=name,
                    email=email,
                    role=role
                ))
        
        logger.debug(f"👥 Extracted {len(contacts)} contacts")
        return contacts
    
    def _classify_issue(self, text: str) -> IssueClassification:
        """Classify issue type based on keywords"""
        text_lower = text.lower()
        
        # Count keyword matches for each issue type
        scores = {}
        matched_keywords = {}
        
        for issue_type, keywords in self.ISSUE_KEYWORDS.items():
            matches = [kw for kw in keywords if kw in text_lower]
            scores[issue_type] = len(matches)
            matched_keywords[issue_type] = matches
        
        # Find highest scoring type
        if not any(scores.values()):
            return IssueClassification(
                primary_type=IssueType.UNKNOWN,
                confidence=0.0,
                reasoning="No clear issue type indicators found"
            )
        
        primary_type = max(scores, key=scores.get)
        max_score = scores[primary_type]
        total_keywords = len(self.ISSUE_KEYWORDS[primary_type])
        confidence = min(max_score / total_keywords * 2, 1.0)  # Scale to 0-1
        
        # Detect product
        product = None
        for prod_name, prod_keywords in self.PRODUCTS.items():
            if any(kw in text_lower for kw in prod_keywords):
                product = prod_name
                break
        
        logger.debug(f"🏷️  Classified as {primary_type.value} (confidence: {confidence:.2f})")
        
        return IssueClassification(
            primary_type=primary_type,
            product=product,
            confidence=confidence,
            reasoning=f"Matched keywords: {', '.join(matched_keywords[primary_type][:3])}",
            keywords=matched_keywords[primary_type]
        )
    
    def _assess_urgency(self, text: str) -> UrgencyAssessment:
        """Assess urgency based on indicators and deadlines"""
        text_lower = text.lower()
        
        # Check for urgency indicators
        indicators = []
        urgency_scores = {"high": 0, "medium": 0, "low": 0}
        
        for level, keywords in self.URGENCY_INDICATORS.items():
            matches = [kw for kw in keywords if kw in text_lower]
            urgency_scores[level] = len(matches)
            indicators.extend(matches)
        
        # Determine urgency level
        if urgency_scores["high"] > 0:
            level = UrgencyLevel.HIGH
            score = 0.9
        elif urgency_scores["medium"] > 0:
            level = UrgencyLevel.MEDIUM
            score = 0.6
        elif urgency_scores["low"] > 0:
            level = UrgencyLevel.LOW
            score = 0.3
        else:
            level = UrgencyLevel.UNKNOWN
            score = 0.0
        
        # Extract deadline if present
        deadline = None
        days_remaining = None
        
        # Simple date patterns (expand as needed)
        date_patterns = [
            r"(december|dec)\s+(\d{1,2}),?\s+(\d{4})",
            r"(\d{1,2})/(\d{1,2})/(\d{4})",
            r"expires?:?\s+(\d{1,2})/(\d{1,2})/(\d{4})",
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text_lower)
            if match:
                # Parse date (simplified - would use dateutil in production)
                try:
                    if "december" in pattern or "dec" in pattern:
                        month = 12
                        day = int(match.group(2))
                        year = int(match.group(3))
                    else:
                        month = int(match.group(1))
                        day = int(match.group(2))
                        year = int(match.group(3))
                    
                    deadline = datetime(year, month, day)
                    days_remaining = (deadline - datetime.now()).days
                    
                    # Adjust urgency based on deadline
                    if days_remaining < 30:
                        level = UrgencyLevel.HIGH
                        score = max(score, 0.9)
                    elif days_remaining < 90:
                        level = UrgencyLevel.MEDIUM
                        score = max(score, 0.6)
                    
                    break
                except:
                    pass
        
        logger.debug(f"⏰ Urgency: {level.value} (score: {score:.2f})")
        
        return UrgencyAssessment(
            level=level,
            deadline=deadline,
            days_remaining=days_remaining,
            indicators=indicators,
            score=score
        )
    
    def _recommend_actions(self, intelligence: CaseIntelligence) -> ActionRecommendation:
        """Generate action recommendations based on analysis"""
        
        # Default recommendation
        primary_action = "Review case details and respond to customer"
        reasoning = "Standard case workflow"
        escalation_targets = []
        immediate_actions = []
        
        # Customize based on issue type
        if intelligence.issue:
            if intelligence.issue.primary_type == IssueType.LICENSING:
                primary_action = "Escalate to licensing team"
                reasoning = "Subscription/licensing issues require licensing team expertise"
                escalation_targets = ["licensing_team", "account_executive"]
                immediate_actions = [
                    "Verify customer subscription entitlements",
                    "Check renewal timeline",
                    "Loop in account executive if needed"
                ]
            
            elif intelligence.issue.primary_type == IssueType.TECHNICAL:
                primary_action = "Begin technical troubleshooting"
                reasoning = "Technical issue requires investigation"
                immediate_actions = [
                    "Request sosreport or must-gather",
                    "Review logs and error messages",
                    "Check KCS for known issues"
                ]
            
            elif intelligence.issue.primary_type == IssueType.GUIDANCE:
                primary_action = "Provide documentation and guidance"
                reasoning = "Customer needs guidance on best practices"
                immediate_actions = [
                    "Search KCS for relevant articles",
                    "Provide documentation links",
                    "Offer to schedule consultation call"
                ]
            
            elif intelligence.issue.primary_type == IssueType.STRATEGIC:
                primary_action = "Schedule TAM engagement"
                reasoning = "Strategic planning requires TAM consultation"
                immediate_actions = [
                    "Schedule architecture review call",
                    "Engage solution architect if needed",
                    "Prepare business case materials"
                ]
        
        # Adjust based on urgency
        if intelligence.urgency and intelligence.urgency.level == UrgencyLevel.HIGH:
            immediate_actions.insert(0, "⚠️ HIGH PRIORITY - Address immediately")
            if intelligence.urgency.deadline:
                immediate_actions.append(
                    f"Monitor deadline: {intelligence.urgency.deadline.strftime('%Y-%m-%d')} "
                    f"({intelligence.urgency.days_remaining} days remaining)"
                )
        
        logger.debug(f"💡 Recommended action: {primary_action}")
        
        return ActionRecommendation(
            primary_action=primary_action,
            reasoning=reasoning,
            escalation_targets=escalation_targets,
            immediate_actions=immediate_actions,
            short_term_actions=[
                "Update case with findings",
                "Document resolution steps",
                "Follow up with customer"
            ],
            long_term_actions=[
                "Schedule post-resolution check-in",
                "Identify improvement opportunities",
                "Update customer profile with learnings"
            ]
        )


# ============================================================================
# Global Singleton
# ============================================================================

_intelligence_engine: Optional[IntelligenceEngine] = None


def get_intelligence_engine() -> IntelligenceEngine:
    """Get global IntelligenceEngine instance"""
    global _intelligence_engine
    
    if _intelligence_engine is None:
        _intelligence_engine = IntelligenceEngine()
    
    return _intelligence_engine


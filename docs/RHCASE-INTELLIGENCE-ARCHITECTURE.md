# rhcase Intelligence - Tesla Architecture

## Vision: AI-Powered Case Analysis

Transform raw rhcase data into actionable intelligence with AI-powered insights.

---

## What We're Building

### 1. **Intelligent Case Dashboard**
Not just a list of cases - **insights and patterns**.

```
┌─────────────────────────────────────────────────────────────┐
│ 🔍 Case Intelligence - ACME Corporation                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📊 Health Score: 72/100 (Good)                             │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 72%                   │
│                                                              │
│  🔥 Hot Issues (Need Attention)                             │
│   • Case 03245678 - Performance degradation (5 days old)   │
│     Similar to RHEL-11111 (suggest linking)                │
│                                                              │
│   • Case 03245679 - Installation failure (2 days old)      │
│     Pattern: 3 similar cases this month                    │
│                                                              │
│  📈 Trends (Last 30 Days)                                    │
│   • Performance issues up 40%                               │
│   • Security cases down 20%                                 │
│   • Average resolution time: 3.2 days (target: 2 days)     │
│                                                              │
│  💡 AI Recommendations                                       │
│   1. Create RFE for recurring performance issue (3 cases)  │
│   2. Schedule proactive call (no contact in 14 days)       │
│   3. Review Case 03245678 for escalation risk              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2. **Case-to-RFE Correlation**
AI automatically suggests when cases should become RFEs.

```
Case 03245678: "Application crashes on RHEL 9.2"
├─ Similar cases: 3 in last 30 days
├─ Impact: High (production down)
├─ Workaround: None
└─ 💡 Recommendation: Convert to RFE
    Suggested title: "Fix crash in libfoo on RHEL 9.2"
    Similar RFEs: RHEL-11222, RHEL-11333
```

### 3. **Customer Health Scoring**
AI-powered health metrics based on case patterns.

```
Health Score: 72/100

Factors:
✅ Good: Cases resolved quickly (avg 3.2 days)
✅ Good: No critical severity cases
⚠️  Concern: Same issue recurring (3 times)
⚠️  Concern: No proactive contact in 14 days
❌ Bad: Case 03245678 aging (5 days, no update)
```

### 4. **Escalation Prediction**
AI predicts which cases might escalate.

```
⚠️  Case 03245678 - 85% escalation risk

Indicators:
• Age: 5 days without resolution
• Customer: Previous escalations (2 in Q3)
• Severity: High (production impact)
• Pattern: Similar to escalated case 03123456

Recommended actions:
1. Update customer today (overdue)
2. Engage senior support
3. Consider temporary workaround
```

---

## Architecture Implementation

### 1. RhcaseService (Backend)

```python
# src/taminator/services/rhcase_service.py

import subprocess
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import re

class RhcaseService:
    """
    Wrap rhcase CLI with intelligent caching and parsing
    
    Converts CLI output to structured data for AI analysis
    """
    
    def __init__(self):
        self._cache = {}
        self._cache_ttl = timedelta(minutes=5)
        logger.info("📋 RhcaseService initialized")
    
    async def list_cases(
        self,
        customer_account: str,
        status: str = "open",
        force_refresh: bool = False
    ) -> List[Dict]:
        """
        Get cases for customer account
        
        Args:
            customer_account: Red Hat account number
            status: Case status filter (open, closed, all)
            force_refresh: Skip cache and fetch fresh data
            
        Returns:
            List of structured case data
        """
        cache_key = f"cases_{customer_account}_{status}"
        
        # Check cache
        if not force_refresh and cache_key in self._cache:
            cached_data, cached_time = self._cache[cache_key]
            if datetime.now() - cached_time < self._cache_ttl:
                logger.debug(f"✅ Returning {len(cached_data)} cases from cache")
                return cached_data
        
        # Execute rhcase command
        logger.info(f"🔍 Fetching cases for account {customer_account}")
        
        try:
            result = subprocess.run(
                [
                    'rhcase',
                    'list',
                    '--account', customer_account,
                    '--status', status,
                    '--format', 'json'  # If rhcase supports it
                ],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                raise Exception(f"rhcase failed: {result.stderr}")
            
            # Parse output to structured format
            cases = self._parse_case_list(result.stdout)
            
            # Cache results
            self._cache[cache_key] = (cases, datetime.now())
            
            logger.info(f"✅ Fetched {len(cases)} cases")
            return cases
            
        except subprocess.TimeoutExpired:
            raise Exception("rhcase command timed out")
        except Exception as e:
            logger.error(f"❌ Failed to fetch cases: {e}")
            raise
    
    async def get_case_details(self, case_id: str) -> Dict:
        """
        Get detailed information for a specific case
        
        Args:
            case_id: Case number (e.g., "03245678")
            
        Returns:
            Structured case details
        """
        logger.info(f"🔍 Fetching details for case {case_id}")
        
        try:
            result = subprocess.run(
                ['rhcase', 'get', case_id],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                raise Exception(f"rhcase failed: {result.stderr}")
            
            # Parse case details
            case = self._parse_case_details(result.stdout)
            
            return case
            
        except Exception as e:
            logger.error(f"❌ Failed to get case {case_id}: {e}")
            raise
    
    def _parse_case_list(self, output: str) -> List[Dict]:
        """
        Parse rhcase list output to structured data
        
        Handles both JSON and text output formats
        """
        # Try JSON first
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            pass
        
        # Fallback: Parse text output
        cases = []
        lines = output.strip().split('\n')
        
        for line in lines:
            # Example format: "03245678  High  Open  Performance issue"
            match = re.match(
                r'(\d{8})\s+(\w+)\s+(\w+)\s+(.+)',
                line
            )
            if match:
                case_id, severity, status, summary = match.groups()
                cases.append({
                    'case_id': case_id,
                    'severity': severity,
                    'status': status,
                    'summary': summary.strip(),
                    'fetched_at': datetime.now().isoformat()
                })
        
        return cases
    
    def _parse_case_details(self, output: str) -> Dict:
        """
        Parse detailed case information
        """
        # Parse key-value pairs from rhcase output
        details = {}
        current_field = None
        
        for line in output.split('\n'):
            # Field: Value format
            if ':' in line and not line.startswith(' '):
                key, value = line.split(':', 1)
                current_field = key.strip().lower().replace(' ', '_')
                details[current_field] = value.strip()
            # Continuation of previous field
            elif current_field and line.startswith(' '):
                details[current_field] += ' ' + line.strip()
        
        return details
    
    async def search_cases(
        self,
        query: str,
        customer_account: Optional[str] = None
    ) -> List[Dict]:
        """
        Search cases by keyword
        
        Args:
            query: Search query
            customer_account: Optional account filter
            
        Returns:
            Matching cases
        """
        cmd = ['rhcase', 'search', '--query', query]
        
        if customer_account:
            cmd.extend(['--account', customer_account])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            raise Exception(f"rhcase search failed: {result.stderr}")
        
        return self._parse_case_list(result.stdout)


# Singleton
_rhcase_service: Optional[RhcaseService] = None

def get_rhcase_service() -> RhcaseService:
    global _rhcase_service
    if _rhcase_service is None:
        _rhcase_service = RhcaseService()
    return _rhcase_service
```

### 2. Case Intelligence Service (AI-Powered)

```python
# src/taminator/services/case_intelligence_service.py

from typing import List, Dict
from ..services.rhcase_service import RhcaseService
from ..services.ai_service import AIService

class CaseIntelligenceService:
    """
    AI-powered case analysis and insights
    
    Transforms raw case data into actionable intelligence
    """
    
    def __init__(
        self,
        rhcase_service: RhcaseService,
        ai_service: AIService
    ):
        self.rhcase = rhcase_service
        self.ai = ai_service
    
    async def analyze_customer_cases(
        self,
        customer_id: str,
        account_number: str
    ) -> Dict:
        """
        Complete case intelligence analysis for customer
        
        Returns:
            {
                'health_score': 72,
                'hot_issues': [...],
                'trends': {...},
                'recommendations': [...]
            }
        """
        # Fetch case data
        cases = await self.rhcase.list_cases(account_number)
        
        # Run parallel analysis
        health_score = await self._calculate_health_score(cases)
        hot_issues = await self._identify_hot_issues(cases)
        trends = await self._analyze_trends(cases, customer_id)
        recommendations = await self._generate_recommendations(
            customer_id, cases, hot_issues, trends
        )
        
        return {
            'health_score': health_score,
            'hot_issues': hot_issues,
            'trends': trends,
            'recommendations': recommendations,
            'total_cases': len(cases),
            'analyzed_at': datetime.now().isoformat()
        }
    
    async def _calculate_health_score(self, cases: List[Dict]) -> int:
        """
        Calculate customer health score (0-100)
        
        Factors:
        - Case age
        - Severity distribution
        - Resolution time
        - Recurring issues
        """
        if not cases:
            return 100  # No cases = healthy
        
        score = 100
        
        # Penalize old cases
        for case in cases:
            age_days = self._get_case_age_days(case)
            if age_days > 7:
                score -= 5
            elif age_days > 14:
                score -= 10
        
        # Penalize high severity cases
        critical_count = sum(
            1 for c in cases if c.get('severity') == 'Critical'
        )
        score -= critical_count * 10
        
        # Cap at 0-100
        return max(0, min(100, score))
    
    async def _identify_hot_issues(self, cases: List[Dict]) -> List[Dict]:
        """
        Identify cases needing immediate attention
        
        Criteria:
        - High/Critical severity
        - Aging cases (>5 days)
        - Potential escalation risk
        """
        hot = []
        
        for case in cases:
            age_days = self._get_case_age_days(case)
            severity = case.get('severity', 'Low')
            
            # Hot if: Critical OR (High + old)
            is_hot = (
                severity == 'Critical' or
                (severity == 'High' and age_days > 5)
            )
            
            if is_hot:
                # Add AI context
                context = await self._get_case_context(case)
                hot.append({
                    **case,
                    'age_days': age_days,
                    'escalation_risk': self._predict_escalation_risk(case),
                    'similar_cases': context.get('similar_cases', []),
                    'recommended_action': context.get('action')
                })
        
        return sorted(hot, key=lambda x: x['escalation_risk'], reverse=True)
    
    async def _analyze_trends(
        self,
        cases: List[Dict],
        customer_id: str
    ) -> Dict:
        """
        Analyze case trends using AI
        
        Returns insights like:
        - Case volume changes
        - Common issues
        - Performance metrics
        """
        # Build prompt with case data
        prompt = self._build_trend_analysis_prompt(cases)
        
        # Get AI analysis
        insights = await self.ai.analyze_text(
            prompt=prompt,
            model="gpt-4",
            response_format="json"
        )
        
        return insights
    
    async def _generate_recommendations(
        self,
        customer_id: str,
        cases: List[Dict],
        hot_issues: List[Dict],
        trends: Dict
    ) -> List[Dict]:
        """
        AI-powered recommendations for TAM actions
        """
        # Build context
        context = {
            'total_cases': len(cases),
            'hot_issues_count': len(hot_issues),
            'trends': trends
        }
        
        # Get AI recommendations
        prompt = f"""
        Analyze this customer's case situation and recommend specific TAM actions:
        
        Context:
        {json.dumps(context, indent=2)}
        
        Provide 3-5 specific, actionable recommendations.
        Format as JSON array with: action, priority, reason
        """
        
        recommendations = await self.ai.complete(
            prompt=prompt,
            model="gpt-4",
            response_format="json"
        )
        
        return recommendations
    
    async def correlate_case_to_rfe(self, case_id: str) -> Dict:
        """
        Suggest if case should become RFE
        
        Uses AI to analyze:
        - Is this a bug or enhancement?
        - How many similar cases exist?
        - What's the business impact?
        - Are there existing RFEs?
        """
        # Get case details
        case = await self.rhcase.get_case_details(case_id)
        
        # Search for similar cases
        similar = await self.rhcase.search_cases(
            query=case['summary'][:50]  # Use summary keywords
        )
        
        # AI analysis
        prompt = f"""
        Analyze if this case should be converted to an RFE:
        
        Case: {case['summary']}
        Severity: {case.get('severity')}
        Similar cases: {len(similar)}
        
        Determine:
        1. Is this a product enhancement request?
        2. Does it affect multiple customers?
        3. Is there a workaround?
        4. Should we create an RFE?
        
        Return JSON with: should_create_rfe (bool), confidence (0-1), reasoning
        """
        
        analysis = await self.ai.complete(
            prompt=prompt,
            model="gpt-4",
            response_format="json"
        )
        
        return {
            'case_id': case_id,
            'should_create_rfe': analysis['should_create_rfe'],
            'confidence': analysis['confidence'],
            'reasoning': analysis['reasoning'],
            'similar_cases': similar[:5],  # Top 5
            'suggested_rfe_title': self._suggest_rfe_title(case)
        }
    
    def _predict_escalation_risk(self, case: Dict) -> float:
        """
        Predict escalation probability (0-1)
        
        Simple ML model based on:
        - Case age
        - Severity
        - Update frequency
        - Customer history
        """
        risk = 0.0
        
        # Age factor
        age_days = self._get_case_age_days(case)
        if age_days > 5:
            risk += 0.3
        if age_days > 10:
            risk += 0.3
        
        # Severity factor
        severity = case.get('severity', 'Low')
        if severity == 'Critical':
            risk += 0.4
        elif severity == 'High':
            risk += 0.2
        
        return min(1.0, risk)
    
    def _get_case_age_days(self, case: Dict) -> int:
        """Calculate case age in days"""
        # Parse created date from case
        # Simplified - real implementation would parse actual date
        return 3  # Placeholder
    
    def _suggest_rfe_title(self, case: Dict) -> str:
        """Generate RFE title from case"""
        summary = case.get('summary', '')
        # Clean up and format
        return f"RFE: {summary[:80]}"


# Singleton
_case_intelligence_service: Optional[CaseIntelligenceService] = None

def get_case_intelligence_service() -> CaseIntelligenceService:
    global _case_intelligence_service
    if _case_intelligence_service is None:
        _case_intelligence_service = CaseIntelligenceService(
            rhcase_service=get_rhcase_service(),
            ai_service=get_ai_service()
        )
    return _case_intelligence_service
```

### 3. API Endpoints

```python
# src/taminator/api/routes/cases.py

from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/api/cases", tags=["cases"])

@router.get("/{customer_id}/intelligence")
async def get_case_intelligence(
    customer_id: str,
    intelligence: CaseIntelligenceService = Depends(get_case_intelligence_service),
    customer_service: CustomerService = Depends(get_customer_service)
):
    """
    Get AI-powered case intelligence for customer
    
    Returns:
        - Health score
        - Hot issues
        - Trends
        - Recommendations
    """
    # Get customer account number
    customer = await customer_service.get_customer(customer_id)
    
    # Run intelligence analysis
    analysis = await intelligence.analyze_customer_cases(
        customer_id=customer_id,
        account_number=customer.account_number
    )
    
    return analysis

@router.get("/{customer_id}/cases")
async def list_customer_cases(
    customer_id: str,
    status: str = "open",
    rhcase: RhcaseService = Depends(get_rhcase_service),
    customer_service: CustomerService = Depends(get_customer_service)
):
    """
    Get list of cases for customer
    """
    customer = await customer_service.get_customer(customer_id)
    cases = await rhcase.list_cases(customer.account_number, status)
    return {"cases": cases}

@router.get("/case/{case_id}/details")
async def get_case_details(
    case_id: str,
    rhcase: RhcaseService = Depends(get_rhcase_service)
):
    """
    Get detailed case information
    """
    details = await rhcase.get_case_details(case_id)
    return details

@router.post("/case/{case_id}/analyze-for-rfe")
async def analyze_case_for_rfe(
    case_id: str,
    intelligence: CaseIntelligenceService = Depends(get_case_intelligence_service)
):
    """
    Analyze if case should become RFE
    
    AI-powered analysis of:
    - Enhancement vs bug
    - Impact scope
    - Similar cases
    - RFE recommendation
    """
    analysis = await intelligence.correlate_case_to_rfe(case_id)
    return analysis

@router.get("/{customer_id}/health-score")
async def get_customer_health_score(
    customer_id: str,
    intelligence: CaseIntelligenceService = Depends(get_case_intelligence_service),
    customer_service: CustomerService = Depends(get_customer_service)
):
    """
    Get AI-calculated customer health score
    """
    customer = await customer_service.get_customer(customer_id)
    cases = await rhcase.list_cases(customer.account_number)
    
    score = await intelligence._calculate_health_score(cases)
    
    return {
        "customer_id": customer_id,
        "health_score": score,
        "total_cases": len(cases)
    }
```

### 4. GUI Integration

```javascript
// gui/index.html - Case Intelligence Tab

async function loadCaseIntelligence(customerId) {
    showLoading('Analyzing cases with AI...');
    
    try {
        const intel = await taminatorAPI.cases.getIntelligence(customerId);
        
        // Display health score
        displayHealthScore(intel.health_score);
        
        // Show hot issues
        displayHotIssues(intel.hot_issues);
        
        // Show trends
        displayTrends(intel.trends);
        
        // Show AI recommendations
        displayRecommendations(intel.recommendations);
        
    } catch (error) {
        handleAPIError(error);
    }
}

function displayHealthScore(score) {
    const color = score > 80 ? 'green' : score > 60 ? 'yellow' : 'red';
    const emoji = score > 80 ? '✅' : score > 60 ? '⚠️' : '❌';
    
    document.getElementById('health-score').innerHTML = `
        <div class="health-score ${color}">
            <span class="emoji">${emoji}</span>
            <span class="score">${score}/100</span>
            <div class="progress-bar">
                <div class="progress" style="width: ${score}%"></div>
            </div>
        </div>
    `;
}

function displayHotIssues(issues) {
    const html = issues.map(issue => `
        <div class="hot-issue">
            <div class="case-id">${issue.case_id}</div>
            <div class="summary">${issue.summary}</div>
            <div class="age">Age: ${issue.age_days} days</div>
            <div class="risk">
                Escalation Risk: ${(issue.escalation_risk * 100).toFixed(0)}%
            </div>
            ${issue.similar_cases.length > 0 ? `
                <div class="context">
                    💡 Similar to ${issue.similar_cases.length} other cases
                </div>
            ` : ''}
            <button onclick="viewCase('${issue.case_id}')">View Details</button>
        </div>
    `).join('');
    
    document.getElementById('hot-issues').innerHTML = html;
}

async function analyzeCaseForRFE(caseId) {
    showLoading('AI analyzing case...');
    
    const analysis = await taminatorAPI.cases.analyzeForRFE(caseId);
    
    if (analysis.should_create_rfe) {
        showRFERecommendation(analysis);
    } else {
        showAlert('AI recommends keeping this as a support case');
    }
}

function showRFERecommendation(analysis) {
    const html = `
        <div class="rfe-recommendation">
            <h3>💡 RFE Recommendation</h3>
            <p><strong>Confidence:</strong> ${(analysis.confidence * 100).toFixed(0)}%</p>
            <p><strong>Reasoning:</strong> ${analysis.reasoning}</p>
            <p><strong>Suggested Title:</strong> ${analysis.suggested_rfe_title}</p>
            
            ${analysis.similar_cases.length > 0 ? `
                <p><strong>Similar Cases:</strong></p>
                <ul>
                    ${analysis.similar_cases.map(c => 
                        `<li>${c.case_id}: ${c.summary}</li>`
                    ).join('')}
                </ul>
            ` : ''}
            
            <button onclick="createRFEFromCase('${analysis.case_id}')">
                Create RFE
            </button>
            <button onclick="dismissRecommendation()">Not Now</button>
        </div>
    `;
    
    showModal(html);
}
```

---

## Key Features

### 1. **Automated Pattern Detection**
```
AI detects:
- "3 cases about performance in last 30 days"
- "Similar to resolved case 03123456"
- "Recurring issue - consider RFE"
```

### 2. **Smart Prioritization**
```
Case Priority Score = f(
    severity,
    age,
    customer_history,
    business_impact,
    escalation_risk
)
```

### 3. **Proactive Recommendations**
```
💡 AI suggests:
- "Create RFE - 3 customers affected"
- "Schedule call - no contact 14 days"
- "Update case - customer expecting response"
```

### 4. **Case-to-RFE Intelligence**
```
AI determines:
- Is this an enhancement request?
- How many customers affected?
- Existing RFEs similar?
- Recommend: YES/NO + confidence
```

---

## Benefits

| Feature | Before (Yugo) | After (Tesla) |
|---------|---------------|---------------|
| **Case List** | Raw rhcase output | Intelligent dashboard |
| **Pattern Detection** | Manual | AI-powered automatic |
| **Priority** | Manual sorting | AI scoring |
| **RFE Correlation** | Manual guess | AI recommendation |
| **Customer Health** | Gut feeling | Data-driven score |
| **Time to Insight** | Hours | Seconds |

---

## Implementation Timeline

### Week 1: Foundation
- Day 1-2: RhcaseService (wrap CLI)
- Day 3-4: Basic intelligence (health score)
- Day 5: API endpoints

### Week 2: AI Intelligence
- Day 1-2: Pattern detection
- Day 3-4: Case-to-RFE correlation
- Day 5: Escalation prediction

### Week 3: GUI Integration
- Day 1-2: Intelligence dashboard
- Day 3-4: Hot issues panel
- Day 5: Testing and refinement

---

## Red Hat Compliance

**rhcase data classification:** Internal  
**Approved AI models:** GPT-4, Granite  
**No customer PII** in AI prompts

---

**This is the Tesla way to do rhcase intelligence.**

Want me to implement the RhcaseService foundation right now?



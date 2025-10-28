# AI Integration - Tesla Architecture

## Vision: AI-Powered TAM Assistant

Instead of manually writing emails, analyzing reports, and tracking action items - **AI does the heavy lifting**.

---

## Implementation Strategy

### Phase 1: Foundation (Week 1)
1. **LiteLLM Integration** - Red Hat compliant proxy
2. **AI Service Layer** - Business logic for AI features
3. **Streaming Support** - WebSocket for real-time responses
4. **Context Management** - Customer data RAG

### Phase 2: Features (Week 2-3)
1. **Email Composer** - Generate RFE update emails
2. **Report Analyzer** - Trend analysis and insights
3. **Smart Suggestions** - Next actions recommendations

### Phase 3: Advanced (Week 4+)
1. **Meeting Notes Parser** - Extract action items
2. **Auto-Categorization** - RFE vs Bug classification
3. **Predictive Analytics** - Forecast RFE completion

---

## Code Architecture

### 1. AI Service (Backend)

```python
# src/taminator/services/ai_service.py

from litellm import completion, acompletion
import asyncio
from typing import AsyncIterator

class AIService:
    def __init__(self, litellm_proxy_url: str = "http://localhost:4000"):
        self.proxy_url = litellm_proxy_url
        self.customer_service = get_customer_service()
    
    async def compose_email(
        self,
        customer_id: str,
        template: str = "rfe_update",
        tone: str = "professional",
        stream: bool = True
    ) -> AsyncIterator[str]:
        """
        Generate customer update email with AI
        
        Streams response for real-time UI updates
        """
        # Get customer context
        customer = await self.customer_service.get_customer(customer_id)
        rfes = await self._get_recent_rfe_changes(customer_id)
        
        # Build prompt with context
        prompt = self._build_email_prompt(customer, rfes, template, tone)
        
        # Stream AI response
        response = await acompletion(
            model="gpt-4",  # or "granite" for customer data
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            stream=stream,
            api_base=self.proxy_url
        )
        
        # Yield chunks for streaming
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    async def analyze_report(
        self,
        customer_id: str,
        timeframe: str = "last_3_months"
    ) -> dict:
        """
        Analyze customer report trends
        
        Returns insights and recommendations
        """
        # Get historical data
        reports = await self._get_report_history(customer_id, timeframe)
        
        # Analyze with AI
        prompt = f"""
        Analyze these TAM reports and provide insights:
        
        {reports}
        
        Provide:
        1. Key trends
        2. Issues needing attention
        3. Recommendations for TAM
        """
        
        response = await acompletion(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a TAM analytics assistant."},
                {"role": "user", "content": prompt}
            ],
            api_base=self.proxy_url
        )
        
        return self._parse_insights(response.choices[0].message.content)
    
    async def suggest_actions(self, customer_id: str) -> list:
        """
        Suggest next actions for TAM based on customer state
        """
        customer = await self.customer_service.get_customer(customer_id)
        stats = await self.customer_service.get_stats(customer_id)
        
        prompt = f"""
        Customer: {customer.name}
        Open RFEs: {stats.total_rfes}
        Open Bugs: {stats.total_bugs}
        Last update: {stats.last_checked}
        
        Suggest 3-5 specific actions the TAM should take.
        Format as JSON array with: action, priority, reason
        """
        
        response = await acompletion(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            api_base=self.proxy_url
        )
        
        return json.loads(response.choices[0].message.content)
    
    def _get_system_prompt(self) -> str:
        return """
        You are a Technical Account Manager (TAM) assistant for Red Hat.
        You help write professional customer communications.
        
        Guidelines:
        - Professional but friendly tone
        - Technical accuracy is critical
        - Always include action items
        - Reference specific JIRA IDs
        - Clear next steps
        """
    
    def _build_email_prompt(
        self,
        customer: Customer,
        rfes: list,
        template: str,
        tone: str
    ) -> str:
        return f"""
        Write an email update for {customer.name} about their RFE status.
        
        Recent changes:
        {self._format_rfe_changes(rfes)}
        
        Template: {template}
        Tone: {tone}
        
        Include:
        1. Brief greeting
        2. Status updates for each RFE
        3. Next steps
        4. Offer to discuss
        """
```

### 2. AI API Endpoints (FastAPI)

```python
# src/taminator/api/routes/ai.py

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from typing import AsyncIterator

router = APIRouter(prefix="/api/ai", tags=["ai"])

@router.post("/{customer_id}/compose-email")
async def compose_email(
    customer_id: str,
    request: EmailComposeRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Generate customer email with AI
    
    Streams response for real-time UI updates
    """
    
    async def generate():
        async for chunk in ai_service.compose_email(
            customer_id=customer_id,
            template=request.template,
            tone=request.tone,
            stream=True
        ):
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )

@router.post("/{customer_id}/analyze")
async def analyze_report(
    customer_id: str,
    request: AnalyzeRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Analyze customer reports and provide insights
    """
    insights = await ai_service.analyze_report(
        customer_id=customer_id,
        timeframe=request.timeframe
    )
    return insights

@router.get("/{customer_id}/suggestions")
async def get_suggestions(
    customer_id: str,
    ai_service: AIService = Depends(get_ai_service)
):
    """
    Get AI-powered action suggestions
    """
    actions = await ai_service.suggest_actions(customer_id)
    return {"suggestions": actions}
```

### 3. GUI Integration (JavaScript)

```javascript
// gui/index.html - AI Email Composer

async function composeEmailWithAI(customerId) {
    const container = document.getElementById('email-content');
    container.innerHTML = '<div class="ai-composing">✨ AI is composing...</div>';
    
    try {
        // Connect to streaming endpoint
        const response = await fetch(
            `http://localhost:8765/api/ai/${customerId}/compose-email`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    template: 'rfe_update',
                    tone: 'professional'
                })
            }
        );
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let email = '';
        
        // Stream response chunks
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));
                    email += data.chunk;
                    
                    // Update UI in real-time
                    container.innerHTML = marked.parse(email);
                }
            }
        }
        
        // Show edit/send buttons
        showEmailActions(email);
        
    } catch (error) {
        showError('AI composition failed: ' + error.message);
    }
}

// AI Dashboard Insights
async function loadAIInsights(customerId) {
    const insights = await taminatorAPI.ai.analyze(customerId, {
        timeframe: 'last_3_months'
    });
    
    displayInsights(insights);
}

// AI Suggestions Panel
async function loadAISuggestions(customerId) {
    const suggestions = await taminatorAPI.ai.getSuggestions(customerId);
    
    const html = suggestions.map(s => `
        <div class="ai-suggestion ${s.priority}">
            <span class="icon">${getPriorityIcon(s.priority)}</span>
            <span class="action">${s.action}</span>
            <span class="reason">${s.reason}</span>
        </div>
    `).join('');
    
    document.getElementById('ai-suggestions').innerHTML = html;
}
```

---

## Red Hat Compliance (MANDATORY)

### Model Selection by Data Type

```python
def get_compliant_model(data_type: str) -> str:
    """
    Red Hat AI policy compliance
    """
    if data_type == "customer_data":
        return "granite"  # Red Hat Granite models ONLY
    elif data_type == "internal_data":
        return "gpt-4"  # AIA-approved models
    elif data_type == "public_data":
        return "llama"  # Open source fallback
    else:
        raise ComplianceError("Unknown data type")
```

### LiteLLM Configuration

```yaml
# litellm_config.yaml
model_list:
  - model_name: granite
    litellm_params:
      model: bedrock/granite-v1
      api_key: ${GRANITE_API_KEY}
  
  - model_name: gpt-4
    litellm_params:
      model: azure/gpt-4
      api_key: ${AZURE_API_KEY}
  
  - model_name: llama
    litellm_params:
      model: ollama/llama3
      api_base: http://localhost:11434
```

---

## UI Examples

### 1. AI Email Composer

```
┌─────────────────────────────────────────────────────────────┐
│ ✉️  Compose Email - ACME Corporation                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Template: [RFE Update ▼]  Tone: [Professional ▼]          │
│                                                              │
│  [✨ Generate with AI]  [📝 Write Manually]                 │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ ✨ AI is composing your email...                       │ │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 65%                │ │
│  │                                                         │ │
│  │ Dear ACME Team,                                        │ │
│  │                                                         │ │
│  │ I wanted to provide you with an update on your        │ │
│  │ open RFE requests:                                     │ │
│  │                                                         │ │
│  │ **RHEL-12345** - Enhanced Container Support           │ │
│  │ Status changed: In Progress → Code Review             │ │
│  │ Engineering has completed the initial implementation   │ │
│  │ and it's now under review. Expected completion: Q4.   │ │
│  │                                                         │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  [📋 Copy to Clipboard]  [✏️  Edit]  [📤 Send]              │
└─────────────────────────────────────────────────────────────┘
```

### 2. AI Dashboard Insights

```
┌─────────────────────────────────────────────────────────────┐
│ 🤖 AI Insights - ACME Corporation                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📊 Trend Analysis (Last 3 Months)                          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │
│                                                              │
│  ✅ Positive Trends:                                         │
│   • Bug resolution time improved 40%                        │
│   • 3 RFEs moved to Code Review                            │
│   • Customer engagement increased (4 meetings)              │
│                                                              │
│  ⚠️  Areas of Concern:                                       │
│   • RHEL-11111 stuck in Backlog for 120 days               │
│   • No portal updates in 45 days (recommend posting)        │
│   • 2 RFEs need customer validation                        │
│                                                              │
│  💡 Recommended Actions:                                     │
│   1. Follow up on RHEL-11111 prioritization                │
│   2. Post quarterly update to customer portal              │
│   3. Schedule validation meeting for Q4 RFEs               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 3. AI Suggestions Panel

```
┌─────────────────────────────────────────────────────────────┐
│ 💡 Smart Suggestions                                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🔴 High Priority                                            │
│  Check RHEL-12345 - No updates in 30 days                   │
│  → Engineering may need reminder                            │
│                                                              │
│  🟡 Medium Priority                                          │
│  Post quarterly update to portal                            │
│  → Last post was 45 days ago                                │
│                                                              │
│  🟢 Low Priority                                             │
│  Schedule customer sync for Q4 planning                     │
│  → Good time to discuss upcoming RFEs                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Benefits: Yugo vs Tesla

| Feature | Yugo (Old) | Tesla (New) |
|---------|------------|-------------|
| **Email Generation** | Manual | AI-generated in 5 seconds |
| **Report Analysis** | Manual Excel | AI insights automatically |
| **Action Items** | Manual tracking | AI suggests next steps |
| **Streaming UI** | ❌ | ✅ Real-time typing effect |
| **Context Awareness** | ❌ | ✅ Remembers conversation |
| **Red Hat Compliance** | ❌ | ✅ Granite for customer data |
| **Cost** | N/A | Optimized with caching |

---

## Implementation Timeline

### Week 1: Foundation
- Day 1-2: LiteLLM proxy setup
- Day 3-4: AI Service implementation
- Day 5: WebSocket streaming support

### Week 2: Email Composer
- Day 1-2: Backend compose endpoint
- Day 3-4: Frontend streaming UI
- Day 5: Testing and refinement

### Week 3: Analytics & Suggestions
- Day 1-2: Report analyzer
- Day 3-4: Smart suggestions
- Day 5: Dashboard integration

---

## Next Steps

1. **Decide on AI provider:**
   - LiteLLM proxy (recommended - Red Hat compliant)
   - Direct Granite API
   - Hybrid approach

2. **Choose first feature:**
   - Email Composer (highest value)
   - Report Analyzer (good demo)
   - Smart Suggestions (quick win)

3. **Set up compliance:**
   - Configure Granite for customer data
   - Set up audit logging
   - Test with sample data

---

## The Vision

**Instead of this (Yugo):**
```
TAM spends 2 hours writing customer update email
TAM manually reviews 50 JIRA tickets for trends
TAM tries to remember all action items
```

**You get this (Tesla):**
```
AI generates email in 5 seconds (TAM reviews/edits)
AI analyzes trends and highlights concerns automatically
AI suggests "Check RHEL-12345 - no updates in 30 days"
```

**Result:**
- 80% time savings on routine communication
- Better insights from data analysis
- Never miss important action items
- More time for strategic TAM work

---

**The Tesla architecture makes AI integration EASY and POWERFUL.**

Want me to implement the AI email composer as a proof of concept?



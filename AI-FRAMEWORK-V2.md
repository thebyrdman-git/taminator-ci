# Taminator v2.0 - AI Framework (Critical)

**Core Principle**: AI is the differentiator. Generic tools exist. AI-powered TAM assistance is what makes this worth using.

**Status**: MUST GET RIGHT before v2.0 ships.

---

## 🎯 Why AI Framework is Critical

### The Problem
TAMs spend hours on repetitive communication:
- Writing RFE reports with proper formatting
- Drafting customer update emails
- Explaining technical issues in business terms
- Summarizing JIRA issues for non-technical stakeholders

### The AI Solution
**"Clippy, but actually useful."**

- Paste customer email → Get professional TAM response draft
- Paste case notes → Get Portal-ready report
- Paste JIRA issues → Get executive summary
- Paste technical details → Get customer-friendly explanation

### The Value Proposition
**"Taminator writes the first draft. You review and send."**

- Save 15-20 minutes per email
- Consistent professional tone
- No more staring at blank email wondering what to say
- Focus on thinking, not typing

---

## 🏗️ AI Framework Architecture

### Layer 1: AI Client (Infrastructure)
**File**: `src/taminator/core/ai_client.py`

**Responsibilities**:
- Connect to LiteLLM proxy (localhost or rhgrimm)
- Manage model selection (Red Hat approved only)
- Handle rate limiting and errors
- Provide health checks
- Cache model availability

**Key Features**:
- ✅ Automatic proxy detection
- ✅ Model validation (Granite only in production)
- ✅ Graceful degradation (tool works without AI)
- ✅ Error handling with clear messages
- ✅ Performance monitoring

**Quality Bar**:
- Must connect in <2 seconds
- Must fail gracefully if unavailable
- Must provide clear status to user
- Must support multiple models (easy to switch)

---

### Layer 2: AI Services (Features)
**Files**: 
- `src/taminator/core/gmail_assistant.py` (Email drafting)
- `src/taminator/services/rfe_generator.py` (RFE reports) - TODO
- `src/taminator/services/summary_generator.py` (Executive summaries) - TODO

**Responsibilities**:
- Use AIClient for generation
- Implement domain-specific prompts
- Handle context detection
- Provide fallback templates
- Validate output quality

**Key Features**:
- ✅ Context-aware (detects RFE vs Bug vs Customer Update)
- ✅ Template fallback (no AI required)
- ✅ Professional tone enforcement
- ✅ Red Hat branding (signatures, style)
- ✅ User control (preview before send)

---

### Layer 3: API Routes (Integration)
**Files**: `src/taminator/api/routes/gmail_assistant.py`

**Responsibilities**:
- Expose AI features via REST API
- Handle async operations
- Provide status endpoints
- Stream responses (for long generations)
- Error handling

---

### Layer 4: GUI (User Interface)
**Files**: `gui/clippy-gmail-assistant.html`

**Responsibilities**:
- Clipboard integration
- Real-time preview
- Edit before save
- Status indicators
- Error messages

---

## 🎨 Prompt Engineering (THE CRITICAL PART)

### Why Prompts Matter
**Bad prompt → Bad output → User abandons tool.**

A poorly crafted email reflects on the TAM, not the AI. If Clippy generates something unprofessional, users will never trust it again.

### Prompt Quality Requirements

#### 1. Professional Tone (MANDATORY)
```
✅ GOOD: "I wanted to follow up on the RFE we discussed..."
❌ BAD: "Hey! So about that thing..."
```

**Test**: Would you send this to a customer without editing? If no, prompt is wrong.

---

#### 2. Context Awareness (MANDATORY)
```
Prompt must include:
- Email type (RFE update, bug report, customer response)
- Customer name (if available)
- JIRA issue keys (if present)
- Urgency level
- Expected tone (friendly-professional, urgent, informative)
```

**Test**: Does output reference correct customer and issues? If no, prompt is wrong.

---

#### 3. Actionable Content (MANDATORY)
```
✅ GOOD: "Next steps: I'll update RHEL-12345 with your feedback and follow up by Friday."
❌ BAD: "Let me know if you need anything."
```

**Test**: Does email have clear next steps? If no, prompt is wrong.

---

#### 4. Length Control (MANDATORY)
```
✅ GOOD: 3-5 paragraphs (200-400 words)
❌ BAD: 1 sentence or 10 paragraphs
```

**Test**: Can you read it in <2 minutes? If no, prompt is wrong.

---

#### 5. Technical Accuracy (CRITICAL)
```
✅ GOOD: Uses correct RHEL version, product names, issue keys
❌ BAD: Hallucinates features, wrong version numbers
```

**Test**: Are all facts verifiable? If no, prompt is wrong.

---

### Current Prompt Template (GmailAssistant)

**Location**: `src/taminator/core/gmail_assistant.py` → `_build_draft_prompt()`

**Review Required**:
```python
def _build_draft_prompt(self, content, context, template):
    prompt = f"""You are a professional Red Hat Technical Account Manager (TAM) writing an email.

CONTEXT:
- Email Type: {context['type']}
- Customer: {context.get('customer', 'N/A')}
- JIRA Issues: {', '.join(context.get('issue_keys', []))}
- Urgency: {context['urgency']}
- Tone: {template['tone']}
- Style: {template['style']}

SOURCE CONTENT (from clipboard):
{content}

TASK:
Generate a professional email draft with:
1. Clear, concise subject line
2. Professional greeting
3. Main content based on source material
4. Call to action (if appropriate)
5. Professional closing

OUTPUT FORMAT:
SUBJECT: [subject line]

BODY:
[email body - 3-5 paragraphs]

GUIDELINES:
- Use professional TAM voice
- Be clear and concise
- Include relevant JIRA links if applicable
- Match the specified tone and style
- Do NOT include signature (added separately)
"""
    return prompt
```

**Issues to Fix**:
1. ⚠️ **Lacks examples** - AI performs better with few-shot examples
2. ⚠️ **No anti-hallucination guardrails** - Needs "ONLY use facts from SOURCE CONTENT"
3. ⚠️ **No length constraint** - Should specify "3-5 paragraphs, 200-400 words"
4. ⚠️ **No tone examples** - What does "professional TAM voice" sound like?
5. ⚠️ **No Red Hat style guide** - Should reference specific phrasing

---

### Improved Prompt Template (v2.0)

```python
def _build_draft_prompt(self, content, context, template):
    """
    Build AI prompt for email draft generation
    
    Quality Requirements:
    - Professional TAM tone
    - 3-5 paragraphs (200-400 words)
    - Fact-based (no hallucination)
    - Actionable next steps
    - Context-aware
    """
    
    # Few-shot examples for better quality
    examples = self._get_prompt_examples(context['type'])
    
    prompt = f"""You are a professional Red Hat Technical Account Manager (TAM).
Your job is to write clear, helpful, professional emails to customers.

## YOUR IDENTITY
- Name: (will be added via signature)
- Role: Senior Technical Account Manager at Red Hat
- Expertise: RHEL, OpenShift, Ansible, enterprise support
- Communication style: Professional, clear, helpful, technical but accessible

## CURRENT TASK
Email Type: {context['type']}
Customer: {context.get('customer', 'N/A')}
Related Issues: {', '.join(context.get('issue_keys', []))}
Urgency: {context['urgency']}
Expected Tone: {template['tone']}

## SOURCE MATERIAL (from clipboard)
{content}

## EXAMPLES OF GOOD TAM EMAILS
{examples}

## YOUR TASK
Generate a professional email draft following this structure:

1. **Subject Line** (clear, specific, includes issue key if relevant)
2. **Greeting** (professional: "Hi [Name]," or "Hello,")
3. **Context/Opening** (1 sentence: why you're emailing)
4. **Main Content** (2-3 paragraphs: key information)
5. **Next Steps** (1 paragraph: what happens next, timeline)
6. **Closing** (professional: "Please let me know..." or "I'll follow up...")

## CRITICAL RULES
1. ✅ ONLY use facts from SOURCE MATERIAL - DO NOT invent details
2. ✅ Keep it concise: 3-5 paragraphs, 200-400 words total
3. ✅ Include JIRA issue keys where relevant (format: RHEL-12345)
4. ✅ Use Red Hat product names correctly (RHEL, not "Red Hat Linux")
5. ✅ Be specific about timelines ("by Friday" not "soon")
6. ✅ Professional tone - you're representing Red Hat
7. ❌ DO NOT use overly casual language ("Hey!", "Awesome!", etc.)
8. ❌ DO NOT make promises you can't keep
9. ❌ DO NOT include signature (added separately)
10. ❌ DO NOT add information not in SOURCE MATERIAL

## OUTPUT FORMAT
SUBJECT: [One clear, specific subject line]

BODY:
[Professional greeting]

[Opening context - 1 sentence]

[Main content - 2-3 paragraphs]

[Next steps - 1 paragraph with timeline]

[Professional closing]

BEGIN OUTPUT NOW:
"""
    
    return prompt


def _get_prompt_examples(self, email_type: str) -> str:
    """Get few-shot examples for prompt"""
    
    examples = {
        "rfe_update": """
Example:
SUBJECT: RFE Update: RHEL-12345 - Performance Monitoring API

BODY:
Hi Sarah,

I wanted to update you on the RFE we submitted for the performance monitoring API feature.

RHEL-12345 has been reviewed by the product team and accepted for the Q2 2025 roadmap. The engineering team confirmed they can deliver the REST API endpoints you requested for CPU and memory metrics. They've also added network I/O metrics based on similar requests from other enterprise customers.

I'll schedule a design review call with you and the engineering team in the next two weeks to review the API specifications. This will ensure the implementation meets your integration requirements before development begins.

Please let me know your availability for the design review, and feel free to reach out if you have any questions in the meantime.
""",
        
        "bug_report": """
Example:
SUBJECT: Bug Report: RHEL-56789 - SELinux Policy Issue

BODY:
Hi Michael,

I've opened RHEL-56789 to track the SELinux policy issue you reported during our call yesterday.

The bug is currently under investigation by the security team. Based on the logs you provided, this appears to be related to a recent policy update in RHEL 9.3. The team has identified a potential fix and is testing it in their lab environment now.

I'll follow up with you by end of week with either a patch for testing or an updated timeline. In the meantime, the documented workaround (setting SELinux to permissive mode for the affected service) should allow you to proceed with your deployment.

Let me know if you need any additional assistance or if the workaround isn't sufficient for your timeline.
""",
        
        "customer_response": """
Example:
SUBJECT: Re: Question about RHEL 9 Upgrade Timeline

BODY:
Hi Jennifer,

Thanks for reaching out about your RHEL 9 upgrade timeline.

Based on our conversation and your current RHEL 7 environment, I recommend starting with a test cluster upgrade in Q1 2025. This gives us time to address any application compatibility issues before moving production workloads. The RHEL 9 upgrade path from RHEL 7 requires going through RHEL 8 first, so we'll want to plan for two upgrade cycles.

I'll put together a detailed upgrade roadmap with timeline estimates and schedule a planning call for next week. I'll also check if any of your key applications have known compatibility issues we should address upfront.

Does next Tuesday or Wednesday work for a 30-minute planning call?
"""
    }
    
    return examples.get(email_type, examples["customer_response"])
```

---

## 🧪 AI Quality Testing (MANDATORY)

### Before v2.0 Ships, Test:

#### Test 1: Professional Tone
```
Input: Casual customer email
Expected: Professional TAM response (not too casual, not too formal)
Pass Criteria: Would you send this to VP-level customer without editing?
```

#### Test 2: Fact Accuracy
```
Input: Email with specific JIRA keys, customer names, dates
Expected: Output includes ALL facts correctly (no hallucination)
Pass Criteria: Every fact in output traceable to input
```

#### Test 3: Length Control
```
Input: Long technical case notes
Expected: 3-5 paragraph summary (200-400 words)
Pass Criteria: Readable in <2 minutes
```

#### Test 4: Context Detection
```
Input: RFE discussion vs Bug report vs Customer question
Expected: Appropriate tone and structure for each
Pass Criteria: Email type correctly identified and formatted
```

#### Test 5: Graceful Degradation
```
Input: AI unavailable (LiteLLM down)
Expected: Template-based draft (still useful)
Pass Criteria: Tool doesn't crash, generates acceptable fallback
```

#### Test 6: Edge Cases
```
- Empty clipboard
- Non-English content
- Very long input (>10KB)
- HTML content
- Special characters
Pass Criteria: Handles gracefully with clear error messages
```

---

## 🚨 AI Quality Red Flags (Fail v2.0)

If ANY of these occur in testing, DO NOT SHIP:

### Red Flag #1: Hallucination
```
❌ AI invents JIRA keys that don't exist
❌ AI makes up customer names
❌ AI creates fake timelines or promises
❌ AI references features that don't exist
```

**Fix**: Improve prompt with strict "SOURCE MATERIAL ONLY" rules

---

### Red Flag #2: Unprofessional Tone
```
❌ "Hey there! 🎉"
❌ "Awesome news!"
❌ "Yikes, that's a tough one"
❌ Overly casual or informal
```

**Fix**: Add tone examples and Red Hat style guide to prompt

---

### Red Flag #3: Too Vague
```
❌ "I'll get back to you soon"
❌ "Let me know if you need anything"
❌ "We're working on it"
❌ No specific next steps or timeline
```

**Fix**: Require actionable next steps in prompt

---

### Red Flag #4: Too Long
```
❌ 10+ paragraphs
❌ >1000 words
❌ Rambling or repetitive
```

**Fix**: Add strict length constraints to prompt

---

### Red Flag #5: Context Missed
```
❌ Doesn't mention customer name when provided
❌ Ignores JIRA issues in input
❌ Wrong email type (treats bug as RFE)
```

**Fix**: Improve context detection and prompt structure

---

## 📊 AI Performance Targets

### Speed
- ✅ Draft generation: <10 seconds (target: <5 seconds)
- ✅ Context detection: <1 second
- ✅ Model loading: <2 seconds

### Quality
- ✅ Professional tone: 95%+ of outputs (human eval)
- ✅ Fact accuracy: 100% (no hallucination)
- ✅ Length compliance: 90%+ within 200-400 words
- ✅ Context detection: 85%+ correct type

### Reliability
- ✅ Availability: 99% (with graceful degradation)
- ✅ Error rate: <1% (excluding network issues)
- ✅ Fallback quality: 80%+ acceptable (template-based)

---

## 🔄 AI Model Strategy

### v2.0: Granite Only (Red Hat Approved)
```
Primary: granite-3.2-8b-instruct
Fallback: granite-3.1-8b-instruct
```

**Rationale**: 
- Red Hat compliant
- Fast enough for real-time use
- Good quality with proper prompts
- Available via LiteLLM proxy

### v2.1+: Model Experimentation
```
- Test larger Granite models (20B+)
- Compare quality vs speed tradeoffs
- User preference (fast vs high-quality)
- Custom fine-tuning for TAM domain
```

---

## 🎯 AI Feature Roadmap

### v2.0 (MUST HAVE)
- ✅ Clippy email assistant (Gmail drafts)
- ✅ Context detection (RFE, Bug, Customer Update)
- ✅ Graceful degradation (template fallback)
- ✅ Professional tone enforcement

### v2.1 (NICE TO HAVE)
- ⏳ RFE report generation (from case notes)
- ⏳ Executive summary generation (JIRA → business language)
- ⏳ Customer Portal report formatting (markdown → HTML)
- ⏳ Meeting notes → follow-up email

### v3.0 (FUTURE)
- ⏳ Custom model fine-tuning (TAM-specific vocabulary)
- ⏳ Multi-language support (non-English customers)
- ⏳ Voice-to-text integration (verbal notes → email)
- ⏳ Sentiment analysis (customer email → urgency detection)

---

## 🔐 AI Compliance (Red Hat)

### Model Approval
- ✅ **ONLY Red Hat approved models** (Granite, Mistral via AIA)
- ❌ **NEVER** use GPT-4, Claude, or external APIs for customer data
- ✅ **LiteLLM proxy** ensures compliance (model routing)

### Data Privacy
- ✅ Customer data stays on rhgrimm (internal network)
- ✅ No external API calls with customer info
- ✅ Clipboard content not logged or persisted
- ✅ Generated drafts deleted on user request

### Audit Trail
- ✅ Log AI usage (model, timestamp, feature)
- ✅ Track performance metrics
- ❌ DO NOT log customer content or generated drafts

---

## 💡 AI User Experience Principles

### Principle 1: Transparency
**User always knows when AI is involved.**

- "AI-generated draft" label
- "Powered by Red Hat Granite" branding
- Model name shown in UI
- Clear "Edit before sending" messaging

---

### Principle 2: User Control
**AI suggests, user decides.**

- Always show preview before saving
- Easy to edit generated content
- Can regenerate with different tone
- Can disable AI and use templates

---

### Principle 3: Trust Through Quality
**AI must earn user trust through consistent quality.**

- First draft is good enough to send 80%+ of the time
- Errors are obvious (not subtle wrong facts)
- Professional tone never wavers
- Graceful degradation preserves trust

---

### Principle 4: Feedback Loop
**Learn from user edits (future v3.0).**

- Track what users change
- Identify common patterns
- Improve prompts based on edits
- Optional: Fine-tune model on accepted drafts

---

## ✅ AI Framework Checklist (v2.0)

Before shipping alpha:

### Code Quality
- [ ] AIClient properly handles all error cases
- [ ] GmailAssistant gracefully degrades without AI
- [ ] Prompts follow best practices (examples, constraints)
- [ ] Context detection accuracy >85%
- [ ] Generated drafts are professional 95%+ of time

### Testing
- [ ] Run AI integration test suite (`tests/test_ai_integration.py`)
- [ ] Test with 10+ real customer emails
- [ ] Test all email types (RFE, Bug, Customer Response)
- [ ] Test graceful degradation (LiteLLM down)
- [ ] Test edge cases (empty input, long input, HTML)

### User Experience
- [ ] Clear AI status indicators in GUI
- [ ] Preview before save
- [ ] Edit functionality works
- [ ] Error messages are helpful
- [ ] Loading states prevent confusion

### Documentation
- [ ] Document how to start LiteLLM proxy
- [ ] Document prompt engineering guidelines
- [ ] Document testing procedures
- [ ] Document troubleshooting (AI unavailable)

---

## 🎯 Success Metrics (Post-Launch)

### Adoption Metrics
- **AI Usage Rate**: % of drafts generated with AI vs templates
  - Target: >70% (users prefer AI)
- **Edit Rate**: % of AI drafts edited before sending
  - Target: <50% (most drafts acceptable as-is)
- **Regeneration Rate**: % of drafts regenerated
  - Target: <20% (first draft usually good)

### Quality Metrics
- **User Satisfaction**: Survey after using Clippy
  - Target: 4/5 stars average
- **Time Saved**: Self-reported time saved per email
  - Target: >10 minutes average
- **Abandonment Rate**: % of users who try Clippy once and never again
  - Target: <10%

### Performance Metrics
- **Generation Time**: p95 latency for draft generation
  - Target: <10 seconds
- **Availability**: % of time AI is available
  - Target: >95% (with graceful degradation)
- **Error Rate**: % of generations that fail
  - Target: <2%

---

## 🚀 Immediate Next Steps

### Week 1: Prompt Engineering
1. Improve `_build_draft_prompt()` with examples
2. Add anti-hallucination guardrails
3. Test with 20+ real customer emails
4. Iterate prompts until 90%+ quality

### Week 2: Quality Testing
1. Run automated test suite
2. Manual testing with real TAM workflows
3. Fix any issues found
4. Document prompt patterns

### Week 3: Alpha Testing
1. Deploy to 3 friendly TAMs
2. Collect feedback on AI quality
3. Track edit rates and regeneration rates
4. Iterate based on feedback

---

## 💬 The Bottom Line

**AI is not a feature. AI is THE differentiator.**

Without AI:
- Taminator is a nice GUI for JIRA/Portal
- Saves maybe 5 minutes per workflow
- Competes with browser bookmarks

With AI (done right):
- Taminator is a TAM productivity multiplier
- Saves 15-20 minutes per email
- Becomes indispensable to daily workflow

**Get the AI framework right in v2.0, and TAMs will adopt it.**  
**Get it wrong, and they'll never trust it again.**

---

*Taminator v2.0 - AI Framework*  
*AI Done Right: Professional. Reliable. Trustworthy.*


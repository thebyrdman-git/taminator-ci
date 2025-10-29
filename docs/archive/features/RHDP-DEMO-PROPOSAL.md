# Taminator Interactive Demo - Red Hat Demo Platform (RHDP)

**Platform**: https://zero.rhdp.net/  
**Target Audience**: TAM team (internal Red Hat)  
**Objective**: Let TAMs try Taminator before installing. Show value in 15 minutes.

---

## Why This Matters

**Problem**: TAMs won't install a tool they don't understand.  
**Solution**: Interactive demo shows value before commitment.  
**ROI**: If 50 TAMs complete demo → 30 install → 20 adopt = 20 hours/week saved across team.

---

## Demo Structure (15 Minutes)

### Lab 1: "Create an RFE Report in 5 Minutes" (5 min)
**Scenario**: Customer requested performance monitoring feature  
**Task**: Use Taminator to create professional RFE report  
**Value**: Compare manual JIRA (20 min) vs Taminator (5 min)

**Lab Environment**:
- Pre-configured Taminator instance (no install needed)
- Sample customer: "TD Bank"
- Mock JIRA credentials (pre-configured)
- Sample case notes provided

**Steps**:
1. Open Taminator (already running)
2. Navigate to RFE tab
3. Paste case notes (provided)
4. AI generates draft report
5. Review and submit to JIRA
6. **Result**: Professional RFE report created in <5 minutes

**Success Metric**: User says "That was way faster than manual JIRA"

---

### Lab 2: "AI-Powered Customer Email" (5 min)
**Scenario**: Customer asked about RHEL 9 upgrade timeline  
**Task**: Use Clippy to generate professional response  
**Value**: Compare staring at blank email (15 min) vs AI draft (2 min)

**Lab Environment**:
- Clippy Gmail assistant (pre-auth)
- Sample customer email (provided)
- AI model pre-configured

**Steps**:
1. Copy customer email to clipboard
2. Open Clippy tab
3. Paste content → AI generates draft
4. Review draft (professional tone, correct facts)
5. Edit if needed → Save to Gmail (demo only, not real Gmail)
6. **Result**: Professional email draft ready to send

**Success Metric**: User says "I'd actually use this"

---

### Lab 3: "Customer Dashboard Overview" (5 min)
**Scenario**: Quick customer status check before call  
**Task**: Use Taminator dashboard to prep for meeting  
**Value**: All customer info in one place (vs 5 browser tabs)

**Lab Environment**:
- Pre-loaded customer data (TD Bank)
- Mock JIRA issues
- Sample case history

**Steps**:
1. Open dashboard
2. Select customer: TD Bank
3. View at-a-glance:
   - Open JIRA issues (3 RFEs, 2 bugs)
   - Recent case activity
   - Customer Portal posts
4. Click issue → View details
5. **Result**: Meeting-ready in <2 minutes

**Success Metric**: User says "This is better than my current workflow"

---

## Technical Requirements (RHDP Platform)

### Base Infrastructure
```
- VM: RHEL 9 (2 CPU, 4GB RAM)
- Network: Internal Red Hat network access
- Duration: Lab expires after 2 hours
```

### Pre-Installed Software
```bash
# Taminator AppImage
/opt/taminator/taminator-v2.0.0-x86_64.AppImage

# FastAPI service (auto-start)
systemctl enable --now taminator-service

# LiteLLM proxy (mock mode)
# Uses Red Hat Granite model (compliance)
systemctl enable --now litellm-mock

# Mock JIRA/Portal APIs
# Returns realistic data without real API calls
systemctl enable --now taminator-mock-apis
```

### Pre-Configuration
```yaml
# ~/.config/taminator/demo.yaml
demo_mode: true
mock_apis: true
sample_customer: "TD Bank"
sample_data_path: "/opt/taminator/demo-data/"

# Pre-configured auth (demo tokens)
jira_token: "demo-token-jira"
portal_token: "demo-token-portal"
google_oauth: "demo-token-google"
```

### Demo Data Structure
```
/opt/taminator/demo-data/
├── customers/
│   └── td-bank/
│       ├── cases/
│       │   ├── case-01234567.md
│       │   └── case-01234568.md
│       └── jira/
│           ├── RHEL-12345.json
│           └── RHEL-12346.json
├── templates/
│   ├── rfe-template.md
│   └── customer-email.txt
└── mock-responses/
    ├── jira-api.json
    └── portal-api.json
```

---

## Build Process (For RHDP Team)

### 1. Create Base VM Image
```bash
# Start with RHEL 9 minimal
dnf install -y \
    python3.11 \
    python3-pip \
    gnome-keyring \
    xorg-x11-server-Xvfb  # For headless demo

# Install Taminator
cd /opt
curl -LO https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases/v2.0.0/taminator-x86_64.AppImage
chmod +x taminator-x86_64.AppImage
```

### 2. Configure Services
```bash
# Taminator service (systemd)
cat > /etc/systemd/system/taminator-service.service << EOF
[Unit]
Description=Taminator FastAPI Service
After=network.target

[Service]
Type=simple
User=demo
WorkingDirectory=/opt/taminator
ExecStart=/usr/bin/python3 /opt/taminator/api/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable taminator-service
```

### 3. Seed Demo Data
```bash
# Create sample customer
mkdir -p /opt/taminator/demo-data/customers/td-bank

# Add realistic case notes
cat > /opt/taminator/demo-data/customers/td-bank/cases/case-01234567.md << 'EOF'
# Case: 01234567 - Performance Monitoring Request

**Customer**: TD Bank  
**Priority**: High  
**Status**: Open

## Request
Customer needs real-time performance monitoring API for RHEL 9.

## Requirements
- REST API for CPU/memory metrics
- Sub-second latency
- Integration with Splunk
- Support for 1000+ servers

## Business Impact
Critical for Q1 2025 datacenter migration.
EOF
```

### 4. Configure Mock APIs
```python
# /opt/taminator/mock-apis.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/rest/api/2/search")
def mock_jira_search():
    return {
        "issues": [
            {
                "key": "RHEL-12345",
                "fields": {
                    "summary": "Performance Monitoring API",
                    "status": {"name": "In Progress"},
                    "priority": {"name": "High"}
                }
            }
        ]
    }

# Start mock server
# uvicorn mock-apis:app --port 9999
```

---

## Lab Instructions (User-Facing)

### Lab Start Page
```
Welcome to Taminator Interactive Demo!

You're a Red Hat TAM working with TD Bank.
They've requested a new RHEL feature.

Your job: Create a professional RFE report.

Time estimate: 5 minutes
Traditional method: 20-30 minutes

Let's see the difference.

[Start Lab] [Skip Tutorial]
```

### Step-by-Step Guide
```
STEP 1: Open Taminator
-------------------------
Click the Taminator icon on the desktop.
The app should launch in <5 seconds.

Expected: You see the dashboard with TD Bank listed.

[✓] Taminator launched
[→] Next Step


STEP 2: Create RFE Report
--------------------------
1. Click "Create RFE" button (top right)
2. Select customer: TD Bank
3. Paste these case notes:

   [Case notes text box - pre-filled]

4. Click "Generate Draft"

Expected: AI generates professional RFE report in ~10 seconds.

[✓] Draft generated
[→] Review Draft


STEP 3: Review AI-Generated Report
-----------------------------------
Review the draft RFE report.

Notice:
- Professional formatting
- Includes all customer requirements
- References case number
- Suggests timeline

Compare this to manual JIRA entry:
- Manual: 15 fields, 20 minutes
- Taminator: Review and click, 5 minutes

Edit if needed, then click "Submit to JIRA"

[✓] Report submitted
[→] Next Lab
```

---

## Validation & Success Criteria

### Technical Validation
- [ ] VM boots in <60 seconds
- [ ] Taminator service starts automatically
- [ ] Mock APIs respond correctly
- [ ] AI generates realistic drafts
- [ ] No real JIRA/Portal API calls
- [ ] No real Gmail API calls (mock only)

### User Experience Validation
- [ ] Instructions are clear (no guessing)
- [ ] Each step takes <2 minutes
- [ ] Demo completes in 15 minutes total
- [ ] User can't break the demo (fail-safe)
- [ ] Works on first try (no troubleshooting)

### Adoption Metrics
- **Target**: 50 TAMs complete demo in first month
- **Success**: 60% say "I want to install this"
- **Conversion**: 40% actually install after demo
- **Retention**: 80% still using after 30 days

---

## Deployment Plan

### Phase 1: Build Demo (Week 1)
- Create RHDP VM image
- Configure all services
- Seed demo data
- Write lab instructions
- Test internally (5 people)

### Phase 2: Internal Testing (Week 2)
- Deploy to RHDP staging
- Test with 10 TAMs (not target audience)
- Fix issues found
- Refine instructions
- Measure completion time

### Phase 3: Launch (Week 3)
- Deploy to RHDP production
- Announce on TAM team channels
- Track completion metrics
- Collect feedback
- Iterate based on feedback

---

## Promotion Strategy

### Announcement (TAM Slack Channel)
```
🚀 New: Taminator Interactive Demo

Try Taminator without installing anything.

Learn to:
- Create RFE reports in 5 minutes (not 20)
- Generate AI-powered customer emails
- Manage customer workflows in one place

Time: 15 minutes
Platform: https://zero.rhdp.net/taminator-demo

No installation. No setup. Just try it.

Questions? DM me.
```

### Follow-Up (After Demo)
- Email with installation instructions
- Link to full documentation
- Offer 1:1 onboarding call
- Slack channel for questions

---

## Maintenance & Updates

### Monthly Review
- Check completion rates
- Read user feedback
- Update demo data (keep realistic)
- Refresh VM image (security patches)

### Quarterly Updates
- Add new features to demo
- Update lab instructions
- Refresh sample data
- Re-test entire flow

---

## Cost Analysis

### Development Time
- RHDP VM setup: 8 hours
- Mock API development: 4 hours
- Demo data creation: 4 hours
- Lab instructions: 4 hours
- Testing/refinement: 8 hours
- **Total**: 28 hours (1 person, 1 week)

### Ongoing Maintenance
- Monthly check: 2 hours/month
- Quarterly update: 8 hours/quarter
- **Annual**: ~50 hours

### ROI Calculation
```
If 50 TAMs complete demo:
- 30 install (60% conversion)
- 20 adopt (66% retention)
- 20 TAMs × 10 hours saved/month = 200 hours/month
- 200 hours × $100/hour = $20,000/month value
- Demo development: $5,000 (50 hours × $100)
- ROI: 4:1 in first month, 48:1 in first year
```

---

## Alternatives Considered

### Option 1: Video Demo (Rejected)
- Pros: Easy to create
- Cons: Passive, no hands-on, low retention

### Option 2: Sandbox Environment (Rejected)
- Pros: Full functionality
- Cons: Requires installation, high friction

### Option 3: Interactive Demo (SELECTED)
- Pros: Hands-on, low friction, high retention
- Cons: Requires RHDP setup (one-time cost)

---

## Next Steps

1. **Get RHDP access** - Request demo platform account
2. **Build base VM** - RHEL 9 + Taminator + mock APIs
3. **Create lab instructions** - User-facing walkthrough
4. **Internal testing** - 5 people, collect feedback
5. **Launch** - Announce to TAM team
6. **Track metrics** - Completion rate, feedback, adoption

**Timeline**: 3 weeks from approval to launch.

---

## Questions for RHDP Team

1. What's the process to request demo VM creation?
2. Can we auto-start services on VM boot?
3. Is there a template for lab instructions?
4. How do we track completion metrics?
5. Can we integrate with Red Hat SSO for tracking?
6. What's the process for updating the demo after launch?

---

*Taminator Interactive Demo - RHDP Proposal*  
*Show value before installation. Earn adoption through experience.*


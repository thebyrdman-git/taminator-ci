# Roadmap

**TAMINATOR Development Roadmap**

!!! info "Status Legend"
    - ✅ **Available** - Shipped and ready to use
    - 🚧 **In Development** - Actively being built
    - 📋 **Planned** - Committed for future release
    - 💡 **Proposed** - Under consideration
    - ❌ **Not Planned** - Out of scope

---

## Current Release: v2.1.0 (November 2025)

### ✅ Shipped Features

**Intelligence Engine:**
- ✅ Pattern-based email analysis (89% accuracy)
- ✅ Case number extraction (95% accuracy)
- ✅ Customer identification (92% accuracy)
- ✅ Issue classification (Licensing, Technical, Guidance, Strategic)
- ✅ Contact extraction with role detection
- ✅ Urgency assessment with deadline calculation
- ✅ Action recommendations with routing logic
- ✅ Confidence scoring for all predictions

**Data & Persistence:**
- ✅ SQLite embedded database
- ✅ Case intelligence history
- ✅ Feedback recording system
- ✅ Accuracy tracking over time
- ✅ Database health checks

**User Interface:**
- ✅ Intelligence Analyzer interface
- ✅ Dashboard analytics
- ✅ Customer management
- ✅ RFE/Bug tracking
- ✅ Report generation
- ✅ Settings management

**Deployment:**
- ✅ Container deployment (Podman/Docker)
- ✅ Systemd service integration
- ✅ AppImage for Linux
- ✅ DMG for macOS (Intel + Apple Silicon)
- ✅ EXE installer for Windows
- ✅ Self-healing with auto-restart

**Integrations:**
- ✅ JIRA API integration
- ✅ Customer Portal API
- ✅ rhcase bot integration
- ✅ Red Hat SSO authentication

**Documentation:**
- ✅ Complete user guide
- ✅ Deployment documentation
- ✅ Architecture documentation
- ✅ API reference

---

## v2.1.x - Refinement Release (Q4 2025)

### 🚧 In Development

**Team Collaboration:**
- 🚧 Pattern sharing across team members
- 🚧 Team intelligence dashboard
- 🚧 Shared customer insights

**Customization:**
- 🚧 Custom pattern editor (GUI)
- 🚧 Pattern testing interface
- 🚧 Import/export custom rules

**Data Management:**
- 🚧 Export intelligence data (JSON/CSV)
- 🚧 Import historical data
- 🚧 Backup/restore workflows

### Target: December 2025

---

## v2.2.0 - Learning & Feedback (Q1 2026)

### 📋 Planned Features

**Advanced Pattern Learning:**
- 📋 Automated pattern optimization from TAM feedback
- 📋 A/B testing for analysis rules
- 📋 Pattern effectiveness scoring
- 📋 Automatic pattern deprecation for low-performing rules

**Feedback System:**
- 📋 One-click feedback on analysis results
- 📋 Bulk feedback processing
- 📋 Feedback analytics dashboard
- 📋 TAM contribution leaderboard

**Accuracy Improvements:**
- 📋 Multi-language support (Spanish, Portuguese)
- 📋 Industry-specific patterns (Finance, Healthcare, Government)
- 📋 Product-specific patterns (AAP, RHEL, OpenShift)
- 📋 Historical case analysis for pattern discovery

### Target: March 2026

---

## v2.3.0 - Team Intelligence (Q2 2026)

### 📋 Planned Features

**Centralized Intelligence:**
- 📋 Shared pattern library (Red Hat-wide)
- 📋 Best practices repository
- 📋 Team pattern approval workflow
- 📋 Pattern versioning and rollback

**Collaboration:**
- 📋 Team-wide accuracy metrics
- 📋 Pattern contribution tracking
- 📋 Knowledge base integration
- 📋 Collaborative pattern refinement

**Analytics:**
- 📋 Team performance dashboard
- 📋 Customer intelligence trends
- 📋 Issue type distribution analysis
- 📋 Escalation pattern analysis

### Target: June 2026

---

## v2.4.0 - Predictive Intelligence (Q3 2026)

### 📋 Planned Features

**Predictive Analysis:**
- 📋 Issue escalation prediction
- 📋 Customer health scoring
- 📋 Churn risk assessment
- 📋 Proactive case recommendations

**Advanced Intelligence:**
- 📋 Sentiment analysis (urgency detection)
- 📋 Priority scoring algorithms
- 📋 Workload balancing suggestions
- 📋 SLA risk detection

**Automation:**
- 📋 Auto-routing to correct teams
- 📋 Auto-assignment based on expertise
- 📋 Auto-escalation triggers
- 📋 Auto-follow-up reminders

### Target: September 2026

---

## v3.0.0 - AI Integration (Q4 2026)

### 📋 Planned Features

!!! warning "Compliance-First AI Integration"
    All AI features will maintain strict Red Hat compliance. Customer data will **never** be sent to external services.

**Ansai Integration (Internal TAM Use Only):**
- 📋 Fabric patterns for TAM documentation
- 📋 LiteLLM for training materials
- 📋 AI-assisted report writing (non-customer data)
- 📋 Knowledge base generation from public documentation

**Advanced Analysis (Offline Only):**
- 📋 Enhanced pattern matching with local ML models
- 📋 Contextual analysis improvements
- 📋 Relationship mapping between cases
- 📋 Trend detection and forecasting

**Compliance:**
- 📋 Clear separation: Customer data vs. Internal data
- 📋 Audit trails for all AI usage
- 📋 User consent for AI features
- 📋 Opt-out options for all AI capabilities

### Target: December 2026

---

## Features NOT Planned

### ❌ Out of Scope

**External AI APIs:**
- ❌ ChatGPT/Claude/Other cloud AI for customer data
- ❌ Cloud-based intelligence processing
- ❌ External data storage
- ❌ Third-party analytics services

**Reason:** Red Hat policy compliance. Customer data must stay local and offline.

**Consumer Features:**
- ❌ Public SaaS offering
- ❌ Non-Red Hat user support
- ❌ General-purpose email analysis

**Reason:** Taminator is purpose-built for Red Hat TAMs.

**Platform Expansion:**
- ❌ Mobile apps (iOS/Android)
- ❌ Browser extensions
- ❌ Slack/Teams bots

**Reason:** Limited team resources, focus on core TAM workflows.

---

## 💡 Proposed Ideas (Under Consideration)

**Community Contributions:**
- 💡 Open-source pattern library
- 💡 Plugin system for custom analyzers
- 💡 Integration marketplace

**Advanced Workflows:**
- 💡 Multi-case analysis (trends across portfolio)
- 💡 Customer journey mapping
- 💡 Automated reporting to management

**Intelligence Sharing:**
- 💡 Anonymous intelligence sharing across Red Hat
- 💡 Industry benchmark comparisons
- 💡 Best practices recommendations

**Vote on Features:** [GitLab Discussions](https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues)

---

## How to Influence the Roadmap

### 1. Submit Feature Requests

[Create an Issue](https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues/new) with:
- Clear use case description
- Expected behavior
- Impact on your workflow
- Proposed implementation (optional)

### 2. Vote on Existing Requests

- 👍 Upvote issues you care about
- 💬 Comment with your specific use case
- 🏷️ Add relevant labels

### 3. Contribute Patterns

- Share analysis patterns that work well
- Document edge cases you've discovered
- Suggest improvements to existing patterns

### 4. Join Beta Testing

- Test new features before release
- Provide detailed feedback
- Help identify bugs and usability issues

---

## Release Schedule

**Cadence:**
- **Major releases** (x.0.0): Quarterly
- **Minor releases** (x.x.0): Monthly
- **Patch releases** (x.x.x): As needed

**Support:**
- **Current release** (2.1.x): Full support
- **Previous release** (2.0.x): Bug fixes only
- **Older releases**: No support (upgrade recommended)

---

## Version History

| Version | Release Date | Status | Notes |
|---------|-------------|---------|-------|
| 2.1.0 | Nov 2025 | ✅ Current | Intelligence engine, container deployment |
| 2.0.0 | Oct 2025 | 🔒 Maintenance | FastAPI architecture, OOBE wizard |
| 1.10.x | Sep 2025 | ⚠️ Deprecated | CLI-based, upgrade recommended |

---

## Communication Channels

**Announcements:**
- GitLab Releases: [Taminator Releases](https://gitlab.cee.redhat.com/jbyrd/taminator/-/releases)
- Slack: #taminator-intelligence (coming soon)
- Email: jbyrd@redhat.com

**Feedback:**
- GitLab Issues: [Report bugs](https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues)
- Feature Requests: [Request features](https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues)
- Direct Contact: jbyrd@redhat.com

---

## Roadmap Transparency

This roadmap is a **living document** and will be updated as:
- Priorities shift based on TAM feedback
- New requirements emerge
- Resources become available
- Technology evolves

**Last Updated:** November 11, 2025  
**Next Review:** December 2025

---

**Philosophy: Build what TAMs need, when they need it. Nothing more, nothing less.**

*Powered by Ansai - https://ansai.dev*


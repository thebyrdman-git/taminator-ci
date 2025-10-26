# Taminator Glossary

**Product:** Taminator v1.10.0  
**Document Type:** Terms and Definitions  
**Last Updated:** October 25, 2025

---

## A

**AAP**  
**Ansible Automation Platform** - Red Hat's enterprise automation solution for IT operations. One of the primary products tracked in Taminator.

**Account Number**  
A unique identifier assigned by Red Hat to enterprise customers. Required for JIRA filtering and customer onboarding. Example: `334224`

**API Token**  
A credential string used for programmatic access to Red Hat APIs. Required tokens: JIRA API token (mandatory), Portal API token (optional).

**AppImage**  
A portable Linux application format that bundles all dependencies. Taminator's primary Linux distribution format (x86_64 and ARM64 variants).

**argparse**  
Python standard library module for parsing command-line arguments. Used in Taminator's CLI routing.

---

## B

**Bug**  
A software defect tracked in JIRA. Taminator monitors open Bugs for TAM customers alongside RFEs.

**Backlog**  
JIRA status indicating an issue has been triaged but not yet prioritized for development.

**Bearer Token**  
An HTTP authentication scheme using a token string in the `Authorization` header. Used for Customer Portal API access.

---

## C

**Case**  
Short for "Support Case" - a customer issue tracked in Red Hat's Customer Portal. Often linked to JIRA RFEs/Bugs via custom field `customfield_12316840`.

**CLI**  
**Command-Line Interface** - Text-based interface for operating Taminator via terminal. All GUI features have CLI equivalents.

**Customer Portal**  
Red Hat's support portal (access.redhat.com) where customers open cases, access documentation, and receive updates.

**Custom Field**  
Extended JIRA fields beyond standard issue properties. Example: `customfield_12316840` stores the linked support case number.

---

## D

**Dashboard**  
Taminator's main tab showing aggregated customer statistics: total RFEs, Bugs, and per-customer breakdowns with live JIRA data.

**DMG**  
**Disk Image** - macOS application distribution format. Taminator provides universal DMG for Intel and Apple Silicon Macs.

**Dry Run**  
A mode that simulates an operation without making actual changes. Example: `tam-rfe post --dry-run` previews Portal posting without publishing.

---

## E

**Electron**  
Cross-platform desktop application framework using Chromium and Node.js. Taminator's GUI is built with Electron 27.x.

**Environment Variable**  
OS-level configuration variable. Taminator supports token storage via `JIRA_TOKEN_API_TOKEN` and `PORTAL_TOKEN_API_TOKEN`.

---

## F

**Factory Reset**  
Settings option to restore Taminator to first-run state, clearing OOBE completion and forcing the wizard to re-run.

**Focus Mode**  
UI setting that disables fun features (Clippy, sounds) for professional presentation or demo scenarios.

---

## G

**Gatekeeper**  
macOS security feature that blocks unsigned applications. Taminator requires right-click → Open on first launch to bypass.

**GitLab**  
Red Hat's internal Git repository hosting platform. Taminator production code: `gitlab.cee.redhat.com/jbyrd/taminator`

**GUI**  
**Graphical User Interface** - Taminator's Electron-based desktop application with dashboard, tabs, and settings.

---

## H

**HashiCorp Vault**  
Enterprise secrets management system. Taminator supports Vault for centralized team token sharing (optional).

**HTTP Basic Auth**  
Authentication scheme sending username and password (or token) in request headers. Used for JIRA API authentication.

---

## I

**IPC**  
**Inter-Process Communication** - Mechanism for Electron main process to communicate with renderer process. Taminator uses IPC to bridge GUI and Python backend.

**Issue**  
Generic term for JIRA tickets (RFEs or Bugs). Taminator tracks open issues for customer accounts.

---

## J

**JIRA**  
Atlassian's issue tracking system. Red Hat JIRA: `issues.redhat.com`. Taminator queries JIRA for live RFE/Bug data.

**JQL**  
**JIRA Query Language** - SQL-like syntax for querying JIRA. Example: `project in (AAP) AND "Red Hat Account" = 334224`

**JSON**  
**JavaScript Object Notation** - Data format for structured output. CLI commands support `--json` flag for machine-readable results.

---

## K

**Keyring**  
OS-level secure credential storage (Windows Credential Manager, macOS Keychain, Linux Secret Service). **Note:** Removed in v1.10.0 in favor of config files.

**Konami Code**  
Classic cheat code (↑↑↓↓←→←→BA) that activates Taminator's SkiFree easter egg.

---

## L

**Live JIRA**  
Real-time data fetched directly from JIRA API, as opposed to cached/saved report data. Dashboard shows 🟢 for live data.

---

## M

**Markdown**  
Lightweight markup language used for Taminator's customer report format (`.md` files).

**Mount Point**  
HashiCorp Vault configuration: the secrets engine path (default: `secret`).

---

## N

**Non-Interactive Mode**  
CLI mode that doesn't prompt for user input, suitable for automation. Example: `tam-rfe onboard --non-interactive`

**NSIS**  
**Nullsoft Scriptable Install System** - Windows installer framework used for Taminator's Windows distribution.

---

## O

**OOBE**  
**Out-of-Box Experience** - First-run setup wizard guiding users through authentication and customer onboarding (screens 1-5).

**Offline Token**  
Long-lived API token for Red Hat Customer Portal. Generated at access.redhat.com/management/api.

---

## P

**PatternFly**  
Red Hat's open-source design system and UI component library. Taminator's GUI follows PatternFly 4.x guidelines.

**Portal API**  
Red Hat Customer Portal REST API (`api.access.redhat.com`) for case queries and group posting.

**Product**  
Red Hat product/service tracked in JIRA. Examples: Ansible Automation Platform, RHEL, OpenShift. Required for customer onboarding.

---

## Q

**Query**  
Database or API search operation. Taminator queries JIRA using JQL to fetch customer RFEs/Bugs.

---

## R

**RFE**  
**Request for Enhancement** - Customer feature request tracked in JIRA. Taminator monitors open RFEs for TAM accounts.

**RHEL**  
**Red Hat Enterprise Linux** - Linux distribution and one of the primary products tracked in Taminator.

**Rich**  
Python library for terminal formatting (tables, colors, progress bars). Used extensively in Taminator CLI output.

---

## S

**SBR Group**  
**SBR** stands for **Support/Business Requirements**. JIRA custom field grouping issues by product team. Example: "SBR Ansible" for Ansible Automation Platform issues.

**Slug**  
Short, URL-safe identifier for customers. Example: `jpmc` for JPMorgan Chase. Used in filenames and commands.

**Status**  
JIRA issue state (New, Backlog, In Progress, Post, Closed, Done). Taminator tracks status changes.

**Subprocess**  
Process spawned by another process. Taminator GUI spawns Python CLI via subprocess for backend operations.

---

## T

**TAM**  
**Technical Account Manager** - Red Hat customer-facing role providing technical guidance and support. Taminator's primary user audience.

**Token**  
Authentication credential for API access. Types: JIRA API token (required), Portal API token (optional).

---

## U

**UAC**  
**User Account Control** - Windows security feature prompting for administrator approval. Taminator installer requires UAC confirmation.

---

## V

**Vault**  
Short for HashiCorp Vault. Centralized secrets management system for team token sharing.

**VPN**  
**Virtual Private Network** - Red Hat's internal network. Required for accessing JIRA and Portal APIs from external networks.

---

## W

**Workflow**  
Sequence of operations to complete a task. Common TAM workflow: Check → Update → Post.

---

## X

**XP Sounds**  
Windows XP system sounds (startup, error, notification) available as Taminator easter egg. Toggle in Settings.

---

## Common Acronyms

| Acronym | Full Name | Context |
|---------|-----------|---------|
| **AAP** | Ansible Automation Platform | Product |
| **API** | Application Programming Interface | Integration |
| **CLI** | Command-Line Interface | User interface |
| **DMG** | Disk Image | macOS installer |
| **GUI** | Graphical User Interface | Desktop app |
| **IPC** | Inter-Process Communication | Architecture |
| **JIRA** | - (brand name) | Issue tracking |
| **JQL** | JIRA Query Language | Querying |
| **JSON** | JavaScript Object Notation | Data format |
| **NSIS** | Nullsoft Scriptable Install System | Windows installer |
| **OOBE** | Out-of-Box Experience | First-run wizard |
| **RFE** | Request for Enhancement | Issue type |
| **RHEL** | Red Hat Enterprise Linux | Product |
| **SBR** | Support/Business Requirements | JIRA grouping |
| **TAM** | Technical Account Manager | User role |
| **UAC** | User Account Control | Windows security |
| **VPN** | Virtual Private Network | Network access |

---

## Command Quick Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `tam-rfe config` | Manage tokens | `tam-rfe config --add-token` |
| `tam-rfe dashboard` | View all customers | `tam-rfe dashboard --json` |
| `tam-rfe check` | Compare report vs JIRA | `tam-rfe check jpmc` |
| `tam-rfe update` | Sync report with JIRA | `tam-rfe update jpmc --yes` |
| `tam-rfe post` | Publish to Portal | `tam-rfe post jpmc` |
| `tam-rfe onboard` | Add new customer | `tam-rfe onboard <slug> --account 123456 --product Ansible` |
| `tam-rfe gui` | Launch GUI | `tam-rfe gui` |

---

## File Locations

| Path | Purpose |
|------|---------|
| `~/.config/taminator/` | Configuration directory |
| `~/.config/taminator/tokens.json` | API tokens (chmod 600) |
| `~/.config/taminator-gui/oobe-state.json` | OOBE completion state |
| `~/taminator-test-data/` | Customer reports |
| `~/taminator-test-data/<slug>.md` | Individual customer report |
| `~/taminator-test-data/<slug>.md.backup` | Automatic backup |

---

## JIRA Custom Fields

| Field ID | Purpose | Example Value |
|----------|---------|---------------|
| `customfield_12316840` | Support Case | `03891234` |
| (Account field) | Red Hat Account Number | `334224` |
| (SBR Group field) | Product Team | `SBR Ansible` |

---

## Status Values

| Status | Meaning |
|--------|---------|
| **New** | Issue created, not yet triaged |
| **Backlog** | Triaged, not yet prioritized |
| **Refinement** | Under review for feasibility |
| **In Progress** | Actively being worked on |
| **Post** | Completed, ready for release |
| **Closed** | Resolved and closed |
| **Done** | Completed and delivered |

---

## Product → SBR Group Mapping

| Product | SBR Group | JIRA Projects |
|---------|-----------|---------------|
| **Ansible Automation Platform** | SBR Ansible | AAP, AAPRFE |
| **Red Hat Enterprise Linux** | SBR RHEL | RHEL |
| **OpenShift Container Platform** | SBR OpenShift | OCPBUGS |
| **Satellite** | SBR Satellite | SAT |

---

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `JIRA_TOKEN_API_TOKEN` | JIRA API token | `MTE1NjQyMD...` |
| `PORTAL_TOKEN_API_TOKEN` | Portal API token | `eyJhbGc...` |
| `VAULT_ADDR` | Vault server URL | `http://vault.example.com:8200` |
| `VAULT_TOKEN` | Vault auth token | `hvs.CAESII...` |
| `VAULT_MOUNT` | Vault mount point | `secret` |
| `VAULT_PATH` | Vault secret path | `taminator/tokens` |
| `TAMINATOR_DEBUG` | Enable debug logging | `1` or `true` |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| **0** | Success |
| **1** | General error |
| **2** | Invalid arguments |
| **3** | Authentication failure |
| **4** | Network error |
| **5** | File not found |

---

## Related Documentation

- **User Guide:** [README.md](README.md)
- **Quick Start:** [GETTING-STARTED.md](GETTING-STARTED.md)
- **Installation:** [INSTALLATION-GUIDE-V1.10.0.md](INSTALLATION-GUIDE-V1.10.0.md)
- **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Release Notes:** [RELEASE-V1.10.0-COMPLETE.md](RELEASE-V1.10.0-COMPLETE.md)

---

**Glossary Version:** 1.0  
**Last Updated:** October 25, 2025  
**Terms:** 75+  
**Status:** Complete


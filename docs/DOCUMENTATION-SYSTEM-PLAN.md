# Taminator Documentation System - Red Hat Enterprise Standard

**Goal**: Emulate Red Hat/Linux documentation ecosystem with professional tooling

---

## 🎯 Documentation Layers

### Layer 1: CLI Help (`--help`)
**Every command has built-in help:**
```bash
tam-rfe --help                    # Main command help
tam-rfe create --help             # Subcommand help
tam-rfe check-jira --help         # Feature help
taminator-service --help          # Service help
```

**Features:**
- Command syntax
- Option descriptions
- Examples
- Exit codes
- See also references

---

### Layer 2: Man Pages (`man`)
**Traditional Unix documentation:**
```bash
man tam-rfe                       # Full command manual
man tam-rfe-create                # Subcommand manual
man taminator-service             # Service manual
man taminator.conf                # Configuration file manual
```

**Man Page Sections:**
- NAME
- SYNOPSIS
- DESCRIPTION
- OPTIONS
- EXAMPLES
- FILES
- SEE ALSO
- BUGS
- AUTHOR

---

### Layer 3: Web Documentation
**Red Hat Customer Portal style:**
```
https://docs.taminator.local/
├── Getting Started
├── Installation Guide
├── User Guide
│   ├── Creating RFEs
│   ├── Tracking Bugs
│   └── Customer Management
├── Integration Guides
│   ├── JIRA Integration
│   ├── Customer Portal
│   ├── Google Workspace
│   └── GitHub
├── Architecture
│   ├── System Overview
│   ├── API Reference
│   └── Architecture Diagrams
├── Reference
│   ├── CLI Reference
│   ├── Configuration Files
│   └── Environment Variables
└── Troubleshooting
```

---

### Layer 4: In-App Help
**Context-sensitive help in GUI:**
- Help menu with links to docs
- ? icons next to features
- Tooltips with explanations
- Error messages with doc links

---

## 📁 File Structure

```
taminator/
├── bin/
│   ├── tam-rfe                   # Updated with --help
│   └── taminator-service         # Updated with --help
├── docs/
│   ├── man/
│   │   ├── tam-rfe.1             # Man page
│   │   ├── tam-rfe-create.1      # Subcommand man
│   │   ├── taminator-service.8   # Service man
│   │   └── taminator.conf.5      # Config man
│   ├── web/
│   │   ├── index.html            # Docs homepage
│   │   ├── getting-started/
│   │   ├── user-guide/
│   │   ├── integrations/
│   │   ├── architecture/
│   │   └── reference/
│   └── help-text/
│       ├── main-help.txt         # CLI help text
│       └── subcommand-help.txt
├── gui/
│   └── help-menu.html            # In-app help
└── ansible/
    └── deploy-docs.yml           # Deploy docs site
```

---

## 🚀 Implementation Plan

### Phase 1: CLI Help System
**Update all CLI commands:**

```python
# bin/tam-rfe with argparse
import argparse

def create_parser():
    parser = argparse.ArgumentParser(
        prog='tam-rfe',
        description='Taminator RFE/Bug tracking tool for Red Hat TAMs',
        epilog='See "tam-rfe COMMAND --help" for more information on a command.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create',
        help='Create a new RFE or Bug report',
        description='Create a new RFE (Request for Enhancement) or Bug report for a customer.',
        epilog='Example: tam-rfe create --customer td-bank --type rfe --title "Auto-scaling feature"'
    )
    create_parser.add_argument('--customer', required=True, help='Customer ID')
    create_parser.add_argument('--type', choices=['rfe', 'bug'], required=True, help='Issue type')
    # ... more options
    
    return parser
```

---

### Phase 2: Man Pages
**Create man pages in groff format:**

```groff
.TH TAM-RFE 1 "October 2025" "Taminator 2.0" "User Commands"
.SH NAME
tam-rfe \- RFE and Bug tracking tool for Red Hat TAMs
.SH SYNOPSIS
.B tam-rfe
[\fIOPTIONS\fR]
.I COMMAND
[\fICOMMAND_OPTIONS\fR]
.SH DESCRIPTION
.B tam-rfe
is a command-line tool for managing RFE (Request for Enhancement) and Bug
reports for Red Hat Technical Account Manager (TAM) workflows.
.PP
It provides integration with JIRA, Customer Portal, and Google Workspace
to streamline customer case management.
.SH COMMANDS
.TP
.B create
Create a new RFE or Bug report
.TP
.B list
List all RFE/Bug reports for a customer
.TP
.B check-jira
Check JIRA status for updates
.SH OPTIONS
.TP
.B \-h, \-\-help
Display help message and exit
.TP
.B \-\-version
Display version information and exit
.SH EXAMPLES
.TP
Create a new RFE:
.nf
tam-rfe create --customer td-bank --type rfe --title "Auto-scaling"
.fi
.TP
List all issues:
.nf
tam-rfe list --customer td-bank
.fi
.SH FILES
.TP
.I ~/.config/taminator/config.yaml
User configuration file
.TP
.I ~/Documents/rh/{customer}/
Customer data directory
.SH SEE ALSO
.BR taminator-service (8),
.BR taminator.conf (5)
.PP
Full documentation: <https://docs.taminator.local>
.SH BUGS
Report bugs to: <https://gitlab.cee.redhat.com/jbyrd/taminator/-/issues>
.SH AUTHOR
Written by Jimmy Byrd <jbyrd@redhat.com>
```

---

### Phase 3: Web Documentation
**Red Hat style documentation site:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Taminator Documentation</title>
    <link rel="stylesheet" href="https://static.redhat.com/libs/redhat/redhat-theme/latest/css/redhat.css">
    <style>
        /* Red Hat documentation style */
        body {
            font-family: "Red Hat Text", "Overpass", Arial, sans-serif;
            line-height: 1.6;
        }
        
        .docs-header {
            background: #ee0000;
            color: white;
            padding: 20px 0;
        }
        
        .docs-nav {
            background: #f5f5f5;
            border-right: 1px solid #d2d2d2;
            min-height: 100vh;
            padding: 20px;
        }
        
        .docs-content {
            padding: 40px;
            max-width: 800px;
        }
        
        .breadcrumb {
            color: #6a6e73;
            font-size: 14px;
            margin-bottom: 20px;
        }
        
        pre {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 4px;
            overflow-x: auto;
        }
        
        code {
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "Red Hat Mono", monospace;
        }
        
        .note {
            background: #e7f1fa;
            border-left: 4px solid #0066cc;
            padding: 16px;
            margin: 20px 0;
        }
        
        .warning {
            background: #fff4e5;
            border-left: 4px solid #f0ab00;
            padding: 16px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <header class="docs-header">
        <div class="container">
            <h1>Taminator Documentation</h1>
            <p>Professional TAM automation for Red Hat</p>
        </div>
    </header>
    
    <div class="container">
        <div class="row">
            <nav class="col-md-3 docs-nav">
                <ul>
                    <li><a href="#getting-started">Getting Started</a></li>
                    <li><a href="#installation">Installation</a></li>
                    <li><a href="#user-guide">User Guide</a>
                        <ul>
                            <li><a href="#creating-rfes">Creating RFEs</a></li>
                            <li><a href="#tracking-bugs">Tracking Bugs</a></li>
                            <li><a href="#customer-mgmt">Customer Management</a></li>
                        </ul>
                    </li>
                    <li><a href="#integrations">Integrations</a>
                        <ul>
                            <li><a href="#jira">JIRA</a></li>
                            <li><a href="#portal">Customer Portal</a></li>
                            <li><a href="#google">Google Workspace</a></li>
                        </ul>
                    </li>
                    <li><a href="#architecture">Architecture</a></li>
                    <li><a href="#cli-reference">CLI Reference</a></li>
                    <li><a href="#troubleshooting">Troubleshooting</a></li>
                </ul>
            </nav>
            
            <main class="col-md-9 docs-content">
                <div class="breadcrumb">
                    Home > Getting Started
                </div>
                
                <h1>Getting Started with Taminator</h1>
                
                <p>Taminator is a professional automation tool for Red Hat Technical Account Managers...</p>
                
                <div class="note">
                    <strong>Note:</strong> This documentation assumes you have a Red Hat account and access to internal systems.
                </div>
                
                <h2>Quick Start</h2>
                <pre><code># Install Taminator
sudo rpm -i taminator-2.0.0.rpm

# Start the service
systemctl --user start taminator

# Launch GUI
taminator

# Or use CLI
tam-rfe --help</code></pre>
                
                <h2>Next Steps</h2>
                <ul>
                    <li><a href="#installation">Complete Installation Guide</a></li>
                    <li><a href="#user-guide">User Guide</a></li>
                    <li><a href="#cli-reference">CLI Reference</a></li>
                </ul>
            </main>
        </div>
    </div>
</body>
</html>
```

---

### Phase 4: In-App Help Links
**Add help menu to GUI:**

```html
<!-- Help menu in main.html -->
<div class="help-menu">
    <button onclick="openDocs()">📚 Documentation</button>
    <button onclick="openHelp('getting-started')">🚀 Getting Started</button>
    <button onclick="openHelp('cli-reference')">⌨️ CLI Reference</button>
    <button onclick="openHelp('integrations')">🔗 Integrations</button>
    <button onclick="openHelp('troubleshooting')">🔧 Troubleshooting</button>
</div>

<script>
function openDocs() {
    window.open('https://docs.taminator.local', '_blank');
}

function openHelp(section) {
    window.open(`https://docs.taminator.local/#${section}`, '_blank');
}
</script>
```

---

## 🎨 Red Hat Design System

### Documentation Portal Design
**Following docs.redhat.com style:**

- **Colors**: Red Hat red (#ee0000), white, grays
- **Fonts**: Red Hat Text, Red Hat Display, Red Hat Mono
- **Layout**: Left sidebar navigation, main content, right TOC
- **Components**: Breadcrumbs, notes, warnings, code blocks
- **Icons**: Red Hat icon library

### Man Page Style
**Following standard Unix conventions:**
- Section 1: User commands (tam-rfe)
- Section 5: Configuration files (taminator.conf)
- Section 8: System administration (taminator-service)

---

## 🔧 Deployment

### Install Man Pages
```bash
# Copy man pages to system
sudo cp docs/man/tam-rfe.1 /usr/share/man/man1/
sudo cp docs/man/taminator-service.8 /usr/share/man/man8/
sudo mandb  # Update man database

# Test
man tam-rfe
```

### Deploy Web Documentation
```yaml
# ansible/deploy-docs.yml
- name: Deploy Taminator documentation
  hosts: miraclemax
  become: yes
  
  tasks:
    - name: Create docs directory
      file:
        path: /var/www/docs.taminator.local
        state: directory
        owner: www-data
        mode: '0755'
    
    - name: Copy documentation files
      synchronize:
        src: ../docs/web/
        dest: /var/www/docs.taminator.local/
    
    - name: Configure nginx
      template:
        src: nginx-docs.conf.j2
        dest: /etc/nginx/sites-available/docs.taminator.local
      notify: reload nginx
    
    - name: Enable site
      file:
        src: /etc/nginx/sites-available/docs.taminator.local
        dest: /etc/nginx/sites-enabled/docs.taminator.local
        state: link
```

---

## 📝 Documentation Standards

### CLI Help Format
```
USAGE:
    tam-rfe [OPTIONS] COMMAND [ARGS]

COMMANDS:
    create        Create a new RFE or Bug report
    list          List all reports for a customer
    check-jira    Check JIRA for status updates
    update        Update an existing report
    delete        Delete a report

OPTIONS:
    -h, --help       Print help information
    -V, --version    Print version information
    -v, --verbose    Verbose output
    -q, --quiet      Suppress output

EXAMPLES:
    # Create a new RFE
    tam-rfe create --customer td-bank --type rfe --title "Feature request"
    
    # List all issues
    tam-rfe list --customer td-bank
    
    # Check JIRA status
    tam-rfe check-jira --customer td-bank

SEE ALSO:
    man tam-rfe              Full manual page
    man tam-rfe-create       Create command details
    https://docs.taminator.local   Web documentation
```

### Web Documentation Format
**Each page includes:**
- Title and description
- Prerequisites
- Step-by-step instructions
- Code examples
- Screenshots (when helpful)
- Related topics
- Feedback link

---

## 🎯 Success Criteria

✅ Every CLI command has `--help`  
✅ Man pages installed and accessible  
✅ Web docs deployed and browsable  
✅ In-app help links functional  
✅ Architecture diagrams included  
✅ Integration guides complete  
✅ Follows Red Hat design system  
✅ Professional documentation quality  

---

*Taminator Documentation System - Enterprise Standard*  
*Red Hat Professional Documentation*


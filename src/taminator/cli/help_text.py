"""
Unified Help Text System

Single source of truth for all documentation:
- CLI --help flags
- Man pages
- Web documentation

Following the Unified Philosophy: Write once, render everywhere.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CommandHelp:
    """Unified help text for a command"""
    name: str
    summary: str
    description: str
    usage: List[str]
    options: List[Dict[str, str]]
    examples: List[Dict[str, str]]
    see_also: List[str]
    category: str


# =============================================================================
# MAIN COMMAND
# =============================================================================

TAMINATOR_HELP = CommandHelp(
    name="taminator",
    summary="Professional TAM automation tool for Red Hat workflows",
    description="""
Taminator provides a unified interface for TAM (Technical Account Manager) 
workflows, including case management, customer engagement, and automation.

All features are accessible through both GUI and CLI interfaces, with 
consistent behavior across all platforms.
    """.strip(),
    usage=[
        "taminator [OPTIONS] COMMAND [ARGS]...",
        "taminator --gui",
        "taminator --version"
    ],
    options=[
        {
            "flag": "--gui",
            "description": "Launch graphical user interface (default)"
        },
        {
            "flag": "--version",
            "description": "Show version and exit"
        },
        {
            "flag": "--help",
            "description": "Show this help message and exit"
        },
        {
            "flag": "--log-level LEVEL",
            "description": "Set logging level (DEBUG, INFO, WARNING, ERROR)"
        }
    ],
    examples=[
        {
            "command": "taminator",
            "description": "Launch GUI (default)"
        },
        {
            "command": "taminator --version",
            "description": "Show version information"
        }
    ],
    see_also=[
        "tam-rfe(1) - RFE/Bug report creation",
        "taminator-service(1) - Backend service management",
        "docs.taminator.local - Complete web documentation"
    ],
    category="Core"
)


# =============================================================================
# TAM-RFE COMMAND
# =============================================================================

TAM_RFE_HELP = CommandHelp(
    name="tam-rfe",
    summary="Create RFE (Request for Enhancement) and Bug reports",
    description="""
Create professional RFE and Bug reports from the command line. Supports
interactive and non-interactive modes for automation.

Reports are created using Red Hat approved AI models with proper TAM
formatting and submission to JIRA.
    """.strip(),
    usage=[
        "tam-rfe [OPTIONS] COMMAND [ARGS]...",
        "tam-rfe create [--type TYPE] [--customer CUSTOMER]",
        "tam-rfe gui"
    ],
    options=[
        {
            "flag": "--help",
            "description": "Show this help message and exit"
        },
        {
            "flag": "--version",
            "description": "Show version and exit"
        },
        {
            "flag": "--non-interactive",
            "description": "Run without prompts (for automation)"
        }
    ],
    examples=[
        {
            "command": "tam-rfe create --type rfe",
            "description": "Create new RFE report (interactive)"
        },
        {
            "command": "tam-rfe create --type bug --customer acme",
            "description": "Create bug report for ACME customer"
        },
        {
            "command": "tam-rfe gui",
            "description": "Open GUI report creator"
        },
        {
            "command": "tam-rfe list --customer acme",
            "description": "List reports for ACME customer"
        }
    ],
    see_also=[
        "tam-rfe-create(1) - Detailed creation options",
        "taminator(1) - Main application",
        "docs.taminator.local/guides/rfe.html - RFE creation guide"
    ],
    category="Reports"
)


TAM_RFE_CREATE_HELP = CommandHelp(
    name="tam-rfe create",
    summary="Create a new RFE or Bug report",
    description="""
Create professional RFE (Request for Enhancement) or Bug reports with
AI-assisted content generation.

Interactive mode guides you through all required fields. Non-interactive
mode accepts all parameters via flags for automation.
    """.strip(),
    usage=[
        "tam-rfe create [OPTIONS]",
        "tam-rfe create --type rfe --customer CUSTOMER",
        "tam-rfe create --type bug --severity high"
    ],
    options=[
        {
            "flag": "--type TYPE",
            "description": "Report type: 'rfe' or 'bug' (required)"
        },
        {
            "flag": "--customer CUSTOMER",
            "description": "Customer name/ID (required)"
        },
        {
            "flag": "--title TITLE",
            "description": "Report title (interactive if omitted)"
        },
        {
            "flag": "--description TEXT",
            "description": "Report description (interactive if omitted)"
        },
        {
            "flag": "--severity LEVEL",
            "description": "Bug severity: low, medium, high, critical"
        },
        {
            "flag": "--priority LEVEL",
            "description": "RFE priority: low, medium, high"
        },
        {
            "flag": "--ai-enhance",
            "description": "Use AI to enhance description (default: true)"
        },
        {
            "flag": "--no-ai",
            "description": "Disable AI enhancement"
        },
        {
            "flag": "--draft",
            "description": "Save as draft without submitting"
        },
        {
            "flag": "--output FILE",
            "description": "Save report to file (markdown format)"
        }
    ],
    examples=[
        {
            "command": "tam-rfe create --type rfe",
            "description": "Create RFE with interactive prompts"
        },
        {
            "command": "tam-rfe create --type bug --customer acme --severity high",
            "description": "Create high-severity bug for ACME"
        },
        {
            "command": "tam-rfe create --type rfe --draft --output report.md",
            "description": "Create draft RFE and save to file"
        },
        {
            "command": "tam-rfe create --type bug --no-ai --customer acme",
            "description": "Create bug without AI enhancement"
        }
    ],
    see_also=[
        "tam-rfe(1) - Main RFE command",
        "tam-rfe-list(1) - List existing reports",
        "docs.taminator.local/guides/rfe-creation.html"
    ],
    category="Reports"
)


# =============================================================================
# AUTH COMMAND
# =============================================================================

TAM_AUTH_HELP = CommandHelp(
    name="tam-rfe auth",
    summary="Manage authentication tokens (unified token system)",
    description="""
Manage authentication tokens for all integrations through the unified
token management system.

All tokens are stored securely in the system keyring and accessible
across GUI and CLI interfaces.
    """.strip(),
    usage=[
        "tam-rfe auth COMMAND [OPTIONS]",
        "tam-rfe auth status",
        "tam-rfe auth login SERVICE",
        "tam-rfe auth logout SERVICE"
    ],
    options=[
        {
            "flag": "--help",
            "description": "Show this help message and exit"
        }
    ],
    examples=[
        {
            "command": "tam-rfe auth status",
            "description": "Show authentication status for all services"
        },
        {
            "command": "tam-rfe auth login jira",
            "description": "Configure JIRA authentication"
        },
        {
            "command": "tam-rfe auth login google",
            "description": "Sign in with Google (opens browser)"
        },
        {
            "command": "tam-rfe auth logout portal",
            "description": "Remove Customer Portal token"
        },
        {
            "command": "tam-rfe auth test jira",
            "description": "Test JIRA connection"
        }
    ],
    see_also=[
        "tam-rfe(1) - Main command",
        "docs.taminator.local/guides/authentication.html",
        "docs.taminator.local/architecture/token-manager.html"
    ],
    category="Authentication"
)


# =============================================================================
# SERVICE COMMAND
# =============================================================================

TAMINATOR_SERVICE_HELP = CommandHelp(
    name="taminator-service",
    summary="Manage Taminator backend service",
    description="""
Control the Taminator FastAPI backend service. The service provides
a unified API for all integrations and features.

Service management is typically handled automatically by the GUI, but
CLI control is available for debugging and automation.
    """.strip(),
    usage=[
        "taminator-service [COMMAND]",
        "taminator-service start",
        "taminator-service status"
    ],
    options=[
        {
            "flag": "start",
            "description": "Start the service (default)"
        },
        {
            "flag": "stop",
            "description": "Stop the service gracefully"
        },
        {
            "flag": "status",
            "description": "Show service status and health"
        },
        {
            "flag": "restart",
            "description": "Restart the service"
        },
        {
            "flag": "logs",
            "description": "Show service logs (real-time)"
        },
        {
            "flag": "--port PORT",
            "description": "Service port (default: 8765)"
        },
        {
            "flag": "--log-level LEVEL",
            "description": "Logging level (default: INFO)"
        }
    ],
    examples=[
        {
            "command": "taminator-service",
            "description": "Start service on default port"
        },
        {
            "command": "taminator-service status",
            "description": "Check if service is running"
        },
        {
            "command": "taminator-service logs",
            "description": "Tail service logs"
        },
        {
            "command": "taminator-service restart",
            "description": "Restart service (apply config changes)"
        }
    ],
    see_also=[
        "taminator(1) - Main application",
        "docs.taminator.local/admin/service-management.html",
        "docs.taminator.local/architecture/api-service.html"
    ],
    category="Administration"
)


# =============================================================================
# HELP TEXT RENDERING
# =============================================================================

def render_cli_help(help_obj: CommandHelp, color: bool = True) -> str:
    """
    Render help text for CLI --help output
    
    Args:
        help_obj: CommandHelp object
        color: Use ANSI colors (default: True)
        
    Returns:
        Formatted help text for terminal
    """
    lines = []
    
    # Header
    if color:
        lines.append(f"\033[1m{help_obj.name}\033[0m - {help_obj.summary}")
    else:
        lines.append(f"{help_obj.name} - {help_obj.summary}")
    
    lines.append("")
    
    # Description
    lines.append("DESCRIPTION")
    for line in help_obj.description.split('\n'):
        lines.append(f"    {line}")
    lines.append("")
    
    # Usage
    lines.append("USAGE")
    for usage in help_obj.usage:
        lines.append(f"    {usage}")
    lines.append("")
    
    # Options
    if help_obj.options:
        lines.append("OPTIONS")
        for opt in help_obj.options:
            flag = opt['flag']
            desc = opt['description']
            if color:
                lines.append(f"    \033[1m{flag}\033[0m")
            else:
                lines.append(f"    {flag}")
            lines.append(f"        {desc}")
        lines.append("")
    
    # Examples
    if help_obj.examples:
        lines.append("EXAMPLES")
        for ex in help_obj.examples:
            lines.append(f"    # {ex['description']}")
            if color:
                lines.append(f"    \033[36m$ {ex['command']}\033[0m")
            else:
                lines.append(f"    $ {ex['command']}")
            lines.append("")
    
    # See Also
    if help_obj.see_also:
        lines.append("SEE ALSO")
        for ref in help_obj.see_also:
            lines.append(f"    {ref}")
        lines.append("")
    
    return '\n'.join(lines)


def render_man_page(help_obj: CommandHelp) -> str:
    """
    Render help text as Unix man page (groff format)
    
    Args:
        help_obj: CommandHelp object
        
    Returns:
        Man page in groff format
    """
    lines = []
    
    # Man page header
    lines.append(f'.TH {help_obj.name.upper().replace(" ", "-")} 1 "2025" "Taminator v2.0" "Taminator Manual"')
    lines.append("")
    
    # Name section
    lines.append(".SH NAME")
    lines.append(f"{help_obj.name} \\- {help_obj.summary}")
    lines.append("")
    
    # Synopsis
    lines.append(".SH SYNOPSIS")
    for usage in help_obj.usage:
        lines.append(f".B {usage}")
        lines.append(".br")
    lines.append("")
    
    # Description
    lines.append(".SH DESCRIPTION")
    for line in help_obj.description.split('\n'):
        if line.strip():
            lines.append(line.strip())
    lines.append("")
    
    # Options
    if help_obj.options:
        lines.append(".SH OPTIONS")
        for opt in help_obj.options:
            lines.append(f".TP")
            lines.append(f".B {opt['flag']}")
            lines.append(opt['description'])
        lines.append("")
    
    # Examples
    if help_obj.examples:
        lines.append(".SH EXAMPLES")
        for ex in help_obj.examples:
            lines.append(f".TP")
            lines.append(f".B {ex['command']}")
            lines.append(ex['description'])
        lines.append("")
    
    # See Also
    if help_obj.see_also:
        lines.append(".SH SEE ALSO")
        see_also_text = ", ".join(help_obj.see_also)
        lines.append(see_also_text)
        lines.append("")
    
    # Footer
    lines.append(".SH AUTHOR")
    lines.append("Taminator is developed and maintained by the Red Hat TAM team.")
    lines.append("")
    lines.append(".SH REPORTING BUGS")
    lines.append("Report bugs to: https://gitlab.cee.redhat.com/jbyrd/taminator/issues")
    lines.append("")
    
    return '\n'.join(lines)


def get_help_text(command: str) -> Optional[CommandHelp]:
    """
    Get help text for a command
    
    Args:
        command: Command name (e.g., 'taminator', 'tam-rfe', 'tam-rfe create')
        
    Returns:
        CommandHelp object or None if not found
    """
    help_map = {
        'taminator': TAMINATOR_HELP,
        'tam-rfe': TAM_RFE_HELP,
        'tam-rfe create': TAM_RFE_CREATE_HELP,
        'tam-rfe auth': TAM_AUTH_HELP,
        'taminator-service': TAMINATOR_SERVICE_HELP,
    }
    
    return help_map.get(command)


# =============================================================================
# CLI INTEGRATION
# =============================================================================

def show_help(command: str, color: bool = True):
    """
    Show help for a command (used by CLI --help)
    
    Args:
        command: Command name
        color: Use ANSI colors
    """
    help_obj = get_help_text(command)
    
    if not help_obj:
        print(f"No help available for command: {command}")
        return
    
    print(render_cli_help(help_obj, color=color))


# =============================================================================
# WEB DOCUMENTATION INTEGRATION
# =============================================================================

def render_web_html(help_obj: CommandHelp) -> str:
    """
    Render help text as HTML for web documentation
    
    Args:
        help_obj: CommandHelp object
        
    Returns:
        HTML string for web docs
    """
    html = []
    
    html.append(f'<h1>{help_obj.name}</h1>')
    html.append(f'<p class="summary">{help_obj.summary}</p>')
    
    html.append('<h2>Description</h2>')
    html.append(f'<div class="description">{help_obj.description.replace(chr(10), "<br>")}</div>')
    
    html.append('<h2>Usage</h2>')
    html.append('<pre class="usage">')
    for usage in help_obj.usage:
        html.append(f'{usage}\n')
    html.append('</pre>')
    
    if help_obj.options:
        html.append('<h2>Options</h2>')
        html.append('<dl class="options">')
        for opt in help_obj.options:
            html.append(f'<dt><code>{opt["flag"]}</code></dt>')
            html.append(f'<dd>{opt["description"]}</dd>')
        html.append('</dl>')
    
    if help_obj.examples:
        html.append('<h2>Examples</h2>')
        for ex in help_obj.examples:
            html.append(f'<div class="example">')
            html.append(f'<p class="example-description">{ex["description"]}</p>')
            html.append(f'<pre class="example-command">$ {ex["command"]}</pre>')
            html.append('</div>')
    
    if help_obj.see_also:
        html.append('<h2>See Also</h2>')
        html.append('<ul class="see-also">')
        for ref in help_obj.see_also:
            html.append(f'<li>{ref}</li>')
        html.append('</ul>')
    
    return '\n'.join(html)


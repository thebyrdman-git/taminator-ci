"""
tam-rfe onboard: Interactive customer onboarding wizard.

Guides TAM through onboarding a new customer:
1. Customer information collection
2. Initial RFE/Bug discovery
3. Report template creation
4. Configuration setup

Usage:
    tam-rfe onboard <customer>
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from ..core.hybrid_auth import hybrid_auth
from ..core.auth_box import auth_required, AuthType

console = Console()


class CustomerOnboarder:
    """Customer onboarding wizard."""
    
    @staticmethod
    def create_customer_report_template(customer_name: str, customer_info: Dict) -> str:
        """
        Create initial report template for customer.
        
        Args:
            customer_name: Customer name
            customer_info: Dictionary with customer details
        
        Returns:
            Report markdown content
        """
        timestamp = datetime.now().strftime('%b %d, %Y, %I:%M %p %Z')
        
        template = f"""# {customer_info.get('display_name', customer_name)} RFE/Bug Tracker

{timestamp} Jimmy Byrd

Summary: 0 total cases (0 RFE, 0 Bug)

## Customer Information

- **Account:** {customer_info.get('account', 'TBD')}
- **Primary Contact:** {customer_info.get('contact', 'TBD')}
- **TAM:** {customer_info.get('tam', 'Jimmy Byrd')}

## Enhancement Requests (RFE)

| RED HAT JIRA ID | Support Case | Enhancement Request | Status |
|-----------------|--------------|---------------------|--------|
| | | | |

*No RFEs tracked yet. Use `tam-rfe update {customer_name}` to add RFEs.*

## Bug Reports

| RED HAT JIRA ID | Support Case | Bug Description | Status |
|-----------------|--------------|-----------------|--------|
| | | | |

*No bugs tracked yet. Use `tam-rfe update {customer_name}` to add bugs.*

---

**Notes:**
- This tracker is automatically updated via Taminator
- Last check: {timestamp}
- For questions, contact Jimmy Byrd (jbyrd@redhat.com)
"""
        return template


@auth_required([AuthType.VPN])
def onboard_customer(customer_name: str, email: str = None, display_name: str = None,
                     non_interactive: bool = False, json_output: bool = False):
    """
    Interactive or automated customer onboarding wizard (Red Hat CLI pattern).
    
    Args:
        customer_name: Customer name (slug format, e.g., 'acmecorp')
        email: TAM email address (required for non-interactive mode)
        display_name: Customer display name (required for non-interactive mode)
        non_interactive: If True, run without prompts (automation mode)
        json_output: If True, output structured JSON for machine parsing
    
    Red Hat Design Pattern:
        Interactive mode: tam-rfe onboard acmecorp
        Automation mode:  tam-rfe onboard acmecorp --email user@redhat.com --display-name "Acme Corp" --non-interactive --json
    """
    import json
    
    # Validate non-interactive mode requirements
    if non_interactive:
        if not email or not display_name:
            error_msg = "Non-interactive mode requires --email and --display-name"
            if json_output:
                print(json.dumps({"success": False, "error": error_msg}))
            else:
                console.print(f"\n❌ Error: {error_msg}", style="red bold")
                console.print("\nUsage for automation:", style="cyan")
                console.print(f"  tam-rfe onboard {customer_name} --email user@redhat.com --display-name 'Customer Name' --non-interactive")
            return 1
    # Interactive mode: Show welcome banner
    if not non_interactive:
        console.print()
        console.print("╔════════════════════════════════════════════════════════════╗", style="cyan bold")
        console.print("║          CUSTOMER ONBOARDING WIZARD                        ║", style="cyan bold")
        console.print("╚════════════════════════════════════════════════════════════╝", style="cyan bold")
        console.print()
        
        welcome = f"""
Welcome to the Taminator Customer Onboarding Wizard!

This wizard will help you set up RFE/Bug tracking for:
  {customer_name}

We'll collect some information and create an initial tracking report.
"""
        console.print(Panel(welcome, border_style="cyan", title="🎯 Getting Started"))
        console.print()
        
        if not Confirm.ask("Ready to begin?", default=True):
            console.print("\n❌ Onboarding cancelled.\n", style="yellow")
            return 0
        
        console.print()
        console.print("═══ Step 1: Customer Information ═══\n", style="cyan bold")
    
    # Collect customer information (interactive or use provided values)
    customer_info = {}
    
    if non_interactive:
        # Automation mode: Use provided values
        customer_info['display_name'] = display_name
        customer_info['account'] = "TBD"
        customer_info['contact'] = "TBD"
        customer_info['tam'] = "Jimmy Byrd"
    else:
        # Interactive mode: Prompt with defaults
        customer_info['display_name'] = display_name or Prompt.ask(
            "Customer display name",
            default=customer_name.replace('_', ' ').title()
        )
        
        customer_info['account'] = Prompt.ask(
            "Red Hat account number",
            default="TBD"
        )
        
        customer_info['contact'] = Prompt.ask(
            "Primary contact name",
            default="TBD"
        )
        
        customer_info['tam'] = Prompt.ask(
            "TAM name",
            default="Jimmy Byrd"
        )
    
    if not non_interactive:
        console.print()
        console.print("═══ Step 2: Report Location ═══\n", style="cyan bold")
    
    # Determine report location
    default_dir = Path.home() / 'taminator-test-data'
    
    if non_interactive:
        # Automation mode: Use default location
        report_dir = default_dir
    else:
        # Interactive mode: Prompt for location
        console.print(f"Default location: {default_dir}/", style="dim")
        
        use_default = Confirm.ask("Use default location?", default=True)
        
        if use_default:
            report_dir = default_dir
        else:
            custom_path = Prompt.ask("Enter directory path")
            report_dir = Path(custom_path).expanduser()
    
    # Ensure directory exists
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_path = report_dir / f"{customer_name}.md"
    
    # Check if report already exists
    if report_path.exists():
        if non_interactive:
            # Automation mode: Overwrite silently
            pass
        else:
            # Interactive mode: Ask for confirmation
            console.print(f"\n⚠️  Report already exists: {report_path}", style="yellow")
            if not Confirm.ask("Overwrite existing report?", default=False):
                console.print("\n❌ Onboarding cancelled.\n", style="yellow")
                return 0
    
    if not non_interactive:
        console.print()
        console.print("═══ Step 3: Create Report ═══\n", style="cyan bold")
    
    # Create report template
    if not non_interactive:
        console.print("📝 Generating report template...", style="cyan")
    
    report_content = CustomerOnboarder.create_customer_report_template(
        customer_name,
        customer_info
    )
    
    # Write report
    with open(report_path, 'w') as f:
        f.write(report_content)
    
    # Output results based on mode
    if json_output:
        # Machine-readable JSON output (Red Hat automation pattern)
        import json
        result = {
            "success": True,
            "customer": {
                "name": customer_name,
                "display_name": customer_info['display_name'],
                "slug": customer_name
            },
            "report": {
                "path": str(report_path),
                "directory": str(report_dir)
            }
        }
        print(json.dumps(result, indent=2))
    elif non_interactive:
        # Non-interactive but human-readable
        console.print(f"✅ Report created: {report_path}", style="green")
    else:
        # Interactive mode: Full summary
        console.print(f"✅ Report created: {report_path}", style="green")
        console.print()
        
        summary = f"""
╔═══════════════════════════════════════════════════════════╗
║                  ONBOARDING COMPLETE                      ║
╚═══════════════════════════════════════════════════════════╝

  Customer: {customer_info['display_name']}
  Report: {report_path.name}
  Location: {report_dir}/
  
  Status: ✅ SUCCESS

Next Steps:
  1. Review the report: {report_path}
  2. Add JIRA IDs to the tables manually
  3. Run: tam-rfe check {customer_name}
  4. Run: tam-rfe update {customer_name}

Need help?
  • Documentation: https://gitlab.cee.redhat.com/jbyrd/taminator
  • Contact: jbyrd@redhat.com
"""
        
        console.print(summary, style="green bold")
        
        # Offer to open report
        if Confirm.ask("View the new report now?", default=True):
            console.print("\n" + "="*70 + "\n")
            console.print(report_content)
            console.print("\n" + "="*70 + "\n")
    
    return 0


# CLI entry point
def main(customer: str = None, email: str = None, display_name: str = None,
         non_interactive: bool = False, json_output: bool = False):
    """Main entry point for tam-rfe onboard command (Red Hat CLI pattern)."""
    
    if not customer:
        console.print("\n❌ Error: Customer name required", style="red bold")
        console.print("\nUsage:", style="cyan")
        console.print("  tam-rfe onboard <customer>  [options]")
        console.print("\nInteractive mode:", style="cyan")
        console.print("  tam-rfe onboard acmecorp")
        console.print("\nAutomation mode (non-interactive):", style="cyan")
        console.print("  tam-rfe onboard acmecorp --email user@redhat.com --display-name 'Acme Corp' --non-interactive")
        console.print("  tam-rfe onboard acmecorp --email user@redhat.com --display-name 'Acme Corp' --non-interactive --json")
        console.print("\nCustomer name should be:")
        console.print("  • Lowercase")
        console.print("  • No spaces (use underscores)")
        console.print("  • Example: 'acme_corp' or 'acmecorp'")
        return 1
    
    return onboard_customer(customer, email=email, display_name=display_name,
                           non_interactive=non_interactive, json_output=json_output)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        main(customer=sys.argv[1])
    else:
        main()


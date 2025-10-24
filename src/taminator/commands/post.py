"""
tam-rfe post: Post RFE/Bug tracker to Red Hat Customer Portal.

Posts the formatted report to customer portal group page.

Usage:
    tam-rfe post <customer>
    tam-rfe post --dry-run <customer>
"""

import os
import sys
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from ..core.hybrid_auth import hybrid_auth
from ..core.auth_box import auth_required, AuthType
from .check import CustomerReportParser

# Import Portal API client from src directory
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from redhat_portal_api_client import RedHatPortalAPIClient

console = Console()


@auth_required([AuthType.VPN, AuthType.PORTAL_TOKEN])
def post_customer_report(customer_name: str, dry_run: bool = False):
    """
    Post customer RFE report to portal.
    
    Args:
        customer_name: Customer name
        dry_run: Preview without posting
    """
    console.print()
    console.print("╔════════════════════════════════════════════════════════════╗", style="cyan bold")
    console.print(f"║  tam-rfe post: {customer_name.upper():^42} ║", style="cyan bold")
    console.print("╚════════════════════════════════════════════════════════════╝", style="cyan bold")
    console.print()
    
    if dry_run:
        console.print("🧪 DRY RUN MODE - No changes will be made\n", style="yellow bold")
    
    # Find report file
    console.print(f"🔍 Searching for {customer_name} report...", style="cyan")
    report_path = CustomerReportParser.find_report(customer_name)
    
    if not report_path:
        console.print(f"\n❌ Report not found for customer: {customer_name}", style="red bold")
        return
    
    console.print(f"✅ Found report: {report_path}", style="green")
    console.print()
    
    # Read report
    with open(report_path, 'r') as f:
        report_content = f.read()
    
    # Preview
    console.print("═══ Report Preview ═══\n", style="cyan bold")
    console.print(Panel(report_content[:500] + "...", border_style="cyan", title="First 500 characters"))
    console.print()
    
    if dry_run:
        console.print("✅ Dry run complete - no changes made\n", style="green")
        console.print("Remove --dry-run flag to post for real\n")
        return
    
    # Confirm posting
    console.print("⚠️  This will post the report to the customer portal", style="yellow bold")
    
    if not Confirm.ask("Proceed with posting?", default=False):
        console.print("\n❌ Posting cancelled.\n", style="yellow")
        return
    
    # Get customer group ID
    console.print()
    console.print("🔍 Customer Group Configuration", style="cyan bold")
    console.print("\nTo post to the portal, we need the Customer Portal Group ID.", style="cyan")
    console.print("You can find this in the portal group URL:", style="cyan")
    console.print("  Example: https://access.redhat.com/group/12345", style="dim")
    console.print()
    
    group_id = Prompt.ask("Enter Customer Portal Group ID", default="")
    
    if not group_id:
        console.print("\n❌ Group ID required to post to portal", style="red bold")
        console.print("\nTip: Find the group ID in the portal group URL\n")
        return
    
    console.print()
    console.print("📤 Posting to customer portal...", style="cyan")
    
    # Initialize Portal API client
    portal_token = hybrid_auth.get_token('portal')
    
    # Note: The Portal API client uses username/password from env vars
    # We should update it to also support bearer tokens
    # For now, check if credentials are available
    if not os.getenv('REDHAT_PORTAL_USERNAME') or not os.getenv('REDHAT_PORTAL_PASSWORD'):
        console.print("\n⚠️  Portal API requires username/password authentication", style="yellow bold")
        console.print("\nSet environment variables:", style="cyan")
        console.print("  export REDHAT_PORTAL_USERNAME='your_username'")
        console.print("  export REDHAT_PORTAL_PASSWORD='your_password'")
        console.print("\nAlternatively, the Portal token can be used for direct API calls.")
        console.print("\n🚧 Full Portal API integration in progress...\n", style="yellow")
        
        # Show what would be posted
        summary = f"""
╔═══════════════════════════════════════════════════════════╗
║                    POST SUMMARY (DRY RUN)                 ║
╚═══════════════════════════════════════════════════════════╝

  Customer: {customer_name}
  Report: {report_path.name}
  Group ID: {group_id}
  
  Would post:
    Title: {customer_name.title()} RFE/Bug Tracker Update
    Body: [Report content]
    Timestamp: {datetime.now().strftime('%b %d, %Y, %I:%M %p')}
  
  Status: ⚠️  Authentication configuration needed
  
  Once configured, the report will be posted to:
  https://access.redhat.com/group/{group_id}/discussions
"""
        console.print(summary, style="yellow bold")
        return
    
    try:
        # Initialize Portal API client
        client = RedHatPortalAPIClient(environment="production")
        
        # Authenticate
        console.print("🔐 Authenticating with Portal API...", style="cyan")
        if not client.authenticate():
            console.print("\n❌ Authentication failed", style="red bold")
            return
        
        console.print("✅ Authentication successful", style="green")
        console.print()
        
        # Prepare post data
        title = f"{customer_name.title()} RFE/Bug Tracker - {datetime.now().strftime('%b %d, %Y')}"
        
        console.print(f"📝 Creating discussion: {title}", style="cyan")
        console.print()
        
        # Post to portal
        result = client.create_group_discussion(
            group_id=group_id,
            title=title,
            body=report_content,
            status="published"
        )
        
        if result and result.get('success'):
            console.print("✅ Report posted successfully!", style="green bold")
            console.print()
            
            discussion_id = result.get('discussion_id')
            portal_url = result.get('url') or f"https://access.redhat.com/group/{group_id}/discussions/{discussion_id}"
            
            summary = f"""
╔═══════════════════════════════════════════════════════════╗
║                    POST SUMMARY                           ║
╚═══════════════════════════════════════════════════════════╝

  Customer: {customer_name}
  Report: {report_path.name}
  Group ID: {group_id}
  Discussion ID: {discussion_id}
  
  Status: ✅ SUCCESS
  
  View your post:
  {portal_url}
"""
            console.print(summary, style="green bold")
        else:
            error_msg = result.get('error', 'Unknown error') if result else 'No response from API'
            console.print(f"\n❌ Failed to post to portal: {error_msg}", style="red bold")
            console.print()
            
    except Exception as e:
        console.print(f"\n❌ Error posting to portal: {str(e)}", style="red bold")
        console.print("\nThis may be due to API endpoint changes or authentication issues.", style="yellow")
        console.print("The portal API is under active development.\n")


# CLI entry point
def main(customer: str = None, dry_run: bool = False):
    """Main entry point for tam-rfe post command."""
    
    if not customer:
        console.print("\n❌ Error: Customer name required", style="red bold")
        console.print("\nUsage:", style="cyan")
        console.print("  tam-rfe post <customer>")
        console.print("  tam-rfe post --dry-run <customer>")
        console.print("\nExamples:", style="cyan")
        console.print("  tam-rfe post acmecorp")
        console.print("  tam-rfe post --dry-run exampleinc")
        return
    
    post_customer_report(customer, dry_run=dry_run)


if __name__ == '__main__':
    import sys
    
    dry_run = '--dry-run' in sys.argv
    
    # Get customer name (first non-flag argument)
    customer = None
    for arg in sys.argv[1:]:
        if not arg.startswith('--'):
            customer = arg
            break
    
    main(customer=customer, dry_run=dry_run)


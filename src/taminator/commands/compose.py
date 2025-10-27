"""
tam-rfe compose: AI-powered email composer for customer communications

Generates professional customer emails about RFE/Bug updates using AI.
"""

import json
import argparse
from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from ..core.ai_client import get_ai_client

console = Console()


def compose_email(args: argparse.Namespace) -> int:
    """
    Compose customer email using AI.
    
    Args:
        args: Command line arguments
    
    Returns:
        Exit code (0 for success)
    """
    
    # Get AI client
    ai_client = get_ai_client()
    
    if not ai_client.is_available():
        console.print("[yellow]⚠️  AI features not available[/yellow]")
        console.print("[yellow]   Install dependencies: pip install openai tiktoken[/yellow]")
        console.print("[yellow]   Or ensure LiteLLM proxy is running on localhost:4000[/yellow]")
        if not args.json:
            console.print()
            console.print("Falling back to template-based generation...")
    
    # Parse RFEs/Bugs from JSON string or file
    rfes_bugs = []
    if args.rfes:
        try:
            rfes_bugs = json.loads(args.rfes)
        except json.JSONDecodeError:
            console.print("[red]❌ Invalid JSON for RFEs/Bugs[/red]")
            return 1
    
    # Generate email
    try:
        result = ai_client.generate_email(
            customer_name=args.customer,
            email_type=args.type,
            rfes_bugs=rfes_bugs,
            additional_context=args.context or "",
            tone=args.tone
        )
        
        # Output format
        if args.json:
            # JSON output for GUI
            output = {
                "success": True,
                "subject": result["subject"],
                "body": result["body"],
                "ai_generated": ai_client.is_available()
            }
            print(json.dumps(output))
        else:
            # Pretty output for CLI
            console.print()
            console.print(Panel(
                f"[bold cyan]Subject:[/bold cyan] {result['subject']}",
                title="✉️ Generated Email",
                border_style="cyan"
            ))
            console.print()
            console.print(Panel(
                result['body'],
                title="Email Body",
                border_style="blue"
            ))
            console.print()
            
            if ai_client.is_available():
                console.print("[green]✅ Generated using AI (Red Hat Granite)[/green]")
            else:
                console.print("[yellow]📝 Generated using templates (AI unavailable)[/yellow]")
        
        return 0
        
    except Exception as e:
        console.print(f"[red]❌ Error generating email: {e}[/red]")
        if args.json:
            print(json.dumps({"success": False, "error": str(e)}))
        return 1


def main():
    """Main entry point for tam-rfe compose command."""
    parser = argparse.ArgumentParser(
        description="AI-powered email composer for customer communications"
    )
    
    parser.add_argument(
        'customer',
        help='Customer name'
    )
    
    parser.add_argument(
        '--type',
        choices=['status_update', 'specific_update', 'action_required', 'good_news', 'custom'],
        default='status_update',
        help='Type of email to generate'
    )
    
    parser.add_argument(
        '--rfes',
        help='JSON array of RFEs/Bugs to include (format: [{"id":"AAP-123","summary":"...","status":"..."}])'
    )
    
    parser.add_argument(
        '--context',
        help='Additional context for the email'
    )
    
    parser.add_argument(
        '--tone',
        choices=['professional', 'formal', 'casual', 'technical'],
        default='professional',
        help='Email tone'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in JSON format (for GUI integration)'
    )
    
    args = parser.parse_args()
    return compose_email(args)


if __name__ == '__main__':
    exit(main())


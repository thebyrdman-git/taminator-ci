#!/usr/bin/env python3
"""
Taminator CLI - Command Line Interface Router

Routes CLI commands to appropriate command modules.

Usage:
    tam-rfe check <customer>
    tam-rfe update <customer>
    tam-rfe post <customer>
    tam-rfe onboard <customer>
    tam-rfe config [options]
"""

import sys
import argparse
from pathlib import Path


def main():
    """Main CLI entry point."""
    
    parser = argparse.ArgumentParser(
        prog='tam-rfe',
        description='Taminator RFE Tool - TAM workflow automation for tracking RFEs and Bugs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tam-rfe check acmecorp            Check Acme Corp report status
  tam-rfe update exampleinc         Update Example Inc report
  tam-rfe post bigcustomer          Post Big Customer report to portal
  tam-rfe onboard newcustomer       Onboard new customer
  tam-rfe config --add-token        Add authentication token

For more help on a command:
  tam-rfe <command> --help
        """
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        required=True
    )
    
    # ========================================
    # CHECK command
    # ========================================
    check_parser = subparsers.add_parser(
        'check',
        help='Check customer RFE/Bug report status',
        description='Compare report JIRA statuses with current JIRA data'
    )
    check_parser.add_argument(
        'customer',
        nargs='?',
        help='Customer name (e.g., acmecorp, exampleinc)'
    )
    check_parser.add_argument(
        '--test-data',
        action='store_true',
        help='Use sample test data instead of real customer'
    )
    
    # ========================================
    # UPDATE command
    # ========================================
    update_parser = subparsers.add_parser(
        'update',
        help='Update customer RFE/Bug report with current JIRA statuses',
        description='Auto-update report file with current JIRA data'
    )
    update_parser.add_argument(
        'customer',
        nargs='?',
        help='Customer name'
    )
    update_parser.add_argument(
        '--test-data',
        action='store_true',
        help='Use sample test data'
    )
    update_parser.add_argument(
        '--auto-confirm',
        action='store_true',
        help='Skip confirmation prompts'
    )
    
    # ========================================
    # POST command
    # ========================================
    post_parser = subparsers.add_parser(
        'post',
        help='Post RFE/Bug report to Red Hat Customer Portal',
        description='Upload report to customer portal group page'
    )
    post_parser.add_argument(
        'customer',
        nargs='?',
        help='Customer name'
    )
    post_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview without actually posting'
    )
    
    # ========================================
    # ONBOARD command
    # ========================================
    onboard_parser = subparsers.add_parser(
        'onboard',
        help='Onboard new customer',
        description='Interactive or automated customer onboarding (Red Hat CLI pattern)'
    )
    onboard_parser.add_argument(
        'customer',
        nargs='?',
        help='Customer name (e.g., acmecorp, jpmc)'
    )
    onboard_parser.add_argument(
        '--email',
        metavar='EMAIL',
        help='TAM email address (required for --non-interactive)'
    )
    onboard_parser.add_argument(
        '--display-name',
        metavar='NAME',
        help='Customer display name (required for --non-interactive)'
    )
    onboard_parser.add_argument(
        '--account',
        metavar='NUMBER',
        help='Red Hat account number (REQUIRED: enterprise customers have multiple accounts)'
    )
    onboard_parser.add_argument(
        '--product',
        metavar='PRODUCT',
        help='Red Hat product (REQUIRED: filters JIRA by SBR group, e.g., RHEL, Ansible, OpenShift)'
    )
    onboard_parser.add_argument(
        '--non-interactive',
        action='store_true',
        help='Run without prompts (automation mode)'
    )
    onboard_parser.add_argument(
        '--json',
        action='store_true',
        dest='json_output',
        help='Output structured JSON for machine parsing'
    )
    onboard_parser.add_argument(
        '--discover',
        metavar='NAME',
        help='Auto-discover customer information (deprecated, use --non-interactive)'
    )
    onboard_parser.add_argument(
        '--generate',
        action='store_true',
        help='Generate customer configuration (not yet implemented)'
    )
    
    # ========================================
    # GUI command
    # ========================================
    gui_parser = subparsers.add_parser(
        'gui',
        help='Launch Taminator GUI',
        description='Open the Taminator graphical interface (cross-platform)'
    )
    
    # ========================================
    # CONFIG command
    # ========================================
    config_parser = subparsers.add_parser(
        'config',
        help='Manage Taminator configuration',
        description='Configure authentication tokens and settings'
    )
    config_parser.add_argument(
        '--add-token',
        action='store_true',
        help='Add authentication token interactively'
    )
    config_parser.add_argument(
        '--setup-vault',
        action='store_true',
        help='Configure HashiCorp Vault for centralized token management'
    )
    config_parser.add_argument(
        '--test-tokens',
        action='store_true',
        help='Test all configured tokens'
    )
    config_parser.add_argument(
        '--show-tokens',
        action='store_true',
        help='Show configured token types'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Route to appropriate command
    try:
        if args.command == 'check':
            from taminator.commands.check import main as check_main
            check_main(
                customer=args.customer,
                test_data=args.test_data
            )
        
        elif args.command == 'update':
            from taminator.commands.update import main as update_main
            update_main(
                customer=args.customer,
                test_data=args.test_data,
                auto_confirm=args.auto_confirm
            )
        
        elif args.command == 'post':
            from taminator.commands.post import main as post_main
            post_main(
                customer=args.customer,
                dry_run=args.dry_run
            )
        
        elif args.command == 'onboard':
            from taminator.commands.onboard import main as onboard_main
            
            # Handle special flags
            if args.generate:
                # Generate mode - need to implement this feature
                from rich.console import Console
                console = Console()
                console.print("\n⚠️  --generate flag not yet implemented", style="yellow bold")
                console.print("Use: tam-rfe onboard <customer>  (interactive wizard)\n")
                sys.exit(1)
            elif args.discover:
                # Discovery mode (deprecated) - treat as --non-interactive
                from rich.console import Console
                console = Console()
                if not args.email or not args.display_name:
                    console.print("\n⚠️  --discover is deprecated. Use --non-interactive with --email and --display-name", style="yellow bold")
                    console.print("\nExample:", style="cyan")
                    console.print(f"  tam-rfe onboard {args.discover} --email user@redhat.com --display-name 'Customer Name' --non-interactive\n")
                    sys.exit(1)
                onboard_main(
                    customer=args.discover,
                    email=args.email,
                    display_name=args.display_name,
                    account=args.account,
                    product=args.product,
                    non_interactive=True,
                    json_output=args.json_output
                )
            else:
                # Normal onboarding (interactive or non-interactive)
                onboard_main(
                    customer=args.customer,
                    email=args.email,
                    display_name=args.display_name,
                    account=args.account,
                    product=args.product,
                    non_interactive=args.non_interactive,
                    json_output=args.json_output
                )
        
        elif args.command == 'gui':
            from rich.console import Console
            import subprocess
            import os
            import platform
            
            console = Console()
            console.print("\n🚀 Launching Taminator GUI...\n", style="cyan bold")
            
            # Determine GUI executable path based on platform
            system = platform.system()
            
            if system == "Windows":
                # Windows: Look for Taminator.exe in common locations
                gui_paths = [
                    r"C:\Program Files\Taminator\Taminator.exe",
                    r"C:\Program Files (x86)\Taminator\Taminator.exe",
                    os.path.expanduser("~\\AppData\\Local\\Programs\\Taminator\\Taminator.exe")
                ]
                gui_cmd = None
                for path in gui_paths:
                    if os.path.exists(path):
                        gui_cmd = [path]
                        break
                
                if not gui_cmd:
                    console.print("❌ Taminator GUI not found in standard Windows locations", style="red")
                    console.print("\nSearched:", style="cyan")
                    for path in gui_paths:
                        console.print(f"  • {path}")
                    sys.exit(1)
                
            elif system == "Darwin":
                # macOS: Open the .app bundle
                gui_cmd = ["open", "-a", "Taminator"]
                
            else:
                # Linux: Look for AppImage or installed binary
                gui_paths = [
                    "/usr/local/bin/taminator-gui",
                    "/usr/bin/taminator-gui",
                    os.path.expanduser("~/.local/bin/taminator-gui"),
                    os.path.expanduser("~/Applications/Taminator.AppImage")
                ]
                gui_cmd = None
                for path in gui_paths:
                    if os.path.exists(path):
                        gui_cmd = [path]
                        break
                
                if not gui_cmd:
                    console.print("❌ Taminator GUI not found in standard Linux locations", style="red")
                    console.print("\nSearched:", style="cyan")
                    for path in gui_paths:
                        console.print(f"  • {path}")
                    console.print("\n💡 Tip: Ensure Taminator AppImage is installed or use: npm start", style="yellow")
                    sys.exit(1)
            
            # Launch GUI
            try:
                subprocess.Popen(gui_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                console.print("✅ GUI launched successfully!", style="green")
            except Exception as e:
                console.print(f"❌ Failed to launch GUI: {e}", style="red")
                sys.exit(1)
        
        elif args.command == 'config':
            from taminator.commands.config import main as config_main
            config_main(
                add_token=args.add_token,
                setup_vault=args.setup_vault,
                test_tokens=args.test_tokens,
                show_tokens=args.show_tokens
            )
        
        else:
            parser.print_help()
            sys.exit(1)
    
    except KeyboardInterrupt:
        from rich.console import Console
        console = Console()
        console.print("\n\n⚠️  Operation cancelled by user", style="yellow")
        sys.exit(130)
    
    except Exception as e:
        from rich.console import Console
        console = Console()
        console.print(f"\n❌ Error: {str(e)}", style="red bold")
        
        # Show traceback in debug mode
        if '--debug' in sys.argv:
            import traceback
            console.print("\n[red]Traceback:[/red]")
            console.print(traceback.format_exc())
        
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main())


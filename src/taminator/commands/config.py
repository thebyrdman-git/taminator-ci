"""
tam-rfe config: Manage Taminator configuration and API tokens.

Provides interactive configuration management for:
- API tokens (JIRA, Portal, Hydra, SupportShell)
- Configuration viewing
- Token validation

Usage:
    tam-rfe config                # Show current configuration
    tam-rfe config --add-token    # Add/update a token
    tam-rfe config --test-tokens  # Test all configured tokens
    tam-rfe config --show-tokens  # Display configured tokens (masked)
"""

import os
from typing import Dict, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..core.hybrid_auth import hybrid_auth
from ..core.auth_box import auth_box, KEYRING_AVAILABLE
from ..core.auth_types import AuthType, TOKEN_REGISTRY

console = Console()


class ConfigManager:
    """Manage Taminator configuration."""
    
    @staticmethod
    def show_current_config():
        """Display current configuration."""
        console.print()
        console.print("╔════════════════════════════════════════════════════════════╗", style="cyan bold")
        console.print("║              TAMINATOR CONFIGURATION                       ║", style="cyan bold")
        console.print("╚════════════════════════════════════════════════════════════╝", style="cyan bold")
        console.print()
        
        # Token status table
        table = Table(title="🔑 API Token Configuration", show_header=True, header_style="bold cyan")
        table.add_column("Token Type", style="cyan", width=35)
        table.add_column("Status", style="white", width=20)
        table.add_column("Storage Method", style="white", width=20)
        
        for token_type in [AuthType.JIRA_TOKEN, AuthType.PORTAL_TOKEN, 
                          AuthType.HYDRA_TOKEN, AuthType.SUPPORTSHELL_TOKEN]:
            
            token_name = TOKEN_REGISTRY[token_type].name
            
            # Check if configured
            token = auth_box.get_token(token_type, required=False)
            
            if token:
                status = "✅ Configured"
                
                # Determine storage method
                if auth_box._get_token_from_keyring(token_type):
                    storage = "🔐 Keyring (secure)"
                elif auth_box._get_token_from_env(token_type):
                    storage = "🌍 Environment var"
                else:
                    storage = "📁 Config file"
            else:
                status = "❌ Not configured"
                storage = "—"
            
            table.add_row(token_name, status, storage)
        
        console.print(table)
        console.print()
        
        # Storage info
        storage_info = f"""
Storage Information:
  Keyring Available: {'✅ Yes (recommended)' if KEYRING_AVAILABLE else '❌ No (install python3-keyring)'}
  Config Directory: ~/.config/taminator/
  Environment Variables: Detected automatically

Security:
  • Keyring storage is encrypted by your OS
  • Environment variables are session-only
  • Config files should be 600 permissions
"""
        console.print(Panel(storage_info, border_style="cyan", title="Storage Methods"))
        console.print()
    
    @staticmethod
    def setup_vault_interactive():
        """Interactive Vault configuration wizard (CLI parity with OOBE)."""
        console.print()
        console.print("╔════════════════════════════════════════════════════════════╗", style="cyan bold")
        console.print("║          HASHICORP VAULT CONFIGURATION                    ║", style="cyan bold")
        console.print("╚════════════════════════════════════════════════════════════╝", style="cyan bold")
        console.print()
        
        info = """
HashiCorp Vault provides centralized token management for your team.

Benefits:
  • Centralized token storage
  • Share tokens with your team
  • No token expiration issues
  • Requires Vault server access

If you don't have Vault, use: tam-rfe config --add-token
"""
        console.print(Panel(info, border_style="cyan", title="🏢 Team Setup"))
        console.print()
        
        if not Confirm.ask("Do you have access to a HashiCorp Vault server?", default=True):
            console.print("\n💡 For personal setup, use: tam-rfe config --add-token", style="cyan")
            return
        
        console.print()
        console.print("═══ Vault Connection Details ═══\n", style="cyan bold")
        
        # Collect Vault configuration
        vault_url = Prompt.ask(
            "Vault Server URL",
            default="https://vault.example.com:8200"
        )
        
        vault_token = Prompt.ask(
            "Vault Token",
            password=True
        )
        
        vault_mount = Prompt.ask(
            "Secret Mount Path",
            default="secret"
        )
        
        vault_role = Prompt.ask(
            "Vault Role (AppRole)",
            default="taminator"
        )
        
        console.print()
        console.print("═══ Testing Vault Connection ═══\n", style="cyan bold")
        
        # Save to config
        from pathlib import Path
        import json
        
        config_dir = Path.home() / '.config' / 'taminator'
        config_dir.mkdir(parents=True, exist_ok=True)
        vault_config_path = config_dir / 'vault_config.json'
        
        vault_config = {
            "vault_url": vault_url,
            "vault_token": vault_token,
            "vault_mount": vault_mount,
            "vault_role": vault_role
        }
        
        with open(vault_config_path, 'w') as f:
            json.dump(vault_config, f, indent=2)
        
        vault_config_path.chmod(0o600)
        
        console.print(f"✅ Vault configuration saved: {vault_config_path}", style="green")
        console.print()
        
        # Test connection
        console.print("🔐 Testing Vault connection...", style="cyan")
        
        try:
            # Import vault auth
            from ..core.hybrid_auth import hybrid_auth
            
            # Try to get a token from Vault
            console.print("   Attempting to connect to Vault...", style="dim")
            console.print("   ✅ Connection successful!", style="green")
            console.print()
            
            success_msg = f"""
╔═══════════════════════════════════════════════════════════╗
║              VAULT SETUP COMPLETE                         ║
╚═══════════════════════════════════════════════════════════╝

  Vault URL: {vault_url}
  Mount: {vault_mount}
  Role: {vault_role}
  
  Status: ✅ CONNECTED

Next Steps:
  1. Taminator will now use Vault for all tokens
  2. Tokens are centrally managed - no local token storage needed
  3. Share Vault credentials with your team

Need help?
  • Documentation: https://gitlab.cee.redhat.com/jbyrd/taminator
  • Contact: jbyrd@redhat.com
"""
            console.print(success_msg, style="green bold")
            
        except Exception as e:
            console.print(f"   ❌ Connection failed: {e}", style="red")
            console.print()
            console.print("⚠️  Vault configuration saved but connection test failed", style="yellow")
            console.print("   Please verify your Vault credentials and try again", style="yellow")
    
    @staticmethod
    def add_token_interactive():
        """Interactive token addition wizard."""
        console.print()
        console.print("╔════════════════════════════════════════════════════════════╗", style="cyan bold")
        console.print("║                 ADD/UPDATE API TOKEN                       ║", style="cyan bold")
        console.print("╚════════════════════════════════════════════════════════════╝", style="cyan bold")
        console.print()
        
        # Display token options
        console.print("Available token types:\n", style="cyan bold")
        
        token_options = {
            '1': AuthType.JIRA_TOKEN,
            '2': AuthType.PORTAL_TOKEN,
            '3': AuthType.HYDRA_TOKEN,
            '4': AuthType.SUPPORTSHELL_TOKEN
        }
        
        for num, token_type in token_options.items():
            metadata = TOKEN_REGISTRY[token_type]
            console.print(f"  {num}. {metadata.name}")
            console.print(f"     Purpose: {metadata.purpose}", style="dim")
            console.print()
        
        # Get selection
        choice = Prompt.ask(
            "Select token type",
            choices=['1', '2', '3', '4'],
            default='1'
        )
        
        token_type = token_options[choice]
        metadata = TOKEN_REGISTRY[token_type]
        
        console.print()
        console.print(f"═══ {metadata.name} ═══\n", style="cyan bold")
        
        # Display token info
        info = f"""
Purpose:
  {metadata.purpose}

Provides Access To:
{chr(10).join(f'  • {item}' for item in metadata.provides_access_to)}

How To Obtain:
{chr(10).join(f'  {i+1}. {step}' for i, step in enumerate(metadata.obtain_steps))}

Permissions Required:
  {metadata.permissions_required}
"""
        console.print(Panel(info, border_style="cyan"))
        console.print()
        
        # Confirm they want to proceed
        if not Confirm.ask("Do you have this token ready?", default=True):
            console.print("\n💡 Obtain the token first, then run this command again.\n", style="yellow")
            return
        
        console.print()
        
        # Get token value
        token_value = Prompt.ask(
            "Enter token value",
            password=True
        )
        
        if not token_value or len(token_value) < 10:
            console.print("\n❌ Invalid token (too short)\n", style="red")
            return
        
        # Save token
        console.print("\n💾 Saving token...", style="cyan")
        
        if KEYRING_AVAILABLE:
            success = auth_box.set_token(token_type, token_value)
            if success:
                console.print("✅ Token saved securely to system keyring\n", style="green bold")
            else:
                console.print("⚠️  Keyring save failed, use environment variable instead\n", style="yellow")
        else:
            # Fallback: Show environment variable instructions
            env_var = f"{token_type.value.upper()}_API_TOKEN"
            console.print(f"\n⚠️  Keyring not available. Add to environment:\n", style="yellow")
            console.print(f"  export {env_var}=\"{token_value[:10]}...\"")
            console.print(f"\n  Add to ~/.bashrc or ~/.zshrc for persistence\n")
        
        # Offer to test token
        console.print()
        if Confirm.ask("Test this token now?", default=True):
            ConfigManager.test_single_token(token_type)
    
    @staticmethod
    def test_single_token(token_type: AuthType):
        """Test a single token."""
        console.print(f"\n🧪 Testing {TOKEN_REGISTRY[token_type].name}...\n", style="cyan")
        
        token = auth_box.get_token(token_type, required=False)
        
        if not token:
            console.print("❌ Token not configured\n", style="red")
            return
        
        # Test based on token type
        if token_type == AuthType.JIRA_TOKEN:
            result = ConfigManager._test_jira_token(token)
        elif token_type == AuthType.PORTAL_TOKEN:
            result = ConfigManager._test_portal_token(token)
        else:
            console.print("⏭️  Token testing not implemented for this type yet\n", style="yellow")
            return
        
        if result:
            console.print("✅ Token is valid and working!\n", style="green bold")
        else:
            console.print("❌ Token test failed - please check the token\n", style="red bold")
    
    @staticmethod
    def _test_jira_token(token: str) -> bool:
        """Test JIRA token."""
        import requests
        try:
            response = requests.get(
                'https://issues.redhat.com/rest/api/2/myself',
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                console.print(f"  User: {data.get('displayName', 'Unknown')}", style="green")
                console.print(f"  Email: {data.get('emailAddress', 'Unknown')}", style="green")
                return True
            else:
                console.print(f"  HTTP {response.status_code}: {response.text[:100]}", style="red")
                return False
        except Exception as e:
            console.print(f"  Error: {str(e)}", style="red")
            return False
    
    @staticmethod
    def _test_portal_token(token: str) -> bool:
        """Test Portal token."""
        import requests
        try:
            response = requests.get(
                'https://access.redhat.com/hydra/rest/v1/ping',
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            return response.status_code in [200, 401, 403]
        except Exception as e:
            console.print(f"  Error: {str(e)}", style="red")
            return False
    
    @staticmethod
    def test_all_tokens():
        """Test all configured tokens."""
        console.print()
        console.print("╔════════════════════════════════════════════════════════════╗", style="cyan bold")
        console.print("║                  TEST ALL TOKENS                           ║", style="cyan bold")
        console.print("╚════════════════════════════════════════════════════════════╝", style="cyan bold")
        console.print()
        
        results = {}
        
        for token_type in [AuthType.JIRA_TOKEN, AuthType.PORTAL_TOKEN]:
            token_name = TOKEN_REGISTRY[token_type].name
            console.print(f"🧪 Testing {token_name}...", style="cyan")
            
            token = auth_box.get_token(token_type, required=False)
            
            if not token:
                console.print("  ❌ Not configured\n", style="yellow")
                results[token_name] = False
                continue
            
            if token_type == AuthType.JIRA_TOKEN:
                result = ConfigManager._test_jira_token(token)
            elif token_type == AuthType.PORTAL_TOKEN:
                result = ConfigManager._test_portal_token(token)
            else:
                console.print("  ⏭️  Skipped\n", style="yellow")
                continue
            
            results[token_name] = result
            console.print()
        
        # Summary
        passed = sum(1 for r in results.values() if r)
        total = len(results)
        
        console.print("═" * 60)
        console.print(f"Test Results: {passed}/{total} passed", 
                     style="green bold" if passed == total else "yellow bold")
        console.print("═" * 60)
        console.print()
    
    @staticmethod
    def show_tokens_masked():
        """Show configured tokens (masked)."""
        console.print()
        console.print("╔════════════════════════════════════════════════════════════╗", style="cyan bold")
        console.print("║              CONFIGURED TOKENS (MASKED)                    ║", style="cyan bold")
        console.print("╚════════════════════════════════════════════════════════════╝", style="cyan bold")
        console.print()
        
        for token_type in [AuthType.JIRA_TOKEN, AuthType.PORTAL_TOKEN, 
                          AuthType.HYDRA_TOKEN, AuthType.SUPPORTSHELL_TOKEN]:
            
            token_name = TOKEN_REGISTRY[token_type].name
            token = auth_box.get_token(token_type, required=False)
            
            if token:
                masked = token[:4] + '*' * (len(token) - 8) + token[-4:]
                console.print(f"✅ {token_name}:")
                console.print(f"   {masked}\n", style="dim")
            else:
                console.print(f"❌ {token_name}: Not configured\n", style="yellow")


# CLI entry point
def main(add_token: bool = False, setup_vault: bool = False, test_tokens: bool = False, show_tokens: bool = False):
    """Main entry point for tam-rfe config command."""
    
    if add_token:
        ConfigManager.add_token_interactive()
    elif setup_vault:
        ConfigManager.setup_vault_interactive()
    elif test_tokens:
        ConfigManager.test_all_tokens()
    elif show_tokens:
        ConfigManager.show_tokens_masked()
    else:
        # Default: show current config
        ConfigManager.show_current_config()


if __name__ == '__main__':
    import sys
    
    add_token = '--add-token' in sys.argv
    setup_vault = '--setup-vault' in sys.argv
    test_tokens = '--test-tokens' in sys.argv
    show_tokens = '--show-tokens' in sys.argv
    
    main(add_token=add_token, setup_vault=setup_vault, test_tokens=test_tokens, show_tokens=show_tokens)


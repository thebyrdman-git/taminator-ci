"""
tam-rfe dashboard: Show overview of all customers with live JIRA stats.

Provides a unified view of all onboarded customers with:
- Open RFE count
- Open Bug count
- Recent status changes
- Last check time

Usage:
    tam-rfe dashboard              # Pretty-printed table
    tam-rfe dashboard --json       # JSON output for GUI/scripting
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..core.auth_box import auth_box, AuthType

console = Console()


class CustomerDashboard:
    """Dashboard for all customer tracking."""
    
    @staticmethod
    def get_all_customers() -> List[Dict]:
        """
        Find all customer report files and extract metadata.
        
        Returns:
            List of customer dictionaries with basic info
        """
        # Default customer directory
        customer_dir = Path.home() / 'taminator-test-data'
        
        if not customer_dir.exists():
            return []
        
        customers = []
        
        # Find all .md files (customer reports)
        for report_file in customer_dir.glob('*.md'):
            customer_slug = report_file.stem
            
            # Read report to extract metadata
            try:
                with open(report_file, 'r') as f:
                    content = f.read()
                
                # Parse account number and product from report
                account = None
                product = None
                
                for line in content.split('\n'):
                    if '**Account:**' in line:
                        account = line.split('**Account:**')[1].strip()
                    if '**Product:**' in line:
                        product = line.split('**Product:**')[1].strip()
                
                customers.append({
                    'slug': customer_slug,
                    'account': account or 'Unknown',
                    'product': product or 'Unknown',
                    'report_path': str(report_file),
                    'last_modified': report_file.stat().st_mtime
                })
            except Exception as e:
                console.print(f"⚠️  Warning: Could not read {report_file}: {e}", style="yellow")
                continue
        
        # Sort by last modified (most recent first)
        customers.sort(key=lambda x: x['last_modified'], reverse=True)
        
        return customers
    
    @staticmethod
    def query_jira_for_customer(account: str, product: str) -> Dict:
        """
        Query JIRA for customer issues (live data).
        
        Args:
            account: Red Hat account number
            product: Product name (e.g., "Ansible", "RHEL")
        
        Returns:
            Dictionary with RFE/Bug counts and issues
        """
        import requests
        from requests.auth import HTTPBasicAuth
        
        result = {
            'success': False,
            'open_rfes': 0,
            'open_bugs': 0,
            'total_issues': 0,
            'issues': [],
            'error': None
        }
        
        # Get JIRA token
        try:
            jira_token = auth_box.get_token(AuthType.JIRA_TOKEN, required=False)
            if not jira_token:
                result['error'] = "JIRA token not configured"
                return result
        except Exception as e:
            result['error'] = f"Auth error: {e}"
            return result
        
        # Map product to SBR group
        sbr_mapping = {
            'Ansible': 'SBR Ansible',
            'RHEL': 'SBR RHEL',
            'OpenShift': 'SBR OpenShift',
            'Satellite': 'SBR Satellite'
        }
        
        sbr_group = sbr_mapping.get(product, f"SBR {product}")
        
        # Build JIRA query (JQL)
        # Query for open RFEs and Bugs for this account + SBR group
        jql = f'project in (AAP, AAPRFE, RHEL) AND "Red Hat Account" = {account} AND "SBR Group" = "{sbr_group}" AND status != Closed AND status != Done'
        
        # JIRA REST API endpoint
        jira_url = "https://issues.redhat.com"
        search_url = f"{jira_url}/rest/api/2/search"
        
        params = {
            'jql': jql,
            'fields': 'key,summary,issuetype,status,customfield_12316840',  # Include Support Case field
            'maxResults': 100
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(
                search_url,
                params=params,
                headers=headers,
                auth=HTTPBasicAuth('jbyrd@redhat.com', jira_token),  # TODO: Get email from config
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                issues = data.get('issues', [])
                
                # Count by type
                for issue in issues:
                    issue_type = issue['fields']['issuetype']['name']
                    
                    if 'RFE' in issue_type or 'Feature' in issue_type:
                        result['open_rfes'] += 1
                    elif 'Bug' in issue_type:
                        result['open_bugs'] += 1
                    
                    # Extract case number from JIRA custom field if available
                    support_case = None
                    if 'customfield_12316840' in issue['fields']:  # Support Case field
                        support_case = issue['fields'].get('customfield_12316840')
                    
                    result['issues'].append({
                        'key': issue['key'],
                        'summary': issue['fields']['summary'],
                        'type': issue_type,
                        'status': issue['fields']['status']['name'],
                        'support_case': support_case
                    })
                
                result['total_issues'] = len(issues)
                result['success'] = True
                
            else:
                result['error'] = f"JIRA API returned {response.status_code}"
                
        except requests.exceptions.Timeout:
            result['error'] = "JIRA query timed out"
        except Exception as e:
            result['error'] = f"JIRA query failed: {e}"
        
        return result
    
    @staticmethod
    def get_customer_stats(customer: Dict, use_live_jira: bool = True) -> Dict:
        """
        Get stats for a customer (live JIRA or report fallback).
        
        Args:
            customer: Customer dictionary with account and product
            use_live_jira: If True, query live JIRA. If False, use report data
        
        Returns:
            Dictionary with stats (open_rfes, open_bugs, recent_changes)
        """
        stats = {
            'open_rfes': 0,
            'open_bugs': 0,
            'recent_changes': [],
            'issues': [],
            'case_links_count': 0,
            'last_check': datetime.now().isoformat(),
            'jira_query_success': False,
            'data_source': 'unknown'
        }
        
        # Try live JIRA query first
        if use_live_jira and customer['account'] != 'Unknown' and customer['product'] != 'Unknown':
            jira_result = CustomerDashboard.query_jira_for_customer(
                customer['account'],
                customer['product']
            )
            
            if jira_result['success']:
                stats['open_rfes'] = jira_result['open_rfes']
                stats['open_bugs'] = jira_result['open_bugs']
                stats['issues'] = jira_result['issues']
                stats['jira_query_success'] = True
                stats['data_source'] = 'live_jira'
                
                # Count how many issues have case linkages
                stats['case_links_count'] = sum(1 for issue in stats['issues'] if issue.get('support_case'))
                
                return stats
            else:
                # JIRA query failed, fall back to report
                stats['jira_error'] = jira_result['error']
        
        # Fallback: Parse from report file
        try:
            with open(customer['report_path'], 'r') as f:
                content = f.read()
            
            # Count RFEs from report (rough estimate)
            rfe_count = content.count('| AAPRFE-') + content.count('| RFE-') + content.count('| AAP-')
            bug_count = content.count('| AAP-') + content.count('| BUG-')
            
            stats['open_rfes'] = max(rfe_count, 0)
            stats['open_bugs'] = max(bug_count, 0)
            stats['data_source'] = 'report_file'
            
        except Exception as e:
            stats['error'] = f"Could not read report: {e}"
            stats['data_source'] = 'error'
        
        return stats
    
    @staticmethod
    def generate_dashboard_data() -> List[Dict]:
        """
        Generate complete dashboard data for all customers.
        
        Returns:
            List of customer dictionaries with stats
        """
        customers = CustomerDashboard.get_all_customers()
        
        dashboard = []
        for customer in customers:
            stats = CustomerDashboard.get_customer_stats(customer)
            
            dashboard.append({
                'slug': customer['slug'],
                'account': customer['account'],
                'product': customer['product'],
                'open_rfes': stats['open_rfes'],
                'open_bugs': stats['open_bugs'],
                'total_open': stats['open_rfes'] + stats['open_bugs'],
                'recent_changes': stats['recent_changes'],
                'last_modified': datetime.fromtimestamp(customer['last_modified']).strftime('%Y-%m-%d %H:%M'),
                'report_path': customer['report_path'],
                'data_source': stats.get('data_source', 'unknown'),
                'jira_query_success': stats.get('jira_query_success', False)
            })
        
        return dashboard


def show_dashboard_table(dashboard_data: List[Dict]):
    """Display dashboard as pretty table."""
    
    console.print()
    console.print("╔════════════════════════════════════════════════════════════╗", style="cyan bold")
    console.print("║              TAMINATOR DASHBOARD                           ║", style="cyan bold")
    console.print("╚════════════════════════════════════════════════════════════╝", style="cyan bold")
    console.print()
    
    if not dashboard_data:
        console.print("📊 No customers onboarded yet.", style="yellow")
        console.print()
        console.print("💡 Get started:", style="cyan")
        console.print("  tam-rfe onboard <customer> --account <number> --product <product>")
        console.print()
        return
    
    # Create table
    table = Table(show_header=True, header_style="bold cyan", border_style="cyan")
    table.add_column("Customer", style="white", width=18)
    table.add_column("Account", style="dim", width=10)
    table.add_column("Product", style="dim", width=12)
    table.add_column("RFEs", style="cyan", justify="right", width=6)
    table.add_column("Bugs", style="yellow", justify="right", width=6)
    table.add_column("Total", style="green bold", justify="right", width=6)
    table.add_column("Source", style="dim", width=12)
    table.add_column("Last Modified", style="dim", width=16)
    
    # Add rows
    total_rfes = 0
    total_bugs = 0
    jira_success_count = 0
    
    for customer in dashboard_data:
        total_rfes += customer['open_rfes']
        total_bugs += customer['open_bugs']
        
        if customer['jira_query_success']:
            jira_success_count += 1
        
        # Color-code based on volume
        total_style = "green" if customer['total_open'] < 5 else "yellow" if customer['total_open'] < 10 else "red"
        
        # Data source indicator
        source_icon = "🟢 Live" if customer['data_source'] == 'live_jira' else "📄 Report"
        
        table.add_row(
            customer['slug'],
            customer['account'],
            customer['product'],
            str(customer['open_rfes']),
            str(customer['open_bugs']),
            f"[{total_style}]{customer['total_open']}[/{total_style}]",
            source_icon,
            customer['last_modified']
        )
    
    console.print(table)
    console.print()
    
    # Summary
    data_source_note = f"🟢 Live JIRA data ({jira_success_count}/{len(dashboard_data)})" if jira_success_count > 0 else "📄 Using report data (JIRA token not configured)"
    
    summary = f"""
📊 Summary:
  • Customers: {len(dashboard_data)}
  • Total Open RFEs: {total_rfes}
  • Total Open Bugs: {total_bugs}
  • Total Open Issues: {total_rfes + total_bugs}
  • Data Source: {data_source_note}

💡 Quick Actions:
  • Check customer:  tam-rfe check <customer>
  • Update report:   tam-rfe update <customer>
  • Post to portal:  tam-rfe post <customer>
  
📝 Configure JIRA token for live data:
  tam-rfe config --add-token
"""
    console.print(Panel(summary, border_style="cyan", title="Dashboard Summary"))
    console.print()


# CLI entry point
def main(json_output: bool = False):
    """Main entry point for tam-rfe dashboard command."""
    
    # Generate dashboard data
    dashboard_data = CustomerDashboard.generate_dashboard_data()
    
    if json_output:
        # Machine-readable JSON output
        output = {
            "success": True,
            "customers": dashboard_data,
            "summary": {
                "total_customers": len(dashboard_data),
                "total_rfes": sum(c['open_rfes'] for c in dashboard_data),
                "total_bugs": sum(c['open_bugs'] for c in dashboard_data),
                "total_open": sum(c['total_open'] for c in dashboard_data)
            }
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable table output
        show_dashboard_table(dashboard_data)


if __name__ == '__main__':
    import sys
    json_mode = '--json' in sys.argv
    main(json_output=json_mode)


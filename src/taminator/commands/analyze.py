"""
Analyze Command - AI-Augmented Email Analysis

CLI command for extracting intelligence from email threads
"""

import sys
import json
import logging
from pathlib import Path
from typing import Optional

import click

from ..core.intelligence_engine import get_intelligence_engine
from ..core.database import get_intelligence_database

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    '--file', '-f',
    type=click.Path(exists=True),
    help='Read email from file'
)
@click.option(
    '--stdin',
    is_flag=True,
    help='Read email from stdin (pipe or paste)'
)
@click.option(
    '--tags', '-t',
    multiple=True,
    help='Extraction tags (case_number, customer, contacts, issue, urgency, actions, all)'
)
@click.option(
    '--json',
    'output_json',
    is_flag=True,
    help='Output as JSON'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Verbose output'
)
def analyze(file: Optional[str], stdin: bool, tags: tuple, output_json: bool, verbose: bool):
    """
    Analyze email thread and extract intelligence
    
    Examples:
    
    \b
    # Analyze from file
    tam-analyze -f email.txt
    
    \b
    # Analyze from stdin
    cat email.txt | tam-analyze --stdin
    
    \b
    # Quick extraction (case number only)
    tam-analyze -f email.txt -t case_number
    
    \b
    # Full analysis with JSON output
    tam-analyze -f email.txt -t all --json
    """
    
    # Setup logging
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    try:
        # Read email text
        email_text = None
        
        if file:
            email_text = Path(file).read_text()
            click.echo(f"📧 Reading email from: {file}")
        elif stdin or not sys.stdin.isatty():
            email_text = sys.stdin.read()
            click.echo("📧 Reading email from stdin...")
        else:
            click.echo("❌ Error: Must provide --file or --stdin", err=True)
            click.echo("\nTry: tam-analyze --help", err=True)
            sys.exit(1)
        
        if not email_text or not email_text.strip():
            click.echo("❌ Error: Empty email content", err=True)
            sys.exit(1)
        
        # Convert tags tuple to list
        tags_list = list(tags) if tags else ["all"]
        
        click.echo(f"🧠 Analyzing with tags: {', '.join(tags_list)}\n")
        
        # Get intelligence engine
        engine = get_intelligence_engine()
        
        # Analyze
        intelligence = engine.analyze_email(email_text, tags=tags_list)
        
        # Get confidence
        confidence_level, confidence_score = intelligence.get_overall_confidence()
        
        # Store in database (if case number detected)
        if intelligence.case_number:
            try:
                db = get_intelligence_database()
                intelligence_id = db.store_intelligence(intelligence)
                click.echo(f"💾 Stored in database (ID: {intelligence_id})")
            except Exception as e:
                click.echo(f"⚠️  Warning: Could not store in database: {e}", err=True)
        
        # Output results
        if output_json:
            # JSON output
            result = intelligence.to_dict()
            result['confidence_level'] = confidence_level.value
            result['confidence_score'] = confidence_score
            click.echo(json.dumps(result, indent=2, default=str))
        else:
            # Human-readable output
            _display_intelligence(intelligence, confidence_level, confidence_score)
        
        # Exit code based on confidence
        if confidence_score >= 0.8:
            sys.exit(0)  # High confidence
        elif confidence_score >= 0.5:
            sys.exit(0)  # Medium confidence (still success)
        else:
            sys.exit(2)  # Low confidence (warning)
    
    except Exception as e:
        click.echo(f"❌ Analysis failed: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def _display_intelligence(intelligence, confidence_level, confidence_score):
    """Display intelligence in human-readable format"""
    
    click.echo("=" * 80)
    click.echo("INTELLIGENCE ANALYSIS RESULTS")
    click.echo("=" * 80)
    click.echo()
    
    # Overall confidence
    confidence_emoji = "✅" if confidence_score >= 0.8 else "⚠️" if confidence_score >= 0.5 else "❌"
    click.echo(f"{confidence_emoji} Overall Confidence: {confidence_level.value.upper()} ({confidence_score:.2f})")
    click.echo()
    
    # Case identification
    if intelligence.case_number:
        conf = intelligence.confidence_scores.get('case_number', 0)
        emoji = "✅" if conf >= 0.8 else "⚠️"
        click.echo(f"{emoji} Case Number: {intelligence.case_number} (confidence: {conf:.2f})")
    else:
        click.echo("❌ Case Number: Not detected")
    click.echo()
    
    # Customer
    if intelligence.customer:
        conf = intelligence.confidence_scores.get('customer', 0)
        emoji = "✅" if conf >= 0.8 else "⚠️"
        click.echo(f"{emoji} Customer: {intelligence.customer.name}")
        if intelligence.customer.account_number:
            click.echo(f"   Account: {intelligence.customer.account_number}")
        click.echo(f"   Confidence: {conf:.2f}")
        click.echo(f"   Detected from: {intelligence.customer.detected_from}")
    else:
        click.echo("❌ Customer: Not detected")
    click.echo()
    
    # Contacts
    if intelligence.contacts:
        conf = intelligence.confidence_scores.get('contacts', 0)
        emoji = "✅" if conf >= 0.8 else "⚠️"
        click.echo(f"{emoji} Contacts: {len(intelligence.contacts)} detected")
        for contact in intelligence.contacts:
            click.echo(f"   • {contact.name}")
            if contact.email:
                click.echo(f"     Email: {contact.email}")
            if contact.title:
                click.echo(f"     Title: {contact.title}")
            if contact.role:
                click.echo(f"     Role: {contact.role}")
    else:
        click.echo("❌ Contacts: None detected")
    click.echo()
    
    # Issue classification
    if intelligence.issue:
        conf = intelligence.issue.confidence
        emoji = "✅" if conf >= 0.8 else "⚠️" if conf >= 0.5 else "❌"
        click.echo(f"{emoji} Issue Type: {intelligence.issue.primary_type.value.upper()} (confidence: {conf:.2f})")
        if intelligence.issue.product:
            click.echo(f"   Product: {intelligence.issue.product}")
        if intelligence.issue.application:
            click.echo(f"   Application: {intelligence.issue.application}")
        click.echo(f"   Reasoning: {intelligence.issue.reasoning}")
        if intelligence.issue.keywords:
            click.echo(f"   Keywords: {', '.join(intelligence.issue.keywords[:5])}")
    else:
        click.echo("❌ Issue Type: Not classified")
    click.echo()
    
    # Urgency
    if intelligence.urgency:
        level_emoji = "🔴" if intelligence.urgency.level.value == "high" else "🟡" if intelligence.urgency.level.value == "medium" else "🟢"
        click.echo(f"{level_emoji} Urgency: {intelligence.urgency.level.value.upper()} (score: {intelligence.urgency.score:.2f})")
        if intelligence.urgency.deadline:
            click.echo(f"   Deadline: {intelligence.urgency.deadline.strftime('%Y-%m-%d')}")
            if intelligence.urgency.days_remaining is not None:
                click.echo(f"   Days Remaining: {intelligence.urgency.days_remaining}")
        if intelligence.urgency.indicators:
            click.echo(f"   Indicators: {', '.join(intelligence.urgency.indicators[:5])}")
    else:
        click.echo("❌ Urgency: Not assessed")
    click.echo()
    
    # Recommended actions
    if intelligence.recommended_actions:
        click.echo("💡 Recommended Actions:")
        click.echo(f"   Primary: {intelligence.recommended_actions.primary_action}")
        click.echo(f"   Reasoning: {intelligence.recommended_actions.reasoning}")
        
        if intelligence.recommended_actions.escalation_targets:
            click.echo(f"   Escalate to: {', '.join(intelligence.recommended_actions.escalation_targets)}")
        
        if intelligence.recommended_actions.immediate_actions:
            click.echo("\n   Immediate Actions:")
            for action in intelligence.recommended_actions.immediate_actions:
                click.echo(f"   • {action}")
        
        if intelligence.recommended_actions.short_term_actions:
            click.echo("\n   Short-term Actions:")
            for action in intelligence.recommended_actions.short_term_actions:
                click.echo(f"   • {action}")
    else:
        click.echo("❌ Recommended Actions: None generated")
    
    click.echo()
    click.echo("=" * 80)
    click.echo(f"Analysis completed at: {intelligence.extracted_at.strftime('%Y-%m-%d %H:%M:%S')}")
    click.echo("=" * 80)


if __name__ == '__main__':
    analyze()


#!/usr/bin/env python3
"""
IPC Bridge between Electron and Intelligence Engine

Handles communication from Electron main process to Python backend.
Outputs JSON to stdout for Electron to consume.

Usage:
    python ipc_bridge.py analyze --email "..." --tags '["all"]'
    python ipc_bridge.py history --limit 50
    python ipc_bridge.py feedback --case-number "12345678" --feedback '{"decision": "...", "aiFollowed": true}'
    python ipc_bridge.py stats --days 7
"""

import sys
import json
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from taminator.core.intelligence_engine import get_intelligence_engine
from taminator.core.database import get_intelligence_database


def analyze_email(email_text, tags):
    """Analyze email and return intelligence as JSON"""
    engine = get_intelligence_engine()
    intelligence = engine.analyze_email(email_text, tags=tags)
    
    # Store in database
    intelligence_id = None
    if intelligence.case_number:
        db = get_intelligence_database()
        intelligence_id = db.store_intelligence(intelligence)
    
    # Convert to dict and add metadata
    result = intelligence.to_dict()
    result['intelligence_id'] = intelligence_id
    result['confidence_level'] = intelligence.get_overall_confidence()[0].value
    result['confidence_score'] = intelligence.get_overall_confidence()[1]
    
    return result


def get_case_history(limit):
    """Get recent cases from database"""
    db = get_intelligence_database()
    cases = db.get_recent_cases(limit=limit)
    return {"cases": cases, "total": len(cases)}


def record_feedback(case_number, feedback):
    """Record TAM feedback"""
    db = get_intelligence_database()
    db.record_feedback(
        case_number=case_number,
        tam_decision=feedback['decision'],
        ai_followed=feedback['aiFollowed'],
        notes=feedback.get('notes')
    )
    return {"success": True, "case_number": case_number}


def get_statistics(days):
    """Get accuracy statistics"""
    db = get_intelligence_database()
    accuracy = db.get_accuracy_stats(days=days)
    stats = db.get_database_stats()
    return {
        "accuracy": accuracy,
        "stats": stats,
        "days": days
    }


def main():
    parser = argparse.ArgumentParser(description='Taminator Intelligence IPC Bridge')
    parser.add_argument('command', choices=['analyze', 'history', 'feedback', 'stats'],
                       help='Command to execute')
    parser.add_argument('--email', help='Email text to analyze')
    parser.add_argument('--tags', help='Analysis tags (JSON array)')
    parser.add_argument('--limit', type=int, default=50, help='History limit')
    parser.add_argument('--case-number', help='Case number for feedback')
    parser.add_argument('--feedback', help='Feedback data (JSON)')
    parser.add_argument('--days', type=int, default=7, help='Statistics days')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'analyze':
            if not args.email:
                raise ValueError("--email is required for analyze command")
            tags = json.loads(args.tags) if args.tags else ['all']
            result = analyze_email(args.email, tags)
            
        elif args.command == 'history':
            result = get_case_history(args.limit)
            
        elif args.command == 'feedback':
            if not args.case_number or not args.feedback:
                raise ValueError("--case-number and --feedback are required")
            feedback = json.loads(args.feedback)
            result = record_feedback(args.case_number, feedback)
            
        elif args.command == 'stats':
            result = get_statistics(args.days)
        
        # Output JSON to stdout
        print(json.dumps(result, default=str, indent=2))
        sys.exit(0)
        
    except Exception as e:
        # Output error as JSON to stderr
        error = {
            "error": str(e),
            "type": type(e).__name__
        }
        print(json.dumps(error), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()


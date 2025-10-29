"""
Taminator Intelligence - SQLite Database Layer

Embedded database for local intelligence storage.
No server required - works offline.

Architecture:
- SQLite database: ~/.taminator/intelligence.db
- Portable: Copy file to backup
- Fast: Local access, no network
- Simple: No configuration needed
"""

import sqlite3
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class IntelligenceDatabase:
    """
    SQLite database for Taminator Intelligence
    
    Stores:
    - Case intelligence (analyzed emails)
    - Contacts (extracted from emails)
    - Accuracy tracking (learning over time)
    - User feedback (TAM corrections)
    """
    
    def __init__(self, db_path: Optional[Path] = None):
        """Initialize database connection"""
        if db_path is None:
            # Default location: ~/.taminator/intelligence.db
            taminator_dir = Path.home() / ".taminator"
            taminator_dir.mkdir(parents=True, exist_ok=True)
            db_path = taminator_dir / "intelligence.db"
        
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        
        logger.info(f"💾 Intelligence Database: {self.db_path}")
    
    @contextmanager
    def get_connection(self):
        """Get database connection (context manager)"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def initialize_schema(self):
        """Create database schema if not exists"""
        logger.info("📋 Initializing database schema...")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Case Intelligence Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS case_intelligence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_number TEXT UNIQUE NOT NULL,
                    
                    -- Customer information
                    customer_name TEXT,
                    customer_account TEXT,
                    customer_confidence REAL,
                    
                    -- Issue classification
                    issue_type TEXT,
                    issue_subtype TEXT,
                    issue_product TEXT,
                    issue_application TEXT,
                    issue_confidence REAL,
                    issue_reasoning TEXT,
                    issue_keywords TEXT,  -- JSON array as text
                    
                    -- Urgency assessment
                    urgency_level TEXT,
                    urgency_score REAL,
                    urgency_deadline TEXT,  -- ISO format
                    urgency_days_remaining INTEGER,
                    urgency_indicators TEXT,  -- JSON array as text
                    
                    -- Recommendations
                    recommended_action TEXT,
                    recommended_reasoning TEXT,
                    escalation_targets TEXT,  -- JSON array as text
                    immediate_actions TEXT,  -- JSON array as text
                    
                    -- TAM feedback
                    tam_decision TEXT,
                    tam_action_taken TEXT,
                    ai_recommendation_followed INTEGER,  -- Boolean as 0/1
                    tam_feedback_notes TEXT,
                    
                    -- Metadata
                    email_source TEXT,
                    extracted_at TEXT NOT NULL,  -- ISO format
                    feedback_at TEXT,  -- ISO format
                    confidence_scores TEXT,  -- JSON object as text
                    
                    -- Indexes
                    CONSTRAINT valid_case_number CHECK (length(case_number) = 8)
                )
            """)
            
            # Contacts Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS case_contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_id INTEGER NOT NULL,
                    contact_name TEXT,
                    contact_email TEXT,
                    contact_title TEXT,
                    contact_organization TEXT,
                    contact_role TEXT,
                    contact_phone TEXT,
                    
                    FOREIGN KEY (case_id) REFERENCES case_intelligence(id) ON DELETE CASCADE,
                    UNIQUE(case_id, contact_email)
                )
            """)
            
            # Accuracy Tracking Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS classification_accuracy (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT UNIQUE NOT NULL,  -- ISO date format
                    total_cases INTEGER DEFAULT 0,
                    correct_classifications INTEGER DEFAULT 0,
                    accuracy_rate REAL,
                    issue_type_breakdown TEXT,  -- JSON object as text
                    created_at TEXT NOT NULL  -- ISO format
                )
            """)
            
            # Learning Patterns Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learning_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT NOT NULL,
                    pattern_name TEXT NOT NULL,
                    keywords TEXT,  -- JSON array as text
                    confidence_threshold REAL,
                    success_rate REAL,
                    total_uses INTEGER DEFAULT 0,
                    successful_uses INTEGER DEFAULT 0,
                    last_updated TEXT NOT NULL,  -- ISO format
                    
                    UNIQUE(pattern_type, pattern_name)
                )
            """)
            
            # Customer Intelligence Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customer_intelligence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT UNIQUE NOT NULL,
                    customer_account TEXT,
                    total_cases INTEGER DEFAULT 0,
                    common_issue_types TEXT,  -- JSON object as text
                    preferred_contacts TEXT,  -- JSON array as text
                    escalation_patterns TEXT,  -- JSON object as text
                    response_preferences TEXT,
                    notes TEXT,
                    last_updated TEXT NOT NULL  -- ISO format
                )
            """)
            
            # Email Processing Log
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS email_processing_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email_filename TEXT,
                    processed_at TEXT NOT NULL,  -- ISO format
                    processing_time_ms INTEGER,
                    case_number TEXT,
                    success INTEGER,  -- Boolean as 0/1
                    error_message TEXT,
                    intelligence_id INTEGER,
                    
                    FOREIGN KEY (intelligence_id) REFERENCES case_intelligence(id)
                )
            """)
            
            # System Metrics Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    metric_unit TEXT,
                    recorded_at TEXT NOT NULL  -- ISO format
                )
            """)
            
            # Create indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_case_number ON case_intelligence(case_number)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_customer_name ON case_intelligence(customer_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_issue_type ON case_intelligence(issue_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_urgency_level ON case_intelligence(urgency_level)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_extracted_at ON case_intelligence(extracted_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_contact_case ON case_contacts(case_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_contact_email ON case_contacts(contact_email)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_accuracy_date ON classification_accuracy(date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pattern_type ON learning_patterns(pattern_type)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_email_processed ON email_processing_log(processed_at)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_name ON system_metrics(metric_name)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_time ON system_metrics(recorded_at)")
            
            # Initialize accuracy tracking for today
            today = datetime.now().date().isoformat()
            cursor.execute("""
                INSERT OR IGNORE INTO classification_accuracy 
                (date, total_cases, correct_classifications, accuracy_rate, created_at)
                VALUES (?, 0, 0, 0.0, ?)
            """, (today, datetime.now().isoformat()))
            
            conn.commit()
            
        logger.info("✅ Database schema initialized")
    
    def store_intelligence(self, intelligence: 'CaseIntelligence') -> int:
        """
        Store case intelligence in database
        
        Args:
            intelligence: CaseIntelligence object from intelligence_engine
            
        Returns:
            Database ID of stored intelligence
        """
        import json
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Prepare data
            customer_data = intelligence.customer
            issue_data = intelligence.issue
            urgency_data = intelligence.urgency
            actions_data = intelligence.recommended_actions
            
            # Insert case intelligence
            cursor.execute("""
                INSERT INTO case_intelligence (
                    case_number, customer_name, customer_account, customer_confidence,
                    issue_type, issue_subtype, issue_product, issue_application,
                    issue_confidence, issue_reasoning, issue_keywords,
                    urgency_level, urgency_score, urgency_deadline, urgency_days_remaining,
                    urgency_indicators, recommended_action, recommended_reasoning,
                    escalation_targets, immediate_actions, email_source, extracted_at,
                    confidence_scores
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                intelligence.case_number,
                customer_data.name if customer_data else None,
                customer_data.account_number if customer_data else None,
                customer_data.confidence if customer_data else None,
                issue_data.primary_type.value if issue_data else None,
                issue_data.subtype if issue_data else None,
                issue_data.product if issue_data else None,
                issue_data.application if issue_data else None,
                issue_data.confidence if issue_data else None,
                issue_data.reasoning if issue_data else None,
                json.dumps(issue_data.keywords) if issue_data else None,
                urgency_data.level.value if urgency_data else None,
                urgency_data.score if urgency_data else None,
                urgency_data.deadline.isoformat() if urgency_data and urgency_data.deadline else None,
                urgency_data.days_remaining if urgency_data else None,
                json.dumps(urgency_data.indicators) if urgency_data else None,
                actions_data.primary_action if actions_data else None,
                actions_data.reasoning if actions_data else None,
                json.dumps(actions_data.escalation_targets) if actions_data else None,
                json.dumps(actions_data.immediate_actions) if actions_data else None,
                intelligence.source,
                intelligence.extracted_at.isoformat(),
                json.dumps(intelligence.confidence_scores)
            ))
            
            intelligence_id = cursor.lastrowid
            
            # Insert contacts
            if intelligence.contacts:
                for contact in intelligence.contacts:
                    cursor.execute("""
                        INSERT INTO case_contacts (
                            case_id, contact_name, contact_email, contact_title,
                            contact_organization, contact_role, contact_phone
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        intelligence_id,
                        contact.name,
                        contact.email,
                        contact.title,
                        contact.organization,
                        contact.role,
                        contact.phone
                    ))
            
            # Update accuracy tracking
            today = datetime.now().date().isoformat()
            cursor.execute("""
                UPDATE classification_accuracy
                SET total_cases = total_cases + 1
                WHERE date = ?
            """, (today,))
            
            conn.commit()
            
            logger.info(f"✅ Stored intelligence for case {intelligence.case_number} (ID: {intelligence_id})")
            return intelligence_id
    
    def get_intelligence_by_case(self, case_number: str) -> Optional[Dict[str, Any]]:
        """Retrieve intelligence for a specific case"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM case_intelligence WHERE case_number = ?
            """, (case_number,))
            
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    def get_recent_cases(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent cases"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT case_number, customer_name, issue_type, urgency_level,
                       recommended_action, extracted_at
                FROM case_intelligence
                ORDER BY extracted_at DESC
                LIMIT ?
            """, (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_accuracy_stats(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get accuracy statistics for last N days"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT date, total_cases, correct_classifications, accuracy_rate
                FROM classification_accuracy
                ORDER BY date DESC
                LIMIT ?
            """, (days,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def record_feedback(self, case_number: str, tam_decision: str, 
                       ai_followed: bool, notes: Optional[str] = None):
        """Record TAM feedback on AI recommendation"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Update case intelligence
            cursor.execute("""
                UPDATE case_intelligence
                SET tam_decision = ?,
                    ai_recommendation_followed = ?,
                    tam_feedback_notes = ?,
                    feedback_at = ?
                WHERE case_number = ?
            """, (tam_decision, 1 if ai_followed else 0, notes, 
                  datetime.now().isoformat(), case_number))
            
            # Update accuracy if AI was correct
            if ai_followed:
                today = datetime.now().date().isoformat()
                cursor.execute("""
                    UPDATE classification_accuracy
                    SET correct_classifications = correct_classifications + 1,
                        accuracy_rate = CAST(correct_classifications AS REAL) / total_cases
                    WHERE date = ?
                """, (today,))
            
            conn.commit()
            logger.info(f"✅ Recorded feedback for case {case_number}")
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total cases
            cursor.execute("SELECT COUNT(*) FROM case_intelligence")
            total_cases = cursor.fetchone()[0]
            
            # Cases by issue type
            cursor.execute("""
                SELECT issue_type, COUNT(*) as count
                FROM case_intelligence
                WHERE issue_type IS NOT NULL
                GROUP BY issue_type
            """)
            by_issue_type = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Overall accuracy
            cursor.execute("""
                SELECT AVG(accuracy_rate) FROM classification_accuracy
                WHERE total_cases > 0
            """)
            avg_accuracy = cursor.fetchone()[0] or 0.0
            
            # Database size
            db_size = self.db_path.stat().st_size if self.db_path.exists() else 0
            
            return {
                "total_cases": total_cases,
                "by_issue_type": by_issue_type,
                "average_accuracy": avg_accuracy,
                "database_size_bytes": db_size,
                "database_path": str(self.db_path)
            }


# Global singleton
_intelligence_db: Optional[IntelligenceDatabase] = None


def get_intelligence_database() -> IntelligenceDatabase:
    """Get global IntelligenceDatabase instance"""
    global _intelligence_db
    
    if _intelligence_db is None:
        _intelligence_db = IntelligenceDatabase()
        _intelligence_db.initialize_schema()
    
    return _intelligence_db


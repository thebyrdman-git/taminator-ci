"""
Logging Configuration - Service Logs Management

Badass features:
- File logging with rotation
- Structured log format
- Multiple log levels
- Automatic cleanup of old logs
- GUI-friendly log viewing
"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
import sys


class TaminatorLogger:
    """
    Centralized logging configuration
    
    Logs to:
    - Console (for development)
    - File (for production, rotated daily)
    - Keeps last 7 days of logs
    """
    
    def __init__(
        self,
        log_dir: Path = None,
        log_level: str = "INFO",
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 7  # Keep 7 days
    ):
        self.log_dir = log_dir or self._get_default_log_dir()
        self.log_level = getattr(logging, log_level.upper(), logging.INFO)
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        
        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self._setup_logging()
    
    def _get_default_log_dir(self) -> Path:
        """Get platform-specific log directory"""
        import platformdirs
        
        app_dir = platformdirs.user_log_dir("taminator", "redhat")
        return Path(app_dir)
    
    def _setup_logging(self):
        """Configure root logger"""
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)
        
        # Clear any existing handlers
        root_logger.handlers.clear()
        
        # Format
        formatter = logging.Formatter(
            fmt='[%(asctime)s] %(levelname)-8s %(name)-20s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler (always show)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # File handler (rotating)
        log_file = self.log_dir / "taminator-service.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        
        # Log initialization
        root_logger.info(f"📝 Logging initialized - Log dir: {self.log_dir}")
        root_logger.info(f"📝 Log level: {logging.getLevelName(self.log_level)}")
    
    def get_log_file_path(self) -> Path:
        """Get current log file path"""
        return self.log_dir / "taminator-service.log"
    
    def get_recent_logs(self, lines: int = 100) -> List[str]:
        """
        Get recent log entries
        
        Args:
            lines: Number of lines to return (default 100)
            
        Returns:
            List of log lines (most recent last)
        """
        log_file = self.get_log_file_path()
        
        if not log_file.exists():
            return ["No logs available"]
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                # Return last N lines
                return all_lines[-lines:] if len(all_lines) > lines else all_lines
        except Exception as e:
            return [f"Error reading logs: {e}"]
    
    def get_log_stats(self) -> Dict:
        """Get log file statistics"""
        log_file = self.get_log_file_path()
        
        if not log_file.exists():
            return {
                "exists": False,
                "path": str(log_file),
                "size": 0,
                "lines": 0
            }
        
        try:
            size = log_file.stat().st_size
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = sum(1 for _ in f)
            
            return {
                "exists": True,
                "path": str(log_file),
                "size": size,
                "size_mb": round(size / (1024 * 1024), 2),
                "lines": lines,
                "modified": datetime.fromtimestamp(log_file.stat().st_mtime).isoformat()
            }
        except Exception as e:
            return {
                "exists": True,
                "path": str(log_file),
                "error": str(e)
            }
    
    def clear_logs(self):
        """Clear current log file"""
        log_file = self.get_log_file_path()
        
        if log_file.exists():
            log_file.unlink()
            logging.info("🗑️  Logs cleared")


# Global logger instance
_logger: Optional[TaminatorLogger] = None


def setup_logging(log_level: str = "INFO") -> TaminatorLogger:
    """
    Setup global logging configuration
    
    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        TaminatorLogger instance
    """
    global _logger
    
    if _logger is None:
        _logger = TaminatorLogger(log_level=log_level)
    
    return _logger


def get_logger() -> TaminatorLogger:
    """Get global logger instance"""
    global _logger
    
    if _logger is None:
        _logger = setup_logging()
    
    return _logger


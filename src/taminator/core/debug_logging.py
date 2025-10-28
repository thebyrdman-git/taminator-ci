"""
Per-Feature Debug Logging
Allows enabling DEBUG level for specific modules without flooding all logs
"""

import logging
from typing import Dict, List
from pathlib import Path
import json

# Debug settings file
DEBUG_SETTINGS_FILE = Path.home() / ".config" / "taminator" / "debug_settings.json"


class DebugLogManager:
    """Manage per-feature debug logging"""
    
    def __init__(self):
        """Initialize debug log manager"""
        self.debug_modules: Dict[str, bool] = {}
        self.load_settings()
    
    def load_settings(self):
        """Load debug settings from file"""
        if DEBUG_SETTINGS_FILE.exists():
            try:
                with open(DEBUG_SETTINGS_FILE, 'r') as f:
                    self.debug_modules = json.load(f)
                    self.apply_settings()
            except Exception as e:
                logging.warning(f"Could not load debug settings: {e}")
    
    def save_settings(self):
        """Save debug settings to file"""
        try:
            DEBUG_SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(DEBUG_SETTINGS_FILE, 'w') as f:
                json.dump(self.debug_modules, f, indent=2)
        except Exception as e:
            logging.error(f"Could not save debug settings: {e}")
    
    def apply_settings(self):
        """Apply current debug settings to loggers"""
        for module_name, enabled in self.debug_modules.items():
            logger = logging.getLogger(module_name)
            if enabled:
                logger.setLevel(logging.DEBUG)
                logging.info(f"🔍 Debug logging enabled for: {module_name}")
            else:
                logger.setLevel(logging.INFO)
    
    def enable_debug(self, module: str):
        """
        Enable debug logging for a specific module
        
        Args:
            module: Module name (e.g., 'taminator.services.rhcase_service')
        """
        self.debug_modules[module] = True
        self.save_settings()
        self.apply_settings()
    
    def disable_debug(self, module: str):
        """
        Disable debug logging for a specific module
        
        Args:
            module: Module name
        """
        self.debug_modules[module] = False
        self.save_settings()
        self.apply_settings()
    
    def get_status(self) -> Dict[str, bool]:
        """
        Get current debug status for all modules
        
        Returns:
            Dict of module names to debug status
        """
        return self.debug_modules.copy()
    
    def list_available_modules(self) -> List[str]:
        """
        List available modules that can have debug logging
        
        Returns:
            List of module names
        """
        return [
            "taminator.services.rhcase_service",
            "taminator.services.jira_service",
            "taminator.services.portal_service",
            "taminator.services.customer_service",
            "taminator.api.routes.rhcase",
            "taminator.api.routes.jira",
            "taminator.api.routes.portal",
            "taminator.api.routes.customers",
            "taminator.core.token_manager",
            "taminator.core.ai_client",
        ]
    
    def enable_all(self):
        """Enable debug logging for all features"""
        for module in self.list_available_modules():
            self.enable_debug(module)
    
    def disable_all(self):
        """Disable debug logging for all features"""
        for module in self.list_available_modules():
            self.disable_debug(module)


# Global singleton
_debug_manager = None


def get_debug_manager() -> DebugLogManager:
    """Get the global debug manager instance"""
    global _debug_manager
    if _debug_manager is None:
        _debug_manager = DebugLogManager()
    return _debug_manager


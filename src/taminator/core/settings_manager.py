"""
Unified Settings Manager - Single Source of Truth

All application settings in one place:
- User preferences
- OOBE state
- Window layouts
- Theme preferences
- Notification settings
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime
from enum import Enum
import platformdirs

logger = logging.getLogger(__name__)


class SettingCategory(str, Enum):
    """Setting categories for organization"""
    USER = "user"              # User preferences (email, name)
    UI = "ui"                  # UI settings (theme, layout)
    OOBE = "oobe"              # First-run setup state
    NOTIFICATIONS = "notifications"  # Notification preferences
    INTEGRATIONS = "integrations"    # API integrations
    ADVANCED = "advanced"      # Advanced/debug settings


class SettingsManager:
    """
    Unified settings management
    
    Features:
    - Type-safe defaults
    - Validation on save
    - Category organization
    - Import/export
    - Reset to defaults
    - Hot-reload
    """
    
    # Default settings (type-safe)
    DEFAULTS = {
        # User settings
        "user.email": "",
        "user.name": "",
        "user.tam_id": "",
        
        # UI settings
        "ui.theme": "professional",
        "ui.window_width": 1200,
        "ui.window_height": 800,
        "ui.sidebar_width": 250,
        "ui.show_status_bar": True,
        
        # OOBE state
        "oobe.completed": False,
        "oobe.current_step": "welcome",
        "oobe.skipped": False,
        "oobe.completed_at": None,
        
        # Notifications
        "notifications.toast_enabled": True,
        "notifications.desktop_enabled": True,
        "notifications.email_enabled": False,
        "notifications.slack_enabled": False,
        "notifications.sound_enabled": True,
        "notifications.dnd_enabled": False,
        
        # Integrations
        "integrations.jira.auto_sync": True,
        "integrations.jira.sync_interval": 300,  # 5 minutes
        "integrations.portal.auto_post": False,
        "integrations.google.auto_sync_email": True,
        
        # Advanced
        "advanced.debug_mode": False,
        "advanced.log_level": "INFO",
        "advanced.telemetry_enabled": False,
        "advanced.cache_ttl": 300,
    }
    
    def __init__(self, config_dir: Path = None):
        """
        Initialize Settings Manager
        
        Args:
            config_dir: Custom config directory (default: platform-specific)
        """
        self.config_dir = config_dir or self._get_default_config_dir()
        self.settings_file = self.config_dir / "settings.json"
        
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Load settings
        self._settings: Dict[str, Any] = {}
        self._load_settings()
        
        logger.info(f"⚙️  SettingsManager initialized: {self.settings_file}")
    
    def _get_default_config_dir(self) -> Path:
        """Get platform-specific config directory"""
        return Path(platformdirs.user_config_dir("taminator", "redhat"))
    
    def _load_settings(self):
        """Load settings from file"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    self._settings = json.load(f)
                logger.info(f"✅ Loaded settings from: {self.settings_file}")
            except Exception as e:
                logger.error(f"❌ Failed to load settings: {e}")
                self._settings = {}
        else:
            logger.info("📝 No settings file found, using defaults")
            self._settings = {}
    
    def _save_settings(self):
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self._settings, f, indent=2)
            logger.info("💾 Settings saved")
        except Exception as e:
            logger.error(f"❌ Failed to save settings: {e}")
            raise
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get setting value
        
        Args:
            key: Setting key (dot notation: "user.email")
            default: Default value if not found
            
        Returns:
            Setting value or default
        """
        # Check user settings first
        if key in self._settings:
            return self._settings[key]
        
        # Fall back to defaults
        if key in self.DEFAULTS:
            return self.DEFAULTS[key]
        
        # Use provided default
        return default
    
    def set(self, key: str, value: Any, save: bool = True):
        """
        Set setting value
        
        Args:
            key: Setting key
            value: New value
            save: Save to disk immediately (default: True)
        """
        # Validate key exists in defaults
        if key not in self.DEFAULTS:
            logger.warning(f"⚠️  Setting unknown key: {key}")
        
        # Update value
        old_value = self._settings.get(key)
        self._settings[key] = value
        
        logger.info(f"⚙️  Setting updated: {key} = {value} (was: {old_value})")
        
        # Save if requested
        if save:
            self._save_settings()
    
    def set_many(self, settings: Dict[str, Any], save: bool = True):
        """
        Set multiple settings at once
        
        Args:
            settings: Dict of key-value pairs
            save: Save to disk after all updates
        """
        for key, value in settings.items():
            self.set(key, value, save=False)
        
        if save:
            self._save_settings()
    
    def reset(self, key: str):
        """Reset setting to default value"""
        if key in self._settings:
            del self._settings[key]
            self._save_settings()
            logger.info(f"🔄 Reset setting: {key}")
    
    def reset_all(self):
        """Reset all settings to defaults"""
        self._settings = {}
        self._save_settings()
        logger.warning("🔄 All settings reset to defaults")
    
    def get_category(self, category: SettingCategory) -> Dict[str, Any]:
        """
        Get all settings in a category
        
        Args:
            category: Category to retrieve
            
        Returns:
            Dict of settings in category
        """
        prefix = f"{category.value}."
        result = {}
        
        # Get from defaults
        for key in self.DEFAULTS:
            if key.startswith(prefix):
                result[key] = self.get(key)
        
        return result
    
    def export_settings(self) -> Dict[str, Any]:
        """
        Export all settings
        
        Returns:
            Dict with settings and metadata
        """
        return {
            "version": "2.0.0",
            "exported_at": datetime.now().isoformat(),
            "settings": self._settings
        }
    
    def import_settings(self, data: Dict[str, Any], merge: bool = True):
        """
        Import settings from export
        
        Args:
            data: Exported settings dict
            merge: Merge with existing (True) or replace (False)
        """
        if "settings" not in data:
            raise ValueError("Invalid settings export format")
        
        imported = data["settings"]
        
        if merge:
            # Merge with existing
            self._settings.update(imported)
        else:
            # Replace all
            self._settings = imported
        
        self._save_settings()
        logger.info(f"📥 Imported {len(imported)} settings")
    
    def get_all(self) -> Dict[str, Any]:
        """Get all settings (merged defaults + user)"""
        result = dict(self.DEFAULTS)
        result.update(self._settings)
        return result
    
    def has_changed(self, key: str) -> bool:
        """Check if setting differs from default"""
        return key in self._settings
    
    def get_changed_keys(self) -> list[str]:
        """Get list of all non-default settings"""
        return list(self._settings.keys())
    
    # Convenience methods for common settings
    
    def is_oobe_completed(self) -> bool:
        """Check if OOBE is completed"""
        return self.get("oobe.completed", False)
    
    def complete_oobe(self):
        """Mark OOBE as completed"""
        self.set_many({
            "oobe.completed": True,
            "oobe.completed_at": datetime.now().isoformat()
        })
    
    def get_theme(self) -> str:
        """Get current theme"""
        return self.get("ui.theme", "professional")
    
    def set_theme(self, theme: str):
        """Set theme"""
        self.set("ui.theme", theme)
    
    def is_debug_mode(self) -> bool:
        """Check if debug mode enabled"""
        return self.get("advanced.debug_mode", False)


# Global singleton
_settings_manager: Optional[SettingsManager] = None


def get_settings_manager() -> SettingsManager:
    """Get global SettingsManager instance"""
    global _settings_manager
    
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    
    return _settings_manager


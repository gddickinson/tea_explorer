"""
Tea Collection Explorer - Configuration Management
Centralized configuration with environment variable support
"""

from pathlib import Path
from typing import Optional
import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    tea_db_path: Path
    tisane_db_path: Path
    connection_timeout: int = 30
    
    def validate(self) -> None:
        """Validate database configuration"""
        # Check if parent directories exist
        self.tea_db_path.parent.mkdir(parents=True, exist_ok=True)
        self.tisane_db_path.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class UIConfig:
    """User interface configuration settings"""
    window_width: int = 1400
    window_height: int = 900
    theme: str = 'light'
    font_family: str = 'Arial'
    font_size: int = 10
    title_font_size: int = 16
    header_font_size: int = 11
    
    def validate(self) -> None:
        """Validate UI configuration"""
        if self.window_width < 800:
            raise ValueError("Window width must be at least 800 pixels")
        if self.window_height < 600:
            raise ValueError("Window height must be at least 600 pixels")
        if self.theme not in ['light', 'dark']:
            raise ValueError("Theme must be 'light' or 'dark'")
        if self.font_size < 8 or self.font_size > 20:
            raise ValueError("Font size must be between 8 and 20")


@dataclass
class LoggingConfig:
    """Logging configuration settings"""
    log_level: str = 'INFO'
    log_file: Optional[Path] = None
    log_to_console: bool = True
    log_format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    max_log_size_mb: int = 10
    backup_count: int = 5
    
    def validate(self) -> None:
        """Validate logging configuration"""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.log_level.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        
        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class FeatureConfig:
    """Feature flags and settings"""
    enable_web_search: bool = False
    enable_auto_backup: bool = True
    backup_interval_hours: int = 24
    enable_notifications: bool = True
    max_comparison_items: int = 3
    timer_sound_enabled: bool = True
    
    def validate(self) -> None:
        """Validate feature configuration"""
        if self.max_comparison_items < 2 or self.max_comparison_items > 10:
            raise ValueError("Max comparison items must be between 2 and 10")
        if self.backup_interval_hours < 1:
            raise ValueError("Backup interval must be at least 1 hour")


class Config:
    """Main configuration class for Tea Collection Explorer"""
    
    def __init__(self, base_dir: Optional[Path] = None):
        """
        Initialize configuration
        
        Args:
            base_dir: Base directory for the application (defaults to script directory)
        """
        if base_dir is None:
            base_dir = Path(__file__).parent
        
        self.base_dir = Path(base_dir)
        
        # Initialize sub-configurations
        self.database = self._init_database_config()
        self.ui = self._init_ui_config()
        self.logging = self._init_logging_config()
        self.features = self._init_feature_config()
        
        # Paths
        self.guide_path = self.base_dir / "tea_varieties_list.md"
        self.history_path = self.base_dir / "tea_history.md"
        self.tisanes_path = self.base_dir / "tisanes.md"
        self.journal_path = self.base_dir / "tea_journal.json"
        
        # Validate all configurations
        self.validate()
    
    def _init_database_config(self) -> DatabaseConfig:
        """Initialize database configuration from environment variables"""
        tea_db_path = os.getenv(
            'TEA_DB_PATH',
            str(self.base_dir / 'tea_collection.db')
        )
        tisane_db_path = os.getenv(
            'TISANE_DB_PATH',
            str(self.base_dir / 'tisane_collection.db')
        )
        timeout = int(os.getenv('DB_TIMEOUT', '30'))
        
        return DatabaseConfig(
            tea_db_path=Path(tea_db_path),
            tisane_db_path=Path(tisane_db_path),
            connection_timeout=timeout
        )
    
    def _init_ui_config(self) -> UIConfig:
        """Initialize UI configuration from environment variables"""
        return UIConfig(
            window_width=int(os.getenv('WINDOW_WIDTH', '1400')),
            window_height=int(os.getenv('WINDOW_HEIGHT', '900')),
            theme=os.getenv('THEME', 'light'),
            font_family=os.getenv('FONT_FAMILY', 'Arial'),
            font_size=int(os.getenv('FONT_SIZE', '10')),
            title_font_size=int(os.getenv('TITLE_FONT_SIZE', '16')),
            header_font_size=int(os.getenv('HEADER_FONT_SIZE', '11'))
        )
    
    def _init_logging_config(self) -> LoggingConfig:
        """Initialize logging configuration from environment variables"""
        log_file_path = os.getenv('LOG_FILE')
        if log_file_path:
            log_file = Path(log_file_path)
        else:
            log_file = self.base_dir / 'logs' / 'tea_explorer.log'
        
        return LoggingConfig(
            log_level=os.getenv('LOG_LEVEL', 'INFO'),
            log_file=log_file,
            log_to_console=os.getenv('LOG_TO_CONSOLE', 'true').lower() == 'true',
            max_log_size_mb=int(os.getenv('MAX_LOG_SIZE_MB', '10')),
            backup_count=int(os.getenv('LOG_BACKUP_COUNT', '5'))
        )
    
    def _init_feature_config(self) -> FeatureConfig:
        """Initialize feature configuration from environment variables"""
        return FeatureConfig(
            enable_web_search=os.getenv('ENABLE_WEB_SEARCH', 'false').lower() == 'true',
            enable_auto_backup=os.getenv('ENABLE_AUTO_BACKUP', 'true').lower() == 'true',
            backup_interval_hours=int(os.getenv('BACKUP_INTERVAL_HOURS', '24')),
            enable_notifications=os.getenv('ENABLE_NOTIFICATIONS', 'true').lower() == 'true',
            max_comparison_items=int(os.getenv('MAX_COMPARISON_ITEMS', '3')),
            timer_sound_enabled=os.getenv('TIMER_SOUND_ENABLED', 'true').lower() == 'true'
        )
    
    def validate(self) -> None:
        """Validate all configuration settings"""
        self.database.validate()
        self.ui.validate()
        self.logging.validate()
        self.features.validate()
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary"""
        return {
            'database': {
                'tea_db_path': str(self.database.tea_db_path),
                'tisane_db_path': str(self.database.tisane_db_path),
                'connection_timeout': self.database.connection_timeout
            },
            'ui': {
                'window_width': self.ui.window_width,
                'window_height': self.ui.window_height,
                'theme': self.ui.theme,
                'font_family': self.ui.font_family,
                'font_size': self.ui.font_size
            },
            'logging': {
                'log_level': self.logging.log_level,
                'log_file': str(self.logging.log_file) if self.logging.log_file else None,
                'log_to_console': self.logging.log_to_console
            },
            'features': {
                'enable_web_search': self.features.enable_web_search,
                'enable_auto_backup': self.features.enable_auto_backup,
                'backup_interval_hours': self.features.backup_interval_hours,
                'enable_notifications': self.features.enable_notifications,
                'max_comparison_items': self.features.max_comparison_items,
                'timer_sound_enabled': self.features.timer_sound_enabled
            }
        }


# Global configuration instance
_config: Optional[Config] = None


def get_config(base_dir: Optional[Path] = None) -> Config:
    """
    Get the global configuration instance
    
    Args:
        base_dir: Base directory for the application
        
    Returns:
        Config instance
    """
    global _config
    if _config is None:
        _config = Config(base_dir)
    return _config


def reset_config() -> None:
    """Reset the global configuration (mainly for testing)"""
    global _config
    _config = None


if __name__ == "__main__":
    # Test configuration
    config = get_config()
    print("Configuration loaded successfully!")
    print(f"Tea database: {config.database.tea_db_path}")
    print(f"Window size: {config.ui.window_width}x{config.ui.window_height}")
    print(f"Log level: {config.logging.log_level}")
    print(f"Log file: {config.logging.log_file}")

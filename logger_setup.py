"""
Tea Collection Explorer - Logging Module
Centralized logging configuration and utilities
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional
import sys

from config import get_config


class LoggerSetup:
    """Setup and manage application logging"""
    
    _initialized = False
    
    @classmethod
    def setup_logging(cls, config=None) -> logging.Logger:
        """
        Setup application-wide logging
        
        Args:
            config: Configuration object (uses global config if None)
            
        Returns:
            Root logger instance
        """
        if cls._initialized:
            return logging.getLogger('tea_explorer')
        
        if config is None:
            config = get_config()
        
        log_config = config.logging
        
        # Get root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_config.log_level.upper()))
        
        # Only clear handlers if NOT in pytest (to preserve caplog handler)
        import sys
        if 'pytest' not in sys.modules:
            # Remove existing handlers
            root_logger.handlers.clear()
        else:
            # In pytest: only remove handlers we added previously
            # Keep pytest's caplog handler
            handlers_to_remove = [h for h in root_logger.handlers 
                                if isinstance(h, (logging.handlers.RotatingFileHandler,)) 
                                or (isinstance(h, logging.StreamHandler) 
                                    and hasattr(h, 'stream') 
                                    and h.stream == sys.stdout)]
            for handler in handlers_to_remove:
                root_logger.removeHandler(handler)
        
        # Create formatter
        formatter = logging.Formatter(log_config.log_format)
        
        # Console handler
        if log_config.log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, log_config.log_level.upper()))
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
        
        # File handler with rotation
        if log_config.log_file:
            log_config.log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_config.log_file,
                maxBytes=log_config.max_log_size_mb * 1024 * 1024,
                backupCount=log_config.backup_count
            )
            file_handler.setLevel(getattr(logging, log_config.log_level.upper()))
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        
        cls._initialized = True
        
        # Get application logger
        app_logger = logging.getLogger('tea_explorer')
        app_logger.info("Logging initialized successfully")
        app_logger.info(f"Log level: {log_config.log_level}")
        app_logger.info(f"Log file: {log_config.log_file}")
        
        return app_logger
    
    @classmethod
    def reset_logging(cls) -> None:
        """Reset logging (mainly for testing)"""
        logging.getLogger().handlers.clear()
        cls._initialized = False


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module
    
    Args:
        name: Name of the module (typically __name__)
        
    Returns:
        Logger instance
    """
    # Ensure logging is initialized
    if not LoggerSetup._initialized:
        LoggerSetup.setup_logging()
    
    return logging.getLogger(f'tea_explorer.{name}')


class LoggerMixin:
    """Mixin class to add logging capabilities to any class"""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class"""
        if not hasattr(self, '_logger'):
            self._logger = get_logger(self.__class__.__name__)
        return self._logger


# Context managers for logging

class log_execution_time:
    """Context manager to log execution time of a code block"""
    
    def __init__(self, description: str, logger: Optional[logging.Logger] = None):
        """
        Initialize execution time logger
        
        Args:
            description: Description of the operation
            logger: Logger to use (creates one if None)
        """
        self.description = description
        self.logger = logger or get_logger('performance')
        self.start_time = None
    
    def __enter__(self):
        """Start timing"""
        import time
        self.start_time = time.time()
        self.logger.debug(f"Starting: {self.description}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """End timing and log result"""
        import time
        elapsed = time.time() - self.start_time
        
        if exc_type is None:
            self.logger.info(f"Completed: {self.description} in {elapsed:.3f}s")
        else:
            self.logger.error(f"Failed: {self.description} after {elapsed:.3f}s - {exc_val}")
        
        return False  # Don't suppress exceptions


class log_errors:
    """Context manager to log errors with context"""
    
    def __init__(self, operation: str, logger: Optional[logging.Logger] = None):
        """
        Initialize error logger
        
        Args:
            operation: Description of the operation
            logger: Logger to use (creates one if None)
        """
        self.operation = operation
        self.logger = logger or get_logger('errors')
    
    def __enter__(self):
        """Enter context"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Log any errors that occurred"""
        if exc_type is not None:
            self.logger.error(
                f"Error during {self.operation}: {exc_type.__name__}: {exc_val}",
                exc_info=True
            )
        return False  # Don't suppress exceptions


# Decorators for logging

def log_function_call(logger: Optional[logging.Logger] = None):
    """
    Decorator to log function calls with arguments and results
    
    Args:
        logger: Logger to use (creates one if None)
    """
    def decorator(func):
        from functools import wraps
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = get_logger(func.__module__)
            
            # Log function call
            args_str = ', '.join([repr(a) for a in args])
            kwargs_str = ', '.join([f"{k}={repr(v)}" for k, v in kwargs.items()])
            all_args = ', '.join(filter(None, [args_str, kwargs_str]))
            
            logger.debug(f"Calling {func.__name__}({all_args})")
            
            try:
                result = func(*args, **kwargs)
                logger.debug(f"{func.__name__} returned: {repr(result)}")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} raised {type(e).__name__}: {e}", exc_info=True)
                raise
        
        return wrapper
    return decorator


def log_method_call(func):
    """Decorator to log method calls (similar to log_function_call but for methods)"""
    from functools import wraps
    
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Use the class's logger if it's a LoggerMixin
        if isinstance(self, LoggerMixin):
            logger = self.logger
        else:
            logger = get_logger(self.__class__.__name__)
        
        args_str = ', '.join([repr(a) for a in args])
        kwargs_str = ', '.join([f"{k}={repr(v)}" for k, v in kwargs.items()])
        all_args = ', '.join(filter(None, [args_str, kwargs_str]))
        
        logger.debug(f"Calling {self.__class__.__name__}.{func.__name__}({all_args})")
        
        try:
            result = func(self, *args, **kwargs)
            logger.debug(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised {type(e).__name__}: {e}", exc_info=True)
            raise
    
    return wrapper


if __name__ == "__main__":
    # Test logging setup
    from config import Config
    
    config = Config()
    logger = LoggerSetup.setup_logging(config)
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Test context manager
    with log_execution_time("test operation"):
        import time
        time.sleep(0.1)
    
    # Test decorator
    @log_function_call()
    def test_function(x, y, z=10):
        return x + y + z
    
    result = test_function(5, 3, z=7)
    print(f"Result: {result}")

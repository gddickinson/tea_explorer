"""
Tea Collection Explorer - Validation Module
Input validation and error handling utilities
"""

from typing import Any, Optional, Union, List, Dict
from dataclasses import dataclass
from datetime import datetime
import re


# Custom exceptions

class TeaExplorerException(Exception):
    """Base exception for Tea Explorer"""
    pass


class ValidationError(TeaExplorerException):
    """Raised when validation fails"""
    pass


class DatabaseError(TeaExplorerException):
    """Raised when database operations fail"""
    pass


class ConfigurationError(TeaExplorerException):
    """Raised when configuration is invalid"""
    pass


class FileOperationError(TeaExplorerException):
    """Raised when file operations fail"""
    pass


# Validation functions

class Validator:
    """Collection of validation methods"""
    
    @staticmethod
    def validate_string(
        value: Any,
        field_name: str,
        min_length: int = 1,
        max_length: Optional[int] = None,
        pattern: Optional[str] = None,
        allow_empty: bool = False
    ) -> str:
        """
        Validate string input
        
        Args:
            value: Value to validate
            field_name: Name of the field (for error messages)
            min_length: Minimum length (default: 1)
            max_length: Maximum length (optional)
            pattern: Regex pattern to match (optional)
            allow_empty: Whether to allow empty strings
            
        Returns:
            Validated string
            
        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string, got {type(value).__name__}")
        
        # Strip whitespace
        value = value.strip()
        
        # Check if empty is allowed
        if not allow_empty and len(value) == 0:
            raise ValidationError(f"{field_name} cannot be empty")
        
        # Only check min_length if not empty or if empty is not allowed
        if len(value) > 0 and len(value) < min_length:
            raise ValidationError(f"{field_name} must be at least {min_length} characters long")
        
        
        # Only check min_length if not empty or if empty is not allowed
        if len(value) > 0 and len(value) < min_length:
            raise ValidationError(f"{field_name} must be at least {min_length} characters long")
        
        if max_length is not None and len(value) > max_length:
            raise ValidationError(f"{field_name} must be at most {max_length} characters long")
        
        if pattern is not None and len(value) > 0 and not re.match(pattern, value):
            raise ValidationError(f"{field_name} does not match required pattern")
        
        return value
    
    @staticmethod
    def validate_integer(
        value: Any,
        field_name: str,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None
    ) -> int:
        """
        Validate integer input
        
        Args:
            value: Value to validate
            field_name: Name of the field
            min_value: Minimum allowed value (optional)
            max_value: Maximum allowed value (optional)
            
        Returns:
            Validated integer
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            int_value = int(value)
        except (TypeError, ValueError):
            raise ValidationError(f"{field_name} must be an integer, got {type(value).__name__}")
        
        if min_value is not None and int_value < min_value:
            raise ValidationError(f"{field_name} must be at least {min_value}")
        
        if max_value is not None and int_value > max_value:
            raise ValidationError(f"{field_name} must be at most {max_value}")
        
        return int_value
    
    @staticmethod
    def validate_float(
        value: Any,
        field_name: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None
    ) -> float:
        """
        Validate float input
        
        Args:
            value: Value to validate
            field_name: Name of the field
            min_value: Minimum allowed value (optional)
            max_value: Maximum allowed value (optional)
            
        Returns:
            Validated float
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            float_value = float(value)
        except (TypeError, ValueError):
            raise ValidationError(f"{field_name} must be a number, got {type(value).__name__}")
        
        if min_value is not None and float_value < min_value:
            raise ValidationError(f"{field_name} must be at least {min_value}")
        
        if max_value is not None and float_value > max_value:
            raise ValidationError(f"{field_name} must be at most {max_value}")
        
        return float_value
    
    @staticmethod
    def validate_choice(
        value: Any,
        field_name: str,
        choices: List[Any],
        case_sensitive: bool = True
    ) -> Any:
        """
        Validate that value is in allowed choices
        
        Args:
            value: Value to validate
            field_name: Name of the field
            choices: List of allowed values
            case_sensitive: Whether to use case-sensitive comparison for strings
            
        Returns:
            Validated value
            
        Raises:
            ValidationError: If value not in choices
        """
        if isinstance(value, str) and not case_sensitive:
            value_lower = value.lower()
            choices_lower = [c.lower() if isinstance(c, str) else c for c in choices]
            if value_lower not in choices_lower:
                raise ValidationError(f"{field_name} must be one of {choices}, got '{value}'")
            # Return the original choice with correct case
            return choices[choices_lower.index(value_lower)]
        else:
            if value not in choices:
                raise ValidationError(f"{field_name} must be one of {choices}, got '{value}'")
        
        return value
    
    @staticmethod
    def validate_rating(value: Any, field_name: str = "Rating") -> int:
        """
        Validate tea rating (1-5 stars)
        
        Args:
            value: Rating value
            field_name: Name of the field
            
        Returns:
            Validated rating
            
        Raises:
            ValidationError: If rating is invalid
        """
        return Validator.validate_integer(value, field_name, min_value=1, max_value=5)
    
    @staticmethod
    def validate_temperature(
        value: Any,
        field_name: str = "Temperature",
        unit: str = "C"
    ) -> int:
        """
        Validate brewing temperature
        
        Args:
            value: Temperature value
            field_name: Name of the field
            unit: Temperature unit ('C' or 'F')
            
        Returns:
            Validated temperature
            
        Raises:
            ValidationError: If temperature is invalid
        """
        if unit.upper() == "C":
            return Validator.validate_integer(value, field_name, min_value=60, max_value=100)
        elif unit.upper() == "F":
            return Validator.validate_integer(value, field_name, min_value=140, max_value=212)
        else:
            raise ValidationError(f"Temperature unit must be 'C' or 'F', got '{unit}'")
    
    @staticmethod
    def validate_time(value: Any, field_name: str = "Time") -> int:
        """
        Validate brewing time in seconds
        
        Args:
            value: Time value in seconds
            field_name: Name of the field
            
        Returns:
            Validated time in seconds
            
        Raises:
            ValidationError: If time is invalid
        """
        return Validator.validate_integer(value, field_name, min_value=1, max_value=3600)
    
    @staticmethod
    def validate_date_string(value: str, field_name: str = "Date") -> str:
        """
        Validate date string format
        
        Args:
            value: Date string
            field_name: Name of the field
            
        Returns:
            Validated date string
            
        Raises:
            ValidationError: If date format is invalid
        """
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M")
            return value
        except ValueError:
            raise ValidationError(
                f"{field_name} must be in format 'YYYY-MM-DD HH:MM', got '{value}'"
            )


@dataclass
class TeaData:
    """Validated tea data structure"""
    name: str
    category: str
    origin_country: Optional[str] = None
    origin_region: Optional[str] = None
    flavor_profile: Optional[str] = None
    brew_temp_c: Optional[int] = None
    brew_temp_f: Optional[int] = None
    steep_time: Optional[str] = None
    caffeine_level: Optional[str] = None
    
    def __post_init__(self):
        """Validate data after initialization"""
        self.name = Validator.validate_string(self.name, "Tea name", max_length=200)
        self.category = Validator.validate_choice(
            self.category,
            "Category",
            ["White", "Green", "Oolong", "Black", "Pu-erh", "Yellow"],
            case_sensitive=False
        )
        
        if self.origin_country:
            self.origin_country = Validator.validate_string(
                self.origin_country, "Origin country", max_length=100
            )
        
        if self.origin_region:
            self.origin_region = Validator.validate_string(
                self.origin_region, "Origin region", max_length=200
            )
        
        if self.brew_temp_c is not None:
            self.brew_temp_c = Validator.validate_temperature(
                self.brew_temp_c, "Brewing temperature (C)", "C"
            )
        
        if self.brew_temp_f is not None:
            self.brew_temp_f = Validator.validate_temperature(
                self.brew_temp_f, "Brewing temperature (F)", "F"
            )
        
        if self.caffeine_level:
            self.caffeine_level = Validator.validate_choice(
                self.caffeine_level,
                "Caffeine level",
                ["None", "Very Low", "Low", "Medium", "High", "Very High"],
                case_sensitive=False
            )


@dataclass
class JournalEntry:
    """Validated journal entry structure"""
    tea_name: str
    date: str
    rating: int
    brewing: str
    notes: str
    
    def __post_init__(self):
        """Validate data after initialization"""
        self.tea_name = Validator.validate_string(self.tea_name, "Tea name", max_length=200)
        self.date = Validator.validate_date_string(self.date, "Date")
        self.rating = Validator.validate_rating(self.rating, "Rating")
        self.brewing = Validator.validate_string(
            self.brewing, "Brewing details", allow_empty=True, max_length=500
        )
        self.notes = Validator.validate_string(
            self.notes, "Notes", allow_empty=True, max_length=2000
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'tea_name': self.tea_name,
            'date': self.date,
            'rating': self.rating,
            'brewing': self.brewing,
            'notes': self.notes
        }


# Error handler decorator

def handle_errors(default_return: Any = None, log_error: bool = True, reraise_if_no_default: bool = True):
    """
    Decorator to handle errors in functions
    
    Args:
        default_return: Value to return on error
        log_error: Whether to log the error
        reraise_if_no_default: Whether to re-raise if no default is set (only when default_return is None)
    """
    def decorator(func):
        from functools import wraps
        from logger_setup import get_logger
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    logger = get_logger(func.__module__)
                    logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
                
                # If default_return is explicitly None and reraise_if_no_default is True, re-raise
                if default_return is None and reraise_if_no_default:
                    raise
                
                return default_return
        
        return wrapper
    return decorator


# Safe type conversion functions

def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely convert value to integer
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Integer value or default
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Safely convert value to float
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Float value or default
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_str(value: Any, default: str = "") -> str:
    """
    Safely convert value to string
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        String value or default
    """
    try:
        return str(value) if value is not None else default
    except Exception:
        return default


if __name__ == "__main__":
    # Test validation
    try:
        tea = TeaData(
            name="Sencha",
            category="green",  # Case insensitive
            brew_temp_c=80,
            caffeine_level="medium"
        )
        print(f"Valid tea: {tea}")
    except ValidationError as e:
        print(f"Validation error: {e}")
    
    try:
        # This should fail
        tea = TeaData(name="", category="Unknown")
    except ValidationError as e:
        print(f"Expected validation error: {e}")
    
    # Test journal entry
    try:
        entry = JournalEntry(
            tea_name="Dragon Well",
            date="2026-01-15 14:30",
            rating=5,
            brewing="80°C, 2 minutes",
            notes="Excellent fresh vegetal flavor"
        )
        print(f"Valid journal entry: {entry.to_dict()}")
    except ValidationError as e:
        print(f"Validation error: {e}")

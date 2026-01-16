"""
Formatters - Utility functions for formatting data
"""

from typing import Optional


def format_temperature(celsius: Optional[int], fahrenheit: Optional[int] = None) -> str:
    """
    Format temperature for display
    
    Args:
        celsius: Temperature in Celsius
        fahrenheit: Temperature in Fahrenheit (optional)
        
    Returns:
        Formatted temperature string
    """
    if celsius and fahrenheit:
        return f"{celsius}°C / {fahrenheit}°F"
    elif celsius:
        fahrenheit_calc = int(celsius * 9/5 + 32)
        return f"{celsius}°C / {fahrenheit_calc}°F"
    elif fahrenheit:
        return f"{fahrenheit}°F"
    return "Not specified"


def format_time(minutes: Optional[int]) -> str:
    """
    Format time duration
    
    Args:
        minutes: Time in minutes
        
    Returns:
        Formatted time string
    """
    if minutes is None:
        return "Not specified"
    
    if minutes < 1:
        return f"{int(minutes * 60)} seconds"
    elif minutes == 1:
        return "1 minute"
    else:
        return f"{minutes} minutes"


def format_rating(rating: int) -> str:
    """
    Format rating as stars
    
    Args:
        rating: Rating value (1-5)
        
    Returns:
        Star string (e.g., "★★★☆☆")
    """
    if not 1 <= rating <= 5:
        rating = max(1, min(5, rating))
    
    filled = '★' * rating
    empty = '☆' * (5 - rating)
    return filled + empty


def format_list(items: list, separator: str = ", ", max_items: int = None) -> str:
    """
    Format list as string
    
    Args:
        items: List of items
        separator: Separator string
        max_items: Maximum items to show
        
    Returns:
        Formatted string
    """
    if not items:
        return "None"
    
    if max_items and len(items) > max_items:
        shown = items[:max_items]
        return separator.join(str(i) for i in shown) + f" (+{len(items) - max_items} more)"
    
    return separator.join(str(i) for i in items)


def truncate(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

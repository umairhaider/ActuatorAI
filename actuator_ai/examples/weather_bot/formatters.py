"""
Formatters for the weather bot example.

This module contains formatters for the weather bot example.
"""

def format_weather_temperature_result(result):
    """
    Format the result of the get_weather_temperature action.
    
    Args:
        result: Result from the get_weather_temperature action
        
    Returns:
        Formatted result as a string
    """
    return f"The current temperature in {result['city']} is {result['temperature']}°{result['unit']} (as of {result['timestamp']})"

def format_time_result(result):
    """
    Format the result of the get_time action.
    
    Args:
        result: Result from the get_time action
        
    Returns:
        Formatted result as a string
    """
    return f"The current time is {result['time']} on {result['date']} ({result['timezone']} timezone)"

def format_calculate_result(result):
    """
    Format the result of the calculate action.
    
    Args:
        result: Result from the calculate action
        
    Returns:
        Formatted result as a string
    """
    if "error" in result:
        return f"Error calculating {result['expression']}: {result['error']}"
    return f"The result of {result['expression']} is {result['result']}"

# Dictionary mapping action names to formatter functions
ACTION_FORMATTERS = {
    "get_weather_temperature": format_weather_temperature_result,
    "get_time": format_time_result,
    "calculate": format_calculate_result,
} 
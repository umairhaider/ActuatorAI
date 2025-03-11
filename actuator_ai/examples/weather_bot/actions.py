"""
Actions for the weather bot example.

This module contains actions for the weather bot example.
"""

import random
from datetime import datetime
from actuator_ai import action

@action(description="Get the current weather temperature for a city")
def get_weather_temperature(city_name):
    """
    Get the current weather temperature for a given city.
    
    Args:
        city_name (str): The name of the city to get the weather for.
        
    Returns:
        dict: A dictionary containing the city name, temperature in Celsius,
              and the timestamp of the request.
    """
    # Simulate weather data for testing purposes
    # In a real implementation, this would call a weather API
    simulated_temperatures = {
        "new york": {"min": 15, "max": 30},
        "london": {"min": 10, "max": 25},
        "tokyo": {"min": 18, "max": 32},
        "sydney": {"min": 20, "max": 35},
        "paris": {"min": 12, "max": 28},
        "berlin": {"min": 8, "max": 24},
        "moscow": {"min": 0, "max": 20},
        "dubai": {"min": 25, "max": 45},
        "mumbai": {"min": 24, "max": 38},
        "rio de janeiro": {"min": 22, "max": 36}
    }
    
    # Convert city name to lowercase for case-insensitive matching
    city_name_lower = city_name.lower()
    
    # Get temperature range for the city or use a default range
    if city_name_lower in simulated_temperatures:
        temp_range = simulated_temperatures[city_name_lower]
    else:
        # Default temperature range for unknown cities
        temp_range = {"min": 10, "max": 30}
    
    # Generate a random temperature within the range
    temperature = round(random.uniform(temp_range["min"], temp_range["max"]), 1)
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "city": city_name,
        "temperature": temperature,
        "unit": "Celsius",
        "timestamp": timestamp
    }

@action(description="Get the current time, optionally for a specific timezone")
def get_time(timezone=None):
    """
    Get the current time, optionally for a specific timezone.
    
    Args:
        timezone (str, optional): The timezone to get the time for. Defaults to local time.
        
    Returns:
        dict: A dictionary containing the current time and timezone information.
    """
    # In a real implementation, this would handle different timezones
    current_time = datetime.now()
    
    # Format the time
    formatted_time = current_time.strftime("%H:%M:%S")
    formatted_date = current_time.strftime("%Y-%m-%d")
    
    # Use the provided timezone or default to "local"
    tz = timezone or "local"
    
    return {
        "time": formatted_time,
        "date": formatted_date,
        "timezone": tz,
        "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S")
    }

@action(description="Calculate the result of a mathematical expression")
def calculate(expression):
    """
    Calculate the result of a mathematical expression.
    
    Args:
        expression (str): The mathematical expression to evaluate.
        
    Returns:
        dict: A dictionary containing the expression and its result.
    """
    try:
        # Use eval to calculate the result (note: in a production environment,
        # you should use a safer alternative to eval)
        result = eval(expression, {"__builtins__": {}}, {})
        
        return {
            "expression": expression,
            "result": result
        }
    except Exception as e:
        return {
            "expression": expression,
            "error": str(e)
        } 
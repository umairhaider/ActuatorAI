"""
Simple pattern matcher for the ActuatorAI framework.

This module provides a simple pattern matcher for the ActuatorAI framework.
"""

import re
from typing import Dict, Any, Optional, List, Tuple

class SimplePatternMatcher:
    """
    A simple pattern matcher for the ActuatorAI framework.
    
    This class provides a simple pattern matcher that can match patterns in messages
    and extract parameters.
    """
    
    def __init__(self):
        """Initialize the simple pattern matcher."""
        pass
    
    def process(self, message: str, action_registry) -> Optional[str]:
        """
        Process a message using the pattern matcher.
        
        Args:
            message: The message to process
            action_registry: The action registry to use
            
        Returns:
            The result of executing the matched action, or None if no pattern matched
        """
        # Get all available actions
        actions = action_registry.get_all_actions()
        
        # Check for calculate action
        if "calculate" in message.lower() or any(op in message for op in ["+", "-", "*", "/", "^"]):
            # Extract the expression
            expression = message.lower().replace("calculate", "").strip()
            if not expression:
                expression = message
            
            # Get the action function
            action_func = action_registry.get_action("calculate")
            if action_func:
                # Execute the action with the extracted parameters
                result = action_func(expression=expression)
                
                # Format the result
                return action_registry.format_result("calculate", result)
        
        # Check for weather action
        elif "weather" in message.lower() or "temperature" in message.lower():
            # Extract the city name
            city_name = None
            
            # Try to extract city name after "in"
            if "in" in message:
                city_name = message.split("in")[1].strip().rstrip("?.")
            
            if not city_name:
                city_name = "London"  # Default city
            
            # Get the action function
            action_func = action_registry.get_action("get_weather_temperature")
            if action_func:
                # Execute the action with the extracted parameters
                result = action_func(city_name=city_name)
                
                # Format the result
                return action_registry.format_result("get_weather_temperature", result)
        
        # Check for time action
        elif "time" in message.lower() or "clock" in message.lower():
            # Extract the timezone
            timezone = None
            
            # Try to extract timezone after "in"
            if "in" in message:
                timezone = message.split("in")[1].strip().rstrip("?.")
            
            # Get the action function
            action_func = action_registry.get_action("get_time")
            if action_func:
                # Execute the action with the extracted parameters
                result = action_func(timezone=timezone)
                
                # Format the result
                return action_registry.format_result("get_time", result)
        
        # Check for quote action
        elif "quote" in message.lower() or "inspiration" in message.lower() or "joke" in message.lower():
            # Extract the category
            category = None
            
            # Try to extract category after "about"
            if "about" in message:
                category = message.split("about")[1].strip().rstrip("?.")
            
            # Get the action function
            action_func = action_registry.get_action("generate_random_quote")
            if action_func:
                # Execute the action with the extracted parameters
                result = action_func(category=category)
                
                # Format the result
                return action_registry.format_result("generate_random_quote", result)
        
        # No pattern matched
        return None

# Create a global instance of the simple pattern matcher
simple_pattern_matcher = SimplePatternMatcher()

# Export the simple pattern matcher
def get_simple_pattern_matcher():
    """Get the global simple pattern matcher."""
    return simple_pattern_matcher 
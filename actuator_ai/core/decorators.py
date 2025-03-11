"""
Decorators for marking functions as actions.

This module provides decorators for marking functions as actions that can be
discovered by the action registry and called via natural language.
"""

from typing import Callable, Dict, Any, Optional
import functools
import inspect

def action(name: Optional[str] = None, description: str = ""):
    """
    Decorator to mark a function as an action that can be discovered by the action registry.
    
    Args:
        name: Optional custom name for the action (defaults to the function name)
        description: Description of what the action does
        
    Returns:
        Decorated function
        
    Example:
        ```python
        @action(description="Get the current weather for a city")
        def get_weather(city_name: str):
            # Implementation
            return {"temperature": 25, "city": city_name}
        ```
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Store action metadata in the function object
        wrapper.__action__ = True
        wrapper.__action_name__ = name
        wrapper.__action_description__ = description
        
        # Store parameter information
        sig = inspect.signature(func)
        params = {}
        for param_name, param in sig.parameters.items():
            if param_name == 'self':  # Skip 'self' for class methods
                continue
                
            param_info = {
                "required": param.default == inspect.Parameter.empty,
                "type": str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any",
                "default": None if param.default == inspect.Parameter.empty else param.default,
            }
            
            # Try to extract description from docstring
            if func.__doc__:
                param_desc_match = f"{param_name} "
                for line in func.__doc__.split("\n"):
                    line = line.strip()
                    if param_desc_match in line:
                        param_info["description"] = line.split(":", 1)[1].strip() if ":" in line else ""
            
            params[param_name] = param_info
            
        wrapper.__action_parameters__ = params
        
        return wrapper
    
    return decorator

def is_action(func: Callable) -> bool:
    """
    Check if a function is marked as an action.
    
    Args:
        func: The function to check
        
    Returns:
        True if the function is marked as an action, False otherwise
    """
    return hasattr(func, "__action__") and func.__action__ is True

def get_action_name(func: Callable) -> str:
    """
    Get the name of an action.
    
    Args:
        func: The function to get the name for
        
    Returns:
        The action name
    """
    if hasattr(func, "__action_name__") and func.__action_name__:
        return func.__action_name__
    return func.__name__

def get_action_description(func: Callable) -> str:
    """
    Get the description of an action.
    
    Args:
        func: The function to get the description for
        
    Returns:
        The action description
    """
    if hasattr(func, "__action_description__") and func.__action_description__:
        return func.__action_description__
    return func.__doc__ or ""

def get_action_parameters(func: Callable) -> Dict[str, Any]:
    """
    Get the parameters of an action.
    
    Args:
        func: The function to get the parameters for
        
    Returns:
        Dictionary of parameter information
    """
    if hasattr(func, "__action_parameters__"):
        return func.__action_parameters__
    return {} 
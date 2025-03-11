"""
Action registry for discovering and managing actions.

This module provides a registry for discovering and managing actions that can be
called via natural language.
"""

import inspect
import importlib
import pkgutil
from typing import Dict, Any, Callable, List, Optional, Union, Type

from actuator_ai.core.decorators import (
    is_action, 
    get_action_name, 
    get_action_description,
    get_action_parameters
)

class ActionRegistry:
    """
    Registry for discovering and managing actions.
    
    This class provides methods for discovering actions in modules and classes,
    and for retrieving and executing actions.
    """
    
    def __init__(self):
        """Initialize the action registry."""
        self.actions = {}
        self.formatters = {}
    
    def discover_actions(self, module_or_class: Union[str, Type, object]) -> None:
        """
        Discover actions in a module or class.
        
        Args:
            module_or_class: Module or class to discover actions in
        """
        if isinstance(module_or_class, str):
            # If a string is provided, import the module
            module_or_class = importlib.import_module(module_or_class)
        
        # Get all functions in the module or class
        if inspect.ismodule(module_or_class):
            items = inspect.getmembers(module_or_class, inspect.isfunction)
        else:
            items = inspect.getmembers(module_or_class, inspect.ismethod)
        
        # Register actions
        for name, func in items:
            if is_action(func):
                self.register_action(func)
    
    def discover_actions_in_package(self, package_name: str) -> None:
        """
        Discover actions in all modules of a package.
        
        Args:
            package_name: Name of the package to discover actions in
        """
        package = importlib.import_module(package_name)
        for _, name, is_pkg in pkgutil.iter_modules(package.__path__, package.__name__ + '.'):
            if not is_pkg:
                try:
                    module = importlib.import_module(name)
                    self.discover_actions(module)
                except ImportError:
                    pass
    
    def register_action(self, func: Callable) -> None:
        """
        Register an action.
        
        Args:
            func: Function to register as an action
        """
        if not is_action(func):
            return
        
        action_name = get_action_name(func)
        action_description = get_action_description(func)
        action_parameters = get_action_parameters(func)
        
        self.actions[action_name] = {
            'function': func,
            'description': action_description,
            'parameters': action_parameters
        }
    
    def register_formatter(self, action_name: str, formatter: Callable) -> None:
        """
        Register a formatter for an action.
        
        Args:
            action_name: Name of the action to register the formatter for
            formatter: Formatter function
        """
        self.formatters[action_name] = formatter
    
    def register_formatters(self, formatters: Dict[str, Callable]) -> None:
        """
        Register multiple formatters.
        
        Args:
            formatters: Dictionary mapping action names to formatter functions
        """
        for action_name, formatter in formatters.items():
            self.register_formatter(action_name, formatter)
    
    def get_action(self, action_name: str) -> Optional[Callable]:
        """
        Get an action by name.
        
        Args:
            action_name: Name of the action to get
            
        Returns:
            Action function or None if not found
        """
        if action_name in self.actions:
            return self.actions[action_name]['function']
        return None
    
    def get_action_info(self, action_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about an action.
        
        Args:
            action_name: Name of the action to get information for
            
        Returns:
            Dictionary with action information or None if not found
        """
        return self.actions.get(action_name)
    
    def get_all_actions(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all registered actions.
        
        Returns:
            Dictionary mapping action names to action information
        """
        return self.actions
    
    def get_required_parameters(self, action_name: str) -> List[str]:
        """
        Get the required parameters for an action.
        
        Args:
            action_name: Name of the action to get required parameters for
            
        Returns:
            List of required parameter names
        """
        if action_name not in self.actions:
            return []
        
        parameters = self.actions[action_name]['parameters']
        return [name for name, info in parameters.items() if info.get('required', False)]
    
    def format_result(self, action_name: str, result: Any) -> str:
        """
        Format the result of an action.
        
        Args:
            action_name: Name of the action that produced the result
            result: Result to format
            
        Returns:
            Formatted result as a string
        """
        # If a custom formatter is registered, use it
        if action_name in self.formatters:
            return self.formatters[action_name](result)
        
        # If no formatter is available, use a simple default formatter
        # This will be replaced by LLM formatting in the LLMAdapter
        if isinstance(result, dict):
            return {"action": action_name, "result": result, "needs_llm_formatting": True}
        return str(result) 
"""
Unit tests for the action decorator.

This module contains tests for the action decorator functionality.
"""

import pytest
from actuator_ai import action
from actuator_ai.core.registry import ActionRegistry
from actuator_ai.core.decorators import is_action, get_action_name, get_action_description, get_action_parameters


def test_action_decorator_basic():
    """Test that the action decorator properly marks a function as an action."""
    @action(description="Test action")
    def test_func(param1, param2=None):
        """Test function docstring."""
        return {"param1": param1, "param2": param2}
    
    # Check that the function is marked as an action
    assert hasattr(test_func, "__action__")
    assert test_func.__action__ is True
    
    # Check that the action name is set correctly
    assert hasattr(test_func, "__action_name__")
    assert get_action_name(test_func) == "test_func"
    
    # Check that the description is set correctly
    assert hasattr(test_func, "__action_description__")
    assert get_action_description(test_func) == "Test action"
    
    # Check that the parameters are extracted correctly
    assert hasattr(test_func, "__action_parameters__")
    params = get_action_parameters(test_func)
    assert "param1" in params
    assert "param2" in params


def test_action_decorator_custom_name():
    """Test that the action decorator handles custom names correctly."""
    @action(name="custom_name", description="Test action with custom name")
    def test_func(param1):
        return {"param1": param1}
    
    assert get_action_name(test_func) == "custom_name"


def test_action_decorator_registry_integration(action_registry):
    """Test that the action decorator works with the ActionRegistry."""
    @action(description="Test action for registry")
    def test_func(param1):
        return {"param1": param1}
    
    # Register the action
    action_registry.register_action(test_func)
    
    # Check that the action is in the registry
    actions = action_registry.get_all_actions()
    assert "test_func" in actions
    
    # Check that the action info is correct
    action_info = action_registry.get_action_info("test_func")
    assert action_info["description"] == "Test action for registry"
    assert "param1" in action_info["parameters"]


def test_action_decorator_with_class_method():
    """Test that the action decorator works with class methods."""
    class TestClass:
        @action(description="Test class method action")
        def test_method(self, param1):
            return {"param1": param1}
    
    # Create an instance of the class
    test_instance = TestClass()
    
    # Check that the method is marked as an action
    assert is_action(test_instance.test_method)
    
    # Check that the action name is set correctly
    assert get_action_name(test_instance.test_method) == "test_method"


def test_action_decorator_docstring_as_description():
    """Test that the action decorator uses the docstring as description if none is provided."""
    @action()
    def test_func(param1):
        """This is a docstring that should be used as description."""
        return {"param1": param1}
    
    assert get_action_description(test_func) == "This is a docstring that should be used as description." 
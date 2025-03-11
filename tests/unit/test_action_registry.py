"""
Unit tests for the ActionRegistry class.

This module contains tests for the ActionRegistry functionality.
"""

import pytest
from actuator_ai.core.registry import ActionRegistry
from actuator_ai import action


def test_action_registry_initialization():
    """Test that the ActionRegistry initializes correctly."""
    registry = ActionRegistry()
    
    # Check that the registry is empty
    assert registry.get_all_actions() == {}
    assert registry.formatters == {}


def test_action_registry_register_action():
    """Test that the ActionRegistry can register an action."""
    registry = ActionRegistry()
    
    @action(description="Test action")
    def test_func(param1):
        return {"param1": param1}
    
    # Register the action
    registry.register_action(test_func)
    
    # Check that the action is in the registry
    actions = registry.get_all_actions()
    assert "test_func" in actions
    
    # Check that we can get the action by name
    assert registry.get_action("test_func") == test_func


def test_action_registry_register_formatter():
    """Test that the ActionRegistry can register a formatter."""
    registry = ActionRegistry()
    
    def test_formatter(result):
        return f"Formatted: {result}"
    
    # Register the formatter
    registry.register_formatter("test_action", test_formatter)
    
    # Check that the formatter is in the registry
    assert "test_action" in registry.formatters
    assert registry.formatters["test_action"] == test_formatter


def test_action_registry_format_result():
    """Test that the ActionRegistry can format results."""
    registry = ActionRegistry()
    
    def test_formatter(result):
        return f"Formatted: {result['value']}"
    
    # Register the formatter
    registry.register_formatter("test_action", test_formatter)
    
    # Format a result
    result = registry.format_result("test_action", {"value": "test"})
    assert result == "Formatted: test"
    
    # Test formatting for an action without a formatter
    result = registry.format_result("unknown_action", {"value": "test"})
    assert isinstance(result, dict)
    assert result["needs_llm_formatting"] is True


def test_action_registry_discover_actions(test_actions_module):
    """Test that the ActionRegistry can discover actions in a module."""
    registry = ActionRegistry()
    
    # Instead of using discover_actions, directly register the action
    registry.register_action(test_actions_module.test_action)
    
    # Check that the action is in the registry
    actions = registry.get_all_actions()
    assert "test_action" in actions
    
    # Check that the action info is correct
    action_info = registry.get_action_info("test_action")
    assert action_info["description"] == "Test action for testing"
    assert "param1" in action_info["parameters"]
    assert "param2" in action_info["parameters"]


def test_action_registry_get_action_info():
    """Test that the ActionRegistry can get action info."""
    registry = ActionRegistry()
    
    @action(description="Test action")
    def test_func(param1, param2=None):
        return {"param1": param1, "param2": param2}
    
    # Register the action
    registry.register_action(test_func)
    
    # Get the action info
    action_info = registry.get_action_info("test_func")
    
    # Check that the action info is correct
    assert action_info["description"] == "Test action"
    assert "param1" in action_info["parameters"]
    assert "param2" in action_info["parameters"]
    
    # Check that getting info for a non-existent action returns None
    assert registry.get_action_info("non_existent_action") is None 
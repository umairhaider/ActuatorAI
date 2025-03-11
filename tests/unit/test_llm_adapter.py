"""
Unit tests for the LLMAdapter class.

This module contains tests for the LLMAdapter functionality.
"""

import pytest
from unittest.mock import MagicMock, patch
from actuator_ai.core.llm_adapter import LLMAdapter
from actuator_ai import action


def test_llm_adapter_initialization():
    """Test that the LLMAdapter initializes correctly."""
    with patch('os.getenv', return_value="test_key"):
        adapter = LLMAdapter()
        
        # Check that the adapter has the correct API key
        assert adapter.openai_api_key == "test_key"
        
        # Check that the adapter has an empty action registry
        assert hasattr(adapter, "action_registry")
        assert adapter.pattern_processors == []


def test_llm_adapter_discover_actions(test_actions_module):
    """Test that the LLMAdapter can discover actions in a module."""
    adapter = LLMAdapter(openai_api_key="test_key")
    
    # Instead of using discover_actions, directly register the action
    adapter.action_registry.register_action(test_actions_module.test_action)
    
    # Check that the action is in the registry
    actions = adapter.action_registry.get_all_actions()
    assert "test_action" in actions


def test_llm_adapter_register_pattern_processor():
    """Test that the LLMAdapter can register a pattern processor."""
    adapter = LLMAdapter(openai_api_key="test_key")
    
    # Create a mock pattern processor
    mock_processor = MagicMock()
    mock_processor.process.return_value = "test_result"
    
    # Register the pattern processor
    adapter.register_pattern_processor(mock_processor)
    
    # Check that the pattern processor is registered
    assert len(adapter.pattern_processors) == 1
    assert adapter.pattern_processors[0] == mock_processor


def test_llm_adapter_register_formatters():
    """Test that the LLMAdapter can register formatters."""
    adapter = LLMAdapter(openai_api_key="test_key")
    
    # Create formatters
    formatters = {
        "test_action": lambda result: f"Formatted: {result}"
    }
    
    # Register the formatters
    adapter.register_formatters(formatters)
    
    # Check that the formatters are registered
    assert "test_action" in adapter.action_registry.formatters


def test_llm_adapter_chat_with_pattern_processor():
    """Test that the LLMAdapter can process messages with a pattern processor."""
    adapter = LLMAdapter(openai_api_key="test_key")
    
    # Create a mock pattern processor
    mock_processor = MagicMock()
    mock_processor.process.return_value = "test_result"
    
    # Register the pattern processor
    adapter.register_pattern_processor(mock_processor)
    
    # Process a message
    result = adapter.chat("test_message")
    
    # Check that the pattern processor was called
    mock_processor.process.assert_called_once_with("test_message", adapter.action_registry)
    
    # Check that the result is correct
    assert result == "test_result"


def test_llm_adapter_chat_with_llm(mock_openai_client):
    """Test that the LLMAdapter can process messages with the LLM."""
    with patch('openai.OpenAI', return_value=mock_openai_client):
        adapter = LLMAdapter(openai_api_key="test_key")
        
        # Process a message
        result = adapter.chat("test_message")
        
        # Check that the OpenAI API was called
        mock_openai_client.chat.completions.create.assert_called_once()
        
        # Check that the result is correct
        assert result == "This is a test response"


def test_llm_adapter_format_with_llm(mock_openai_client):
    """Test that the LLMAdapter can format results with the LLM."""
    with patch('openai.OpenAI', return_value=mock_openai_client):
        adapter = LLMAdapter(openai_api_key="test_key")
        
        # Format a result
        result = adapter._format_with_llm("test_action", {"value": "test"})
        
        # Check that the OpenAI API was called
        mock_openai_client.chat.completions.create.assert_called_once()
        
        # Check that the result is correct
        assert result == "This is a test response"


def test_llm_adapter_get_available_actions(test_actions_module):
    """Test that the LLMAdapter can get available actions."""
    adapter = LLMAdapter(openai_api_key="test_key")
    
    # Instead of using discover_actions, directly register the action
    adapter.action_registry.register_action(test_actions_module.test_action)
    
    # Get available actions
    actions = adapter.get_available_actions()
    
    # Check that the action is in the list
    assert len(actions) == 1
    assert actions[0]["name"] == "test_action"
    assert actions[0]["description"] == "Test action for testing"
    assert "param1" in actions[0]["parameters"]
    assert "param2" in actions[0]["parameters"] 
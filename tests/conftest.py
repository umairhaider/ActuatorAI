"""
Pytest configuration file for ActuatorAI tests.

This module provides fixtures and configuration for testing ActuatorAI.
"""

import os
import pytest
from unittest.mock import MagicMock, patch

from actuator_ai.core.llm_adapter import LLMAdapter
from actuator_ai.core.registry import ActionRegistry
from actuator_ai import action


@pytest.fixture
def action_registry():
    """Fixture for a clean ActionRegistry instance."""
    return ActionRegistry()


@pytest.fixture
def mock_openai_client():
    """Fixture for a mocked OpenAI client."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    
    # Set up the mock response structure
    mock_message.content = "This is a test response"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response
    
    return mock_client


@pytest.fixture
def llm_adapter(mock_openai_client):
    """Fixture for an LLMAdapter with a mocked OpenAI client."""
    with patch('openai.OpenAI', return_value=mock_openai_client):
        adapter = LLMAdapter(openai_api_key="test_key")
        yield adapter


@pytest.fixture
def test_actions_module():
    """Fixture for a module with test actions."""
    # Create a module-like object with the test action
    class TestActionsModule:
        pass
    
    # Define the test action using the action decorator
    @action(name="test_action", description="Test action for testing")
    def test_func(param1=None, param2=None):
        """Test action for testing."""
        return {
            "param1": param1,
            "param2": param2,
            "result": "test_result"
        }
    
    # Add the test action to the module
    setattr(TestActionsModule, "test_action", test_func)
    
    return TestActionsModule 
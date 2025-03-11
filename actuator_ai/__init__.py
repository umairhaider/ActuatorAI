"""
ActuatorAI: A framework for building natural language interfaces to actions.

This package provides a flexible way to create natural language interfaces
for your Python functions. Simply decorate your functions with @action and
they will be automatically discoverable and callable via natural language.
"""

__version__ = "0.1.0"

from actuator_ai.core.decorators import action
from actuator_ai.core.registry import ActionRegistry
from actuator_ai.core.llm_adapter import LLMAdapter
from actuator_ai.api.app import create_app, run_app

__all__ = [
    "action",
    "ActionRegistry",
    "LLMAdapter",
    "create_app",
    "run_app",
] 
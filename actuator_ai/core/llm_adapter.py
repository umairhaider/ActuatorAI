"""
LLM adapter for processing natural language messages.

This module provides an adapter for processing natural language messages using
various LLM providers (OpenAI, etc.).
"""

import os
import json
from typing import Dict, Any, List, Optional, Callable, Union

class LLMAdapter:
    """
    Adapter for processing natural language messages using LLMs.
    
    This class provides methods for processing natural language messages using
    various LLM providers (OpenAI, etc.).
    """
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """
        Initialize the LLM adapter.
        
        Args:
            openai_api_key: OpenAI API key (defaults to OPENAI_API_KEY environment variable)
        """
        from actuator_ai.core.registry import ActionRegistry
        
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        
        # For testing purposes, use a dummy key if none is provided
        if not self.openai_api_key:
            self.openai_api_key = "dummy_api_key_for_testing"
        
        self.action_registry = ActionRegistry()
        self.pattern_processors = []
    
    def discover_actions(self, module_or_class) -> None:
        """
        Discover actions in a module or class.
        
        Args:
            module_or_class: Module or class to discover actions in
        """
        self.action_registry.discover_actions(module_or_class)
    
    def discover_all_actions(self) -> None:
        """
        Discover all actions in the current package.
        
        This method attempts to discover actions in the 'actions' module of the
        current package.
        """
        try:
            import actions
            self.action_registry.discover_actions(actions)
        except ImportError:
            pass
    
    def register_pattern_processor(self, processor: Callable) -> None:
        """
        Register a pattern processor.
        
        Args:
            processor: Pattern processor function or object with a process method
        """
        self.pattern_processors.append(processor)
    
    def register_formatters(self, formatters: Dict[str, Callable]) -> None:
        """
        Register formatters for actions.
        
        Args:
            formatters: Dictionary mapping action names to formatter functions
        """
        self.action_registry.register_formatters(formatters)
    
    def chat(self, message: str) -> str:
        """
        Process a natural language message.
        
        Args:
            message: Natural language message to process
            
        Returns:
            Response to the message
        """
        # Try pattern processors first
        for processor in self.pattern_processors:
            if hasattr(processor, 'process'):
                result = processor.process(message, self.action_registry)
            else:
                result = processor(message, self.action_registry)
            
            if result:
                # Check if the result needs LLM formatting
                if isinstance(result, dict) and result.get("needs_llm_formatting", False):
                    return self._format_with_llm(result["action"], result["result"])
                return result
        
        # If no pattern processor matched, use the LLM
        return self._process_with_llm(message)
    
    def _process_with_llm(self, message: str) -> str:
        """
        Process a message using the LLM.
        
        Args:
            message: Message to process
            
        Returns:
            Response from the LLM
        """
        import openai
        from openai import OpenAI
        
        # Create a client
        client = OpenAI(api_key=self.openai_api_key)
        
        # Get all available actions
        actions = self.action_registry.get_all_actions()
        
        # Create a prompt for the LLM
        action_descriptions = []
        for action_name, details in actions.items():
            description = details.get('description', '')
            parameters = details.get('parameters', {})
            param_descriptions = []
            for param_name, param_info in parameters.items():
                param_descriptions.append(f"- {param_name}: {param_info.get('description', '')}")
            
            action_descriptions.append(f"Action: {action_name}\nDescription: {description}\nParameters:\n" + "\n".join(param_descriptions))
        
        # Join action descriptions with double newlines
        joined_descriptions = "\n\n".join(action_descriptions)
        
        prompt = f"""
You are an AI assistant that can help with various tasks. You have access to the following actions:

{joined_descriptions}

User message: {message}

Please respond to the user's message. If you need to use one of the available actions, please say so.
"""
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Extract the response
        return response.choices[0].message.content
    
    def _format_with_llm(self, action_name: str, result: Dict[str, Any]) -> str:
        """
        Format a result using the LLM.
        
        Args:
            action_name: Name of the action that produced the result
            result: Result to format
            
        Returns:
            Formatted result as a string
        """
        import openai
        from openai import OpenAI
        
        # Create a client
        client = OpenAI(api_key=self.openai_api_key)
        
        # Get action info
        action_info = self.action_registry.get_action_info(action_name)
        description = action_info.get("description", "") if action_info else ""
        
        # Create a prompt for the LLM
        prompt = f"""
You are an AI assistant that formats the results of actions in a natural, human-friendly way.

Action: {action_name}
Description: {description}
Result: {result}

Please format this result as a natural language response that would be helpful and informative to a user.
Keep your response concise and focused on the information in the result.
Do not add any disclaimers, explanations about yourself, or additional information not present in the result.
"""
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that formats action results in a natural way."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        # Extract the response
        formatted_response = response.choices[0].message.content.strip()
        return formatted_response
    
    def get_available_actions(self) -> List[Dict[str, Any]]:
        """
        Get information about all available actions.
        
        Returns:
            List of dictionaries with action information
        """
        actions = []
        for action_name, details in self.action_registry.get_all_actions().items():
            actions.append({
                "name": action_name,
                "description": details.get('description', ''),
                "parameters": details.get('parameters', {})
            })
        return actions 
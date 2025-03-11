"""
Main entry point for the weather bot example.

This module provides a main entry point for the weather bot example.
"""

import os
import sys
import argparse
from actuator_ai import run_app
from actuator_ai.core.patterns import get_simple_pattern_matcher

# Import actions and formatters
from actuator_ai.examples.weather_bot import actions
from actuator_ai.examples.weather_bot import formatters

def main(args=None):
    """
    Main entry point for the weather bot example.
    
    Args:
        args: Command line arguments
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Weather Bot Example")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=5005, help="Port to run the server on")
    parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    
    # Parse arguments
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)
    
    # Get the OpenAI API key from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    # Create a function to set up the LLM adapter
    def setup_llm_adapter(llm_adapter):
        # Register the simple pattern matcher
        llm_adapter.register_pattern_processor(get_simple_pattern_matcher())
        
        # Register formatters
        llm_adapter.register_formatters(formatters.ACTION_FORMATTERS)
    
    # Run the application
    run_app(
        actions_module=actions,
        openai_api_key=openai_api_key,
        host=args.host,
        port=args.port,
        reload=not args.no_reload,
        title="Weather Bot API",
        description="API for processing natural language messages about weather, time, and calculations",
        version="0.1.0",
        setup_llm_adapter=setup_llm_adapter
    )

if __name__ == "__main__":
    main() 
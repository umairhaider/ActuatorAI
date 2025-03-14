"""
Command-line interface for the ActuatorAI framework.

This module provides a command-line interface for the ActuatorAI framework,
allowing users to start the API server and perform other tasks.
"""

import argparse
import importlib
import os
import sys
from typing import Optional

def main():
    """Main entry point for the ActuatorAI CLI."""
    parser = argparse.ArgumentParser(description="ActuatorAI CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Server command
    server_parser = subparsers.add_parser("server", help="Start the API server")
    server_parser.add_argument("--host", default="0.0.0.0", help="Host to run the server on")
    server_parser.add_argument("--port", type=int, default=5005, help="Port to run the server on")
    server_parser.add_argument("--actions", help="Module containing actions to discover")
    server_parser.add_argument("--openai-api-key", help="OpenAI API key")
    server_parser.add_argument("--telegram-token", help="Telegram bot token")
    server_parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    
    # Run command (alias for server, but with a simpler name)
    run_parser = subparsers.add_parser("run", help="Run the API server (alias for 'server')")
    run_parser.add_argument("--host", default="0.0.0.0", help="Host to run the server on")
    run_parser.add_argument("--port", type=int, default=5005, help="Port to run the server on")
    run_parser.add_argument("--actions", help="Module containing actions to discover")
    run_parser.add_argument("--openai-api-key", help="OpenAI API key")
    run_parser.add_argument("--telegram-token", help="Telegram bot token")
    run_parser.add_argument("--no-reload", action="store_true", help="Disable auto-reload")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new ActuatorAI project")
    init_parser.add_argument("project_name", help="Name of the project to create")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "server" or args.command == "run":
        run_server(
            host=args.host,
            port=args.port,
            actions_module=args.actions,
            openai_api_key=args.openai_api_key,
            telegram_token=args.telegram_token,
            reload=not args.no_reload
        )
    elif args.command == "init":
        init_project(args.project_name)
    else:
        # If no command is provided, default to run
        if len(sys.argv) == 1:
            print("No command specified. Running the server with default settings...")
            run_server()
        else:
            parser.print_help()

def run_server(
    host: str = "0.0.0.0",
    port: int = 5005,
    actions_module: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    telegram_token: Optional[str] = None,
    reload: bool = True
):
    """
    Start the API server.
    
    Args:
        host: Host to run the server on
        port: Port to run the server on
        actions_module: Module containing actions to discover
        openai_api_key: OpenAI API key
        telegram_token: Telegram bot token
        reload: Whether to reload the server on code changes
    """
    from actuator_ai.api.app import run_app
    from actuator_ai.core.patterns import get_simple_pattern_matcher
    
    # Import the actions module if specified
    actions_module_obj = None
    if actions_module:
        try:
            actions_module_obj = importlib.import_module(actions_module)
        except ImportError:
            print(f"Error: Could not import actions module '{actions_module}'")
            sys.exit(1)
    
    # Create a function to set up the LLM adapter
    def setup_llm_adapter(llm_adapter):
        # Register the simple pattern matcher
        llm_adapter.register_pattern_processor(get_simple_pattern_matcher())
        
        # Try to import formatters if available
        try:
            if actions_module:
                formatters_module = f"{actions_module}.formatters"
                formatters = importlib.import_module(formatters_module)
                if hasattr(formatters, "ACTION_FORMATTERS"):
                    llm_adapter.register_formatters(formatters.ACTION_FORMATTERS)
        except ImportError:
            # No formatters module, that's fine
            pass
    
    # Run the application
    run_app(
        actions_module=actions_module_obj,
        openai_api_key=openai_api_key,
        telegram_token=telegram_token,
        host=host,
        port=port,
        reload=reload,
        setup_llm_adapter=setup_llm_adapter
    )

def init_project(project_name: str):
    """
    Initialize a new ActuatorAI project.
    
    Args:
        project_name: Name of the project to create
    """
    import shutil
    from pathlib import Path
    
    # Create project directory
    project_dir = Path(project_name)
    if project_dir.exists():
        print(f"Error: Directory '{project_name}' already exists")
        sys.exit(1)
    
    project_dir.mkdir()
    
    # Create actions.py
    with open(project_dir / "actions.py", "w") as f:
        f.write("""\"\"\"
Actions for the ActuatorAI project.

This module contains actions that can be discovered by the ActuatorAI framework
and called via natural language.
\"\"\"

from datetime import datetime
import random
from actuator_ai import action

@action(description="Get the current time, optionally for a specific timezone")
def get_time(timezone=None):
    \"\"\"
    Get the current time, optionally for a specific timezone.
    
    Args:
        timezone (str, optional): The timezone to get the time for. Defaults to local time.
        
    Returns:
        dict: A dictionary containing the current time and timezone information.
    \"\"\"
    # In a real implementation, this would handle different timezones
    current_time = datetime.now()
    
    # Format the time
    formatted_time = current_time.strftime("%H:%M:%S")
    formatted_date = current_time.strftime("%Y-%m-%d")
    
    # Use the provided timezone or default to "local"
    tz = timezone or "local"
    
    return {
        "time": formatted_time,
        "date": formatted_date,
        "timezone": tz,
        "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S")
    }

@action(description="Calculate the result of a mathematical expression")
def calculate(expression):
    \"\"\"
    Calculate the result of a mathematical expression.
    
    Args:
        expression (str): The mathematical expression to evaluate.
        
    Returns:
        dict: A dictionary containing the expression and its result.
    \"\"\"
    try:
        # Use eval to calculate the result (note: in a production environment,
        # you should use a safer alternative to eval)
        result = eval(expression, {"__builtins__": {}}, {})
        
        return {
            "expression": expression,
            "result": result
        }
    except Exception as e:
        return {
            "expression": expression,
            "error": str(e)
        }
""")
    
    # Create formatters.py
    with open(project_dir / "formatters.py", "w") as f:
        f.write("""\"\"\"
Formatters for the ActuatorAI project.

This module contains formatters for formatting the results of actions.
If you don't provide a formatter for an action, the system will automatically
use the LLM to format the result in a natural, human-friendly way.
\"\"\"

def format_time_result(result):
    \"\"\"
    Format the result of the get_time action.
    
    Args:
        result: Result from the get_time action
        
    Returns:
        Formatted result as a string
    \"\"\"
    return f"The current time is {result['time']} on {result['date']} ({result['timezone']} timezone)"

def format_calculate_result(result):
    \"\"\"
    Format the result of the calculate action.
    
    Args:
        result: Result from the calculate action
        
    Returns:
        Formatted result as a string
    \"\"\"
    if "error" in result:
        return f"Error calculating {result['expression']}: {result['error']}"
    return f"The result of {result['expression']} is {result['result']}"

def format_random_number_result(result):
    \"\"\"
    Format the result of the get_random_number action.
    
    Args:
        result: Result from the get_random_number action
        
    Returns:
        Formatted result as a string
    \"\"\"
    return f"Random number between {{result['min']}} and {{result['max']}}: {{result['number']}}"

# Dictionary mapping action names to formatter functions
ACTION_FORMATTERS = {
    "get_time": format_time_result,
    "calculate": format_calculate_result,
    "get_random_number": format_random_number_result,
}

# Note: For any action without a formatter, the LLM will automatically
# generate a natural language response based on the action's result.
""")
    
    # Create main.py
    with open(project_dir / "main.py", "w") as f:
        f.write("""\"\"\"
Main entry point for the ActuatorAI project.
\"\"\"

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import actions
import actions

from actuator_ai.api.app import run_app

def main():
    \"\"\"Main entry point for the ActuatorAI project.\"\"\"
    # Get the OpenAI API key from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    # Get the Telegram bot token from environment variables (optional)
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    # Run the application
    run_app(
        actions_module=actions,
        openai_api_key=openai_api_key,
        telegram_token=telegram_token,
        title="My ActuatorAI API",
        description="API for processing natural language messages",
        version="0.1.0"
    )

if __name__ == "__main__":
    main()
""")
    
    # Create .env file
    with open(project_dir / ".env", "w") as f:
        f.write("""# OpenAI API key
OPENAI_API_KEY=your_openai_api_key

# Telegram bot token (optional)
# TELEGRAM_BOT_TOKEN=your_telegram_bot_token
""")
    
    # Create requirements.txt
    with open(project_dir / "requirements.txt", "w") as f:
        f.write("""actuator-ai==0.1.0
python-dotenv==1.0.1
""")
    
    # Create README.md
    with open(project_dir / "README.md", "w") as f:
        f.write(f"""# {project_name}

A natural language interface for actions built with ActuatorAI.

## Setup

1. Create a virtual environment (optional but recommended):
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Edit the `.env` file
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```
   - (Optional) Add your Telegram bot token to the `.env` file:
     ```
     TELEGRAM_BOT_TOKEN=your_telegram_bot_token
     ```

## Running the Application

Start the FastAPI server:
```
python main.py
```

Or use the ActuatorAI CLI:
```
actuator-ai server --actions actions
```

## Testing the API

### REST API
```
curl -X POST http://localhost:5005/webhooks/rest/webhook \\
  -H "Content-Type: application/json" \\
  -d '{{"sender": "user", "message": "What time is it?"}}'
```

### Telegram Bot Integration

1. Create a Telegram bot using BotFather (https://t.me/botfather)
2. Get your bot token and add it to the `.env` file
3. Set the webhook URL for your bot:
   ```
   curl -X POST http://localhost:5005/telegram/set-webhook?webhook_url=https://your-public-url.com/webhooks/telegram/webhook
   ```
   Note: You need a public URL for Telegram to send updates to your bot. You can use ngrok for testing.
4. Start chatting with your bot on Telegram!
""")
    
    print(f"Initialized new ActuatorAI project in '{project_name}'")
    print(f"To get started, cd into '{project_name}' and run:")
    print("  pip install -r requirements.txt")
    print("  python main.py")

if __name__ == "__main__":
    main()
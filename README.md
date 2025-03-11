# ActuatorAI: Natural Language Interface for Actions

<div align="center">
     <img src="https://raw.githubusercontent.com/umairhaider/ActuatorAI/main/actuator-ai-logo.png" alt="ActuatorAI Logo" width="300">
  <p><em>Talk to your Python Actions.</em></p>
</div>

[![PyPI version](https://badge.fury.io/py/actuator-ai.svg)](https://badge.fury.io/py/actuator-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Run Tests](https://github.com/umairhaider/ActuatorAI/actions/workflows/test.yml/badge.svg)](https://github.com/umairhaider/ActuatorAI/actions/workflows/test.yml)
[![Pull Request Checks](https://github.com/umairhaider/ActuatorAI/actions/workflows/pr-checks.yml/badge.svg)](https://github.com/umairhaider/ActuatorAI/actions/workflows/pr-checks.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Maintainability](https://img.shields.io/badge/maintainability-A-brightgreen)](https://github.com/umairhaider/ActuatorAI)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/umairhaider/ActuatorAI/blob/main/CONTRIBUTING.md)
[![OpenAI Compatible](https://img.shields.io/badge/OpenAI-Compatible-brightgreen)](https://openai.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.11-009688.svg)](https://fastapi.tiangolo.com/)

ActuatorAI is a conversational AI framework powerd by LLMs for building natural language interfaces to your Python functions. It allows you to create conversational interfaces that can execute actions based on natural language input.

## Features

- **Simple Action Definition**: Decorate your functions with `@action` to make them callable via natural language
- **Automatic Discovery**: Actions are automatically discovered and registered
- **Flexible API**: Rasa-compatible API for processing natural language messages
- **Customizable Formatters**: Format action results in a user-friendly way
- **LLM-Based Formatting**: Automatic natural language formatting when no custom formatter is provided
- **Easy Integration**: Works with any Python function or method

## Installation

```bash
pip install actuator-ai
```

## Quick Start

### 1. Initialize a New Project

```bash
actuator-ai init myproject
cd myproject
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Your OpenAI API Key

Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the Application

```bash
python main.py
```

### 5. Test the API

```bash
# Time query
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "user", "message": "What time is it?"}'

# Calculator
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "user", "message": "Calculate 15 * 7 + 3"}'
```

## Creating Actions

Actions are Python functions decorated with `@action`. Here's an example:

```python
from actuator_ai import action

@action(description="Get a random number between two values")
def get_random_number(min_value=0, max_value=100):
    """
    Get a random number between two values.
    
    Args:
        min_value (int, optional): Minimum value. Defaults to 0.
        max_value (int, optional): Maximum value. Defaults to 100.
        
    Returns:
        dict: A dictionary containing the random number and the range.
    """
    import random
    number = random.randint(min_value, max_value)
    return {
        "number": number,
        "min": min_value,
        "max": max_value
    }
```

## Formatting Results

You have two options for formatting action results:

### Option 1: Custom Formatters (Recommended for Production)

Create formatters for precise control over output formatting:

```python
def format_random_number_result(result):
    """
    Format the result of the get_random_number action.
    
    Args:
        result: Result from the get_random_number action
        
    Returns:
        Formatted result as a string
    """
    return f"Random number between {result['min']} and {result['max']}: {result['number']}"

# Add the formatter to the ACTION_FORMATTERS dictionary
ACTION_FORMATTERS["get_random_number"] = format_random_number_result
```

### Option 2: LLM-Based Formatting (Great for Rapid Development)

If you don't provide a formatter, the system will automatically use the LLM to format the result in a natural, human-friendly way. This is perfect for:

- Rapid prototyping
- Simple actions
- When you want natural language responses

For example, with the action above but no formatter, the LLM might format the result as:
```
I've generated a random number for you: 42. This number is between 0 and 100.
```

The LLM uses the action name, description, and result data to create a natural response.

## API Reference

### Decorators

#### `@action(name=None, description="")`

Decorator to mark a function as an action that can be discovered by the action registry.

- `name`: Optional custom name for the action (defaults to the function name)
- `description`: Description of what the action does

### Classes

#### `ActionRegistry`

Registry for discovering and managing actions.

- `discover_actions(module_or_class)`: Discover actions in a module or class
- `register_action(func)`: Register an action
- `register_formatter(action_name, formatter)`: Register a formatter for an action
- `get_action(action_name)`: Get an action by name
- `get_all_actions()`: Get all registered actions

#### `LLMAdapter`

Adapter for processing natural language messages using LLMs.

- `discover_actions(module_or_class)`: Discover actions in a module or class
- `register_pattern_processor(processor)`: Register a pattern processor
- `register_formatters(formatters)`: Register formatters for actions
- `chat(message)`: Process a natural language message

### Functions

#### `create_app(actions_module=None, openai_api_key=None, ...)`

Create a FastAPI application for the ActuatorAI framework.

#### `run_app(actions_module=None, openai_api_key=None, ...)`

Run the FastAPI application.

## CLI Reference

### `actuator-ai init <project_name>`

Initialize a new ActuatorAI project.

### `actuator-ai server [options]`

Start the API server.

Options:
- `--host`: Host to run the server on (default: 0.0.0.0)
- `--port`: Port to run the server on (default: 5005)
- `--actions`: Module containing actions to discover
- `--openai-api-key`: OpenAI API key
- `--no-reload`: Disable auto-reload

## Examples

Check out the examples directory for more examples:

- [Weather Bot](actuator_ai/examples/weather_bot): A simple weather bot that can tell you the weather, time, and perform calculations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Testing

ActuatorAI includes a comprehensive test suite. To run the tests:

```bash
./run_tests.sh
```

This will run unit tests, integration tests, and generate a coverage report.

## Releasing

ActuatorAI uses GitHub Actions to automate the release process. To release a new version:

1. Create a new branch with the format `release/x.y.z` (e.g., `release/0.2.0`)
   ```bash
   git checkout -b release/0.2.0
   ```

2. Push the branch to GitHub
   ```bash
   git push -u origin release/0.2.0
   ```

3. The GitHub Actions workflow will automatically:
   - Extract the version from the branch name
   - Update the version in setup.py
   - Build the package
   - Run tests
   - Create a GitHub Release with the tag v0.2.0
   - Publish the package to PyPI

4. You can also manually trigger the workflow from the GitHub Actions tab.

**Note**: You need to set up a PyPI API token as a GitHub secret named `PYPI_API_TOKEN` for the publishing step to work.

## Branch Protection

To ensure code quality and prevent merges when tests fail, you should set up branch protection rules in GitHub:

1. Go to your GitHub repository
2. Navigate to Settings > Branches
3. Click "Add rule" under "Branch protection rules"
4. In "Branch name pattern", enter `main` (or `master` if that's your default branch)
5. Enable the following options:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
6. In the "Status checks that are required" section, search for and select:
   - "Validate PR"
7. Click "Create" or "Save changes"

With these settings, pull requests to the main branch will require the tests to pass before merging is allowed.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
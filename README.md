# ActuatorAI

<div align="center">
  <img src="https://raw.githubusercontent.com/umairhaider/ActuatorAI/main/actuator-ai.png" alt="ActuatorAI Logo" width="300">
  <h3>Natural Language Interface for Actions</h3>
  <p><em>Talk to your Python Actions.</em></p>
  
  [![PyPI version](https://badge.fury.io/py/actuator-ai.svg)](https://badge.fury.io/py/actuator-ai)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![Run Tests](https://github.com/umairhaider/ActuatorAI/actions/workflows/test.yml/badge.svg)](https://github.com/umairhaider/ActuatorAI/actions/workflows/test.yml)
  [![Pull Request Checks](https://github.com/umairhaider/ActuatorAI/actions/workflows/pr-checks.yml/badge.svg)](https://github.com/umairhaider/ActuatorAI/actions/workflows/pr-checks.yml)
  [![Maintainability](https://img.shields.io/badge/maintainability-A-brightgreen)](https://github.com/umairhaider/ActuatorAI)
  [![OpenAI Compatible](https://img.shields.io/badge/OpenAI-Compatible-brightgreen)](https://openai.com/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-0.115.11-009688.svg)](https://fastapi.tiangolo.com/)
</div>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-creating-actions">Creating Actions</a> •
  <a href="#-api-reference">API Reference</a> •
  <a href="#-examples">Examples</a>
</p>

<div align="center">
  <br>
  <pre align="center">
  <code>pip install actuator-ai</code>
  </pre>
</div>

## 📖 Overview

ActuatorAI is a conversational AI framework powered by LLMs for building natural language interfaces to your Python functions. It enables you to:

- 🗣️ **Create conversational interfaces** that understand natural language
- 🔄 **Execute Python functions** based on user requests
- 🤖 **Leverage LLMs** for understanding and formatting
- 🔌 **Integrate easily** with existing Python code

<div align="center">
  <table>
    <tr>
      <td align="center">
        <b>User:</b> <i>"What's the weather in San Francisco?"</i>
      </td>
    </tr>
    <tr>
      <td align="center">
        <b>ActuatorAI:</b> <i>"It's currently 72°F and sunny in San Francisco."</i>
      </td>
    </tr>
  </table>
</div>

## ✨ Features

- **🔸 Simple Action Definition** - Decorate your functions with `@action` to make them callable via natural language
- **🔸 Automatic Discovery** - Actions are automatically discovered and registered
- **🔸 Flexible API** - Rasa-compatible API for processing natural language messages
- **🔸 Customizable Formatters** - Format action results in a user-friendly way
- **🔸 LLM-Based Formatting** - Automatic natural language formatting when no custom formatter is provided
- **🔸 Easy Integration** - Works with any Python function or method

## 🚀 Installation

```bash
pip install actuator-ai
```

## 🏁 Quick Start

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

## 🛠️ Creating Actions

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

## 💬 Formatting Results

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

## 📚 API Reference

### Decorators

#### `@action(name=None, description="")`

Decorator to mark a function as an action that can be discovered by the action registry.

- `name`: Optional custom name for the action (defaults to the function name)
- `description`: Description of what the action does

### Classes

#### `ActionRegistry`

Registry for discovering and managing actions.

| Method | Description |
|--------|-------------|
| `discover_actions(module_or_class)` | Discover actions in a module or class |
| `register_action(func)` | Register an action |
| `register_formatter(action_name, formatter)` | Register a formatter for an action |
| `get_action(action_name)` | Get an action by name |
| `get_all_actions()` | Get all registered actions |

#### `LLMAdapter`

Adapter for processing natural language messages using LLMs.

| Method | Description |
|--------|-------------|
| `discover_actions(module_or_class)` | Discover actions in a module or class |
| `register_pattern_processor(processor)` | Register a pattern processor |
| `register_formatters(formatters)` | Register formatters for actions |
| `chat(message)` | Process a natural language message |

### Functions

#### `create_app(actions_module=None, openai_api_key=None, ...)`

Create a FastAPI application for the ActuatorAI framework.

#### `run_app(actions_module=None, openai_api_key=None, ...)`

Run the FastAPI application.

## 💻 CLI Reference

### `actuator-ai init <project_name>`

Initialize a new ActuatorAI project.

### `actuator-ai server [options]`

Start the API server.

| Option | Description |
|--------|-------------|
| `--host` | Host to run the server on (default: 0.0.0.0) |
| `--port` | Port to run the server on (default: 5005) |
| `--actions` | Module containing actions to discover |
| `--openai-api-key` | OpenAI API key |
| `--no-reload` | Disable auto-reload |

## 📋 Examples

Check out the examples directory for more examples:

- [Weather Bot](actuator_ai/examples/weather_bot): A simple weather bot that can tell you the weather, time, and perform calculations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
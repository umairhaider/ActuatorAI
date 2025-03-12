# ActuatorAI

<div align="center">
  <img src="https://raw.githubusercontent.com/umairhaider/ActuatorAI/main/actuator-ai.png" alt="ActuatorAI Logo" width="200"/>
  <p><strong>A powerful framework for building natural language interfaces to actions</strong></p>
</div>

## Overview

ActuatorAI makes it easy to create AI-powered interfaces that can understand natural language requests and execute corresponding actions. It provides a clean, declarative API for defining actions and their natural language triggers.

## Features

- ✨ **Simple Declarative API** - Define actions with intuitive decorators
- 🧠 **Built-in LLM Integration** - Leverages state-of-the-art language models
- 🔌 **Extensible Architecture** - Create custom actions, formatters, and adapters
- 🌐 **API Server** - Ready-to-use FastAPI server for web integration
- 🛠️ **Customizable** - Configure to use different LLM providers

## Installation

```bash
pip install actuator-ai
```

## Quick Start

### Basic Usage

```python
from actuator_ai.core import action, ActuatorAI

# Define an action with a natural language pattern
@action("Get the weather for {location}")
def get_weather(location: str):
    # Your implementation here
    return {"temperature": 72, "condition": "sunny"}

# Create an ActuatorAI instance
ai = ActuatorAI()

# Process a natural language request
result = ai.process("What's the weather in San Francisco?")
print(result)
```

### Multiple Actions

```python
@action("Find restaurants in {city}")
def find_restaurants(city: str):
    return {"restaurants": ["Restaurant A", "Restaurant B"]}

@action("Book a flight from {origin} to {destination}")
def book_flight(origin: str, destination: str):
    return {"flight": "AB123", "departure": "9:00 AM"}

# ActuatorAI will automatically determine which action to use
result = ai.process("Find me some restaurants in New York")
```

## API Server

ActuatorAI includes a ready-to-use FastAPI server:

```python
from actuator_ai.api import create_app

app = create_app()

# Run with: uvicorn my_module:app --reload
```

## Documentation

For full documentation, examples, and advanced usage, visit our [GitHub repository](https://github.com/umairhaider/ActuatorAI).

## License

MIT 
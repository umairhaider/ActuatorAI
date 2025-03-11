#!/bin/bash

# Run unit tests
echo "Running unit tests..."
python -m pytest tests/unit -v

# Run integration tests
echo "Running integration tests..."
python -m pytest tests/integration -v

# Run all tests with coverage
echo "Running all tests with coverage..."
python -m pytest --cov=actuator_ai --cov-report=term --cov-report=html --cov-report=xml 
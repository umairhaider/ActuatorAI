"""
FastAPI application for the ActuatorAI framework.

This module provides a FastAPI application for the ActuatorAI framework,
including endpoints for processing natural language messages.
"""

import os
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

from actuator_ai.core.llm_adapter import LLMAdapter

# Models for API requests and responses
class Entity(BaseModel):
    """Model for an entity extracted from a message."""
    start: int = 0
    end: int = 0
    value: str
    entity: str
    confidence: float = 1.0

class Intent(BaseModel):
    """Model for an intent extracted from a message."""
    confidence: float
    name: str

class ParseData(BaseModel):
    """Model for parsed message data."""
    entities: List[Entity] = []
    intent: Intent
    intent_ranking: List[Intent] = []
    text: str
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = {}

class WebhookRequest(BaseModel):
    """Model for webhook requests."""
    sender: str
    message: str

class WebhookResponse(BaseModel):
    """Model for webhook responses."""
    recipient_id: str
    text: str

class Message(BaseModel):
    """Model for a message."""
    event: str = "user"
    timestamp: Optional[float] = None
    metadata: Dict[str, Any] = {}
    text: str
    input_channel: str = "rest"
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    parse_data: Optional[ParseData] = None

def create_app(
    actions_module=None,
    openai_api_key=None,
    title="ActuatorAI API",
    description="API for processing natural language messages",
    version="0.1.0",
    setup_llm_adapter=None
) -> FastAPI:
    """
    Create a FastAPI application for the ActuatorAI framework.
    
    Args:
        actions_module: Module containing actions to discover
        openai_api_key: OpenAI API key
        title: API title
        description: API description
        version: API version
        setup_llm_adapter: Function to set up the LLM adapter
        
    Returns:
        FastAPI application
    """
    # Create the FastAPI application
    app = FastAPI(
        title=title,
        description=description,
        version=version,
    )
    
    # Initialize the LLM adapter
    def get_llm_adapter():
        """Get the LLM adapter with all actions and processors registered."""
        # Get the OpenAI API key
        api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        
        # Debug print
        print(f"DEBUG: openai_api_key in get_llm_adapter: {openai_api_key}")
        print(f"DEBUG: OPENAI_API_KEY env var in get_llm_adapter: {os.getenv('OPENAI_API_KEY')}")
        print(f"DEBUG: Final api_key in get_llm_adapter: {api_key}")
        
        # Create the LLM adapter
        adapter = LLMAdapter(openai_api_key=api_key)
        
        # Discover actions
        if actions_module:
            adapter.discover_actions(actions_module)
        else:
            adapter.discover_all_actions()
        
        # Set up the LLM adapter if a setup function is provided
        if setup_llm_adapter:
            setup_llm_adapter(adapter)
        
        return adapter
    
    # Define API endpoints
    @app.get("/")
    async def root() -> Dict[str, str]:
        """Root endpoint to check if the API is running."""
        return {
            "status": "API is running", 
            "message": "Use the /webhooks/rest/webhook endpoint for natural language processing",
            "version": version
        }
    
    @app.get("/status")
    async def status() -> Dict[str, Any]:
        """Status endpoint to check if the API is running."""
        return {
            "status": "ok",
            "version": version,
            "available_endpoints": [
                "/",
                "/status",
                "/webhooks/rest/webhook",
                "/model/parse"
            ]
        }
    
    @app.post("/webhooks/{rest_channel}/webhook", response_model=List[WebhookResponse])
    async def webhook(
        rest_channel: str,
        request: WebhookRequest, 
        llm_adapter: LLMAdapter = Depends(get_llm_adapter)
    ) -> List[WebhookResponse]:
        """
        Process a natural language message using the LLM adapter.
        
        Args:
            rest_channel: The REST channel to use (e.g., "rest", "callback")
            request: WebhookRequest containing the sender and message
            
        Returns:
            List of WebhookResponse containing the response
        """
        if rest_channel not in ["rest", "callback"]:
            raise HTTPException(status_code=400, detail=f"Invalid REST channel: {rest_channel}")
        
        try:
            # Process the message using the LLM adapter
            response = llm_adapter.chat(request.message)
            
            # Return the response in the expected webhook format
            return [
                WebhookResponse(
                    recipient_id=request.sender,
                    text=response
                )
            ]
        except Exception as e:
            # If there's an unexpected error, provide a helpful error message
            error_message = f"I'm sorry, I encountered an unexpected error: {str(e)}"
            return [
                WebhookResponse(
                    recipient_id=request.sender,
                    text=error_message
                )
            ]
    
    @app.post("/model/parse", response_model=ParseData)
    async def parse(
        message: Message,
        llm_adapter: LLMAdapter = Depends(get_llm_adapter)
    ) -> ParseData:
        """
        Parse a natural language message and extract intents and entities.
        
        Args:
            message: Message containing the message to parse
            
        Returns:
            ParseData containing the parsed message
        """
        try:
            # Process the message using the LLM adapter
            response = llm_adapter.chat(message.text)
            
            # For now, just return a simple intent and no entities
            # In a real implementation, you would parse the response to extract intents and entities
            return ParseData(
                entities=[],
                intent=Intent(name="default", confidence=1.0),
                intent_ranking=[Intent(name="default", confidence=1.0)],
                text=message.text,
                message_id=message.message_id
            )
        except Exception as e:
            # If there's an error, return a fallback intent
            return ParseData(
                entities=[],
                intent=Intent(name="nlu_fallback", confidence=0.3),
                intent_ranking=[Intent(name="nlu_fallback", confidence=0.3)],
                text=message.text,
                message_id=message.message_id
            )
    
    return app

def run_app(
    actions_module=None,
    openai_api_key=None,
    host="0.0.0.0",
    port=5005,
    reload=True,
    setup_llm_adapter=None,
    **kwargs
):
    """
    Run the FastAPI application.
    
    Args:
        actions_module: Module containing actions to discover
        openai_api_key: OpenAI API key
        host: Host to run the application on
        port: Port to run the application on
        reload: Whether to reload the application on code changes
        setup_llm_adapter: Function to set up the LLM adapter
        **kwargs: Additional arguments to pass to create_app
    """
    import uvicorn
    
    # Create the application
    app = create_app(
        actions_module=actions_module,
        openai_api_key=openai_api_key,
        setup_llm_adapter=setup_llm_adapter,
        **kwargs
    )
    
    # If reload is True, we need to use a different approach
    if reload:
        # Run the application with reload=True
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=False  # We disable reload here to avoid the warning
        )
    else:
        # Run the application without reload
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=False
        ) 
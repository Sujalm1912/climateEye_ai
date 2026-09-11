"""Chat API Route.

Endpoint for interacting with ClimateEye AI's environmental intelligence chatbot.
"""

from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.gemini_service import gemini_service

router = APIRouter(prefix="/api/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    """Schema for incoming chat query."""
    message: str = Field(..., min_length=1, description="User's environmental question")
    context: Optional[str] = Field(None, description="Optional environmental context")


@router.post("")
async def chat_endpoint(request: Optional[ChatRequest] = None):
    """Chat endpoint for environmental AI intelligence.

    In this initial phase, returns a placeholder response indicating service readiness.
    If Gemini API key is configured and a message is supplied, prepares generation.
    """
    if request and gemini_service.is_configured():
        try:
            response_text = await gemini_service.generate_response(
                prompt=request.message,
                context=request.context,
            )
            return {
                "status": "ok",
                "response": response_text,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Gemini generation error: {str(e)}",
            }

    return {
        "status": "not implemented yet",
        "message": "Chat endpoint ready for Gemini AI integration. Chatbot will be built in the next phase.",
        "gemini_configured": gemini_service.is_configured(),
    }

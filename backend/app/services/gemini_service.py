"""Gemini AI Service for ClimateEye AI.

Prepares client configuration using the official google-genai SDK.
Loads GEMINI_API_KEY securely from environment variables.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()


class GeminiService:
    """Encapsulates Gemini API interactions using google-genai SDK."""

    def __init__(self):
        self.api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self._client: Optional[genai.Client] = None

    def is_configured(self) -> bool:
        """Check whether a valid Gemini API key is configured."""
        return bool(self.api_key and self.api_key.strip() and self.api_key != "your_gemini_api_key_here")

    def get_client(self) -> genai.Client:
        """Get or initialize the Google GenAI client safely.

        Raises:
            ValueError: If GEMINI_API_KEY is missing or invalid.
        """
        if not self.is_configured():
            raise ValueError(
                "GEMINI_API_KEY is not configured. "
                "Please add your API key from Google AI Studio to backend/.env."
            )

        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)

        return self._client

    async def generate_response(
        self,
        prompt: str,
        context: Optional[str] = None,
        model: str = "gemini-3.6-flash",
    ) -> str:
        """Basic prompt generation helper prepared for future chatbot phases.

        Args:
            prompt: User question or message.
            context: Optional environmental/weather context.
            model: Gemini model name.

        Returns:
            The generated string response from Gemini.
        """
        client = self.get_client()

        full_prompt = prompt
        if context:
            full_prompt = f"Environmental Context:\n{context}\n\nUser Question:\n{prompt}"

        response = client.models.generate_content(
            model=model,
            contents=full_prompt,
        )
        return response.text or ""


# Singleton service instance
gemini_service = GeminiService()

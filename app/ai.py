import json
from typing import Any

from google import genai
from google.genai import types

from .config import get_settings


class GeminiService:

    def __init__(self):
        self.settings = get_settings()

        if self.settings.gemini_api_key:
            self.client = genai.Client(
                api_key=self.settings.gemini_api_key
            )
        else:
            self.client = None

    @property
    def enabled(self) -> bool:
        return self.client is not None

    def generate_json(
        self,
        prompt: str,
        image_bytes: bytes | None = None,
        mime_type: str | None = None,
    ) -> dict[str, Any] | None:

        if not self.client:
            return None

        contents: list[Any] = [
            prompt
        ]

        if image_bytes and mime_type:
            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                )
            )

        try:
            response = (
                self.client.models.generate_content(
                    model=self.settings.gemini_model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        temperature=0.35,
                        response_mime_type="application/json",
                    ),
                )
            )

            response_text = response.text or ""

            return json.loads(response_text)

        except Exception:
            # If Gemini is unavailable, the calling
            # recommendation service will use the
            # local deterministic fallback.
            return None


gemini_service = GeminiService()
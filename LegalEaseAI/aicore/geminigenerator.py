import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
            raise ValueError(
                "GEMINI_API_KEY is missing. Please add your Gemini API key to .env"
            )

        self.client = genai.Client(api_key=api_key)

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        effective_date,
        jurisdiction=None,
        additional_instructions=None,
    ):

        prompt = f"""
Create a professional legal document draft.

Document Type:
{document_type}

Parties:
{parties}

Effective Date:
{effective_date}

Jurisdiction:
{jurisdiction or "[NOT PROVIDED]"}

Key Terms:
{terms}

Additional Instructions:
{additional_instructions or "[NONE]"}

Requirements:
- Create a clear and professional legal document.
- Use appropriate headings and sections.
- Do not invent names, dates, addresses, amounts, or legal facts.
- If information is missing, use [NOT PROVIDED].
- Make the document easy to edit.
- This is a draft and should be reviewed by a qualified legal professional.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text
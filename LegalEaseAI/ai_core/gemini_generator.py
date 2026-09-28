import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Please add it to your .env file."
            )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

        self.client = genai.Client(
            api_key=self.api_key
        )

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
You are a professional legal document drafting assistant.

Create a clear, professional draft for the following document.

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
- Create a professional legal document.
- Use clear and simple legal language.
- Use appropriate headings and sections.
- Do not invent missing personal, legal, financial, or jurisdiction-specific facts.
- Use [NOT PROVIDED] where information is missing.
- Make the document easy to edit.
- Include a short legal review notice at the end.
"""

        # ---------------------------------------------------------
        # TRY GEMINI FIRST
        # ---------------------------------------------------------

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            if response and response.text:
                return response.text

        except Exception as e:

            error_text = str(e)

            print("\nGemini generation failed.")
            print("Reason:", error_text)

            # These errors mean Gemini is temporarily unavailable
            fallback_errors = [
                "429",
                "RESOURCE_EXHAUSTED",
                "503",
                "UNAVAILABLE",
                "quota",
                "Quota exceeded",
                "high demand",
                "rate limit",
            ]

            if any(error in error_text for error in fallback_errors):

                print("Using local LegalEase fallback template...\n")

                return self._generate_local_document(
                    document_type=document_type,
                    parties=parties,
                    terms=terms,
                    effective_date=effective_date,
                    jurisdiction=jurisdiction,
                    additional_instructions=additional_instructions,
                )

            # For other errors, also use fallback so the application
            # does not completely fail.
            print("Using local LegalEase fallback template...\n")

            return self._generate_local_document(
                document_type=document_type,
                parties=parties,
                terms=terms,
                effective_date=effective_date,
                jurisdiction=jurisdiction,
                additional_instructions=additional_instructions,
            )

        # Empty Gemini response
        return self._generate_local_document(
            document_type=document_type,
            parties=parties,
            terms=terms,
            effective_date=effective_date,
            jurisdiction=jurisdiction,
            additional_instructions=additional_instructions,
        )

    # =============================================================
    # LOCAL FALLBACK DOCUMENT GENERATOR
    # =============================================================

    def _generate_local_document(
        self,
        document_type,
        parties,
        terms,
        effective_date,
        jurisdiction=None,
        additional_instructions=None,
    ):

        document_type_clean = document_type.strip()

        # Convert semicolon-separated terms into readable clauses
        term_list = []

        if terms:
            for term in terms.split(";"):
                term = term.strip()

                if term:
                    term_list.append(term)

        if not term_list:
            term_list.append("[NOT PROVIDED]")

        terms_text = ""

        for index, term in enumerate(term_list, start=1):
            terms_text += f"{index}. {term}\n"

        document = f"""
{document_type_clean.upper()}

THIS AGREEMENT is made effective as of {effective_date}.

1. PARTIES

The parties to this agreement are:

{parties}

2. PURPOSE

This agreement sets out the terms and conditions agreed between the
parties in connection with the above-mentioned arrangement.

3. EFFECTIVE DATE

The effective date of this agreement is:

{effective_date}

4. KEY TERMS AND CONDITIONS

{terms_text}

5. RESPONSIBILITIES OF THE PARTIES

Each party agrees to perform its responsibilities in accordance with
the terms agreed under this document.

The parties shall provide accurate information and cooperate with
each other where reasonably necessary to fulfill the purpose of this
agreement.

6. CONFIDENTIALITY

Where confidential information is shared between the parties, the
parties should take reasonable steps to protect such information
from unauthorized disclosure.

7. COMPLIANCE

The parties agree to comply with applicable laws and regulations
relevant to this agreement.

8. CHANGES TO THIS AGREEMENT

Any changes to this agreement should be made in writing and agreed
to by the parties.

9. TERMINATION

This agreement may be terminated according to the terms agreed
between the parties or as permitted by applicable law.

10. GOVERNING JURISDICTION

Jurisdiction:

{jurisdiction or "[NOT PROVIDED]"}

11. ADDITIONAL INSTRUCTIONS

{additional_instructions or "[NONE]"}

12. AGREEMENT

By accepting this document, the parties acknowledge that they have
read and understood the terms stated above and agree to comply with
the applicable provisions of this agreement.

PARTY DETAILS

Party information:

{parties}

EFFECTIVE DATE:

{effective_date}


------------------------------------------------------------

LEGAL REVIEW NOTICE

This document was generated by LegalEase. It is provided for
informational and drafting purposes only and does not constitute
legal advice.

The document should be reviewed and, where appropriate, modified
by a qualified legal professional before being signed or used.
"""

        return document.strip()
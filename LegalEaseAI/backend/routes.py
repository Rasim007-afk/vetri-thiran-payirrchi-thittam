from fastapi import APIRouter, HTTPException
from backend.models import DocumentRequest
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()

generator = GeminiDocumentGenerator()


@router.post("/generate")
def generate_document(request: DocumentRequest):

    try:
        generated_text = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
            jurisdiction=request.jurisdiction,
            additional_instructions=request.additional_instructions,
        )

        return {
            "document_type": request.document_type,
            "content": generated_text,
            "disclaimer": (
                "This document is an AI-generated draft for informational "
                "purposes only. It is not legal advice. Please have it "
                "reviewed by a qualified legal professional before use."
            ),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
from services.exporters import (
    to_txt,
    to_docx,
    to_pdf
)


def test_txt_export():

    result = to_txt(
        "Hello LegalEase"
    )

    assert (
        b"Hello LegalEase"
        in result
    )


def test_docx_export():

    result = to_docx(
        "Hello LegalEase",
        "Test Document"
    )

    # DOCX files are ZIP containers
    assert result[:2] == b"PK"


def test_pdf_export():

    result = to_pdf(
        "Hello LegalEase",
        "Test Document"
    )

    assert result.startswith(
        b"%PDF"
    )
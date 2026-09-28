from io import BytesIO

from services.sanitizer import sanitize_text


# ============================================================
# TXT
# ============================================================

def to_txt(text: str) -> bytes:

    cleaned_text = sanitize_text(text)

    return cleaned_text.encode(
        "utf-8"
    )


# ============================================================
# DOCX
# ============================================================

def to_docx(
    text: str,
    title: str = "LegalEase Document"
) -> bytes:

    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, Inches

    document = Document()

    section = document.sections[0]

    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    # Normal font
    normal_style = document.styles["Normal"]

    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(11)

    # ========================================================
    # TITLE
    # ========================================================

    title_paragraph = document.add_paragraph()

    title_paragraph.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    title_run = title_paragraph.add_run(
        title
    )

    title_run.bold = True
    title_run.font.name = "Times New Roman"
    title_run.font.size = Pt(16)

    # ========================================================
    # BODY
    # ========================================================

    cleaned_text = sanitize_text(text)

    lines = cleaned_text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:

            document.add_paragraph()

            continue

        paragraph = document.add_paragraph()

        # Detect headings / numbered clauses
        if (
            line.isupper()
            and len(line) < 120
        ) or line.startswith(
            (
                "1.",
                "2.",
                "3.",
                "4.",
                "5.",
                "6.",
                "7.",
                "8.",
                "9."
            )
        ):

            run = paragraph.add_run(
                line
            )

            run.bold = True

        else:

            paragraph.add_run(
                line
            )

    # ========================================================
    # FOOTER
    # ========================================================

    footer = section.footer.paragraphs[0]

    footer.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER
    )

    footer.add_run(
        "LegalEase - AI-generated draft. "
        "Review with a qualified legal professional."
    )

    # ========================================================
    # SAVE TO MEMORY
    # ========================================================

    output = BytesIO()

    document.save(
        output
    )

    return output.getvalue()


# ============================================================
# PDF
# ============================================================

def to_pdf(
    text: str,
    title: str = "LegalEase Document"
) -> bytes:

    from fpdf import FPDF

    class LegalEasePDF(FPDF):

        def header(self):

            self.set_font(
                "Helvetica",
                "B",
                10
            )

            self.cell(
                0,
                8,
                "LegalEase",
                align="C"
            )

            self.ln(5)

        def footer(self):

            self.set_y(-15)

            self.set_font(
                "Helvetica",
                "I",
                8
            )

            self.cell(
                0,
                10,
                "AI-generated draft - "
                "professional legal review recommended.",
                align="C"
            )

    pdf = LegalEasePDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=20
    )

    pdf.add_page()

    # ========================================================
    # TITLE
    # ========================================================

    pdf.set_font(
        "Helvetica",
        "B",
        16
    )

    pdf.multi_cell(
        0,
        9,
        title,
        align="C"
    )

    pdf.ln(4)

    # ========================================================
    # BODY
    # ========================================================

    pdf.set_font(
        "Helvetica",
        "",
        11
    )

    cleaned_text = sanitize_text(
        text
    )

    # FPDF's default Helvetica font doesn't support
    # every Unicode character, so replace unsupported
    # characters safely.

    safe_text = (
        cleaned_text
        .encode(
            "latin-1",
            "replace"
        )
        .decode(
            "latin-1"
        )
    )

    for line in safe_text.splitlines():

        line = line.strip()

        if not line:

            pdf.ln(4)

            continue

        if (
            line.isupper()
            and len(line) < 120
        ):

            pdf.set_font(
                "Helvetica",
                "B",
                11
            )

        else:

            pdf.set_font(
                "Helvetica",
                "",
                11
            )

        pdf.multi_cell(
            0,
            6,
            line
        )

        pdf.ln(1)

    return bytes(
        pdf.output()
    )
import os
import html

import requests
import streamlit as st

from dotenv import load_dotenv

from services.exporters import (
    to_txt,
    to_docx,
    to_pdf
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


API_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 44px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .sub-title {
        text-align: center;
        color: #888888;
        margin-bottom: 30px;
        font-size: 18px;
    }

    .preview-box {
        background: #111827;
        color: #f3f4f6;
        padding: 25px;
        border-radius: 14px;
        min-height: 400px;
        white-space: pre-wrap;
        font-family: Georgia, serif;
        line-height: 1.7;
        overflow-x: auto;
    }

    .notice-box {
        padding: 15px;
        border-radius: 10px;
        background: #fff7ed;
        color: #7c2d12;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'AI-Powered Legal Document Generator'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "Document Details"
    )

    document_type = st.text_input(
        "Document Type",
        value="Freelance Work Contract"
    )

    parties = st.text_area(
        "Parties Involved",
        value=(
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),
        height=100
    )

    terms = st.text_area(
        "Terms & Conditions",
        value=(
            "Payment within 30 days of invoice; "
            "Confidentiality must be maintained; "
            "Provider will deliver work by the agreed deadline; "
            "Either party may terminate with 15 days notice"
        ),
        height=170
    )

    effective_date = st.text_input(
        "Effective Date",
        value="September 24, 2026"
    )

    jurisdiction = st.text_input(
        "Jurisdiction",
        value="Not specified"
    )

    additional_instructions = st.text_area(
        "Additional Instructions",
        height=100
    )

    generate_button = st.button(
        "Generate Document",
        type="primary",
        use_container_width=True
    )


# ============================================================
# SESSION STATE
# ============================================================

if "content" not in st.session_state:

    st.session_state.content = ""


# ============================================================
# GENERATE DOCUMENT
# ============================================================

if generate_button:

    payload = {

        "document_type":
            document_type,

        "parties":
            parties,

        "terms":
            terms,

        "effective_date":
            effective_date,

        "jurisdiction":
            jurisdiction,

        "additional_instructions":
            additional_instructions
    }

    try:

        with st.spinner(
            "Generating legal document..."
        ):

            response = requests.post(
                f"{API_URL}/generate",
                json=payload,
                timeout=120
            )

        if response.ok:

            data = response.json()

            st.session_state.content = (
                data["content"]
            )

            st.success(
                "Document generated successfully!"
            )

        else:

            st.error(
                f"Backend error: {response.text}"
            )

    except requests.RequestException as error:

        st.error(
            "Could not connect to the FastAPI backend."
        )

        st.code(
            str(error)
        )


# ============================================================
# PREVIEW
# ============================================================

st.subheader(
    "Document Preview"
)


if st.session_state.content:

    preview_tab, edit_tab = st.tabs(
        [
            "Preview",
            "Edit Document"
        ]
    )

    # ========================================================
    # PREVIEW TAB
    # ========================================================

    with preview_tab:

        safe_content = html.escape(
            st.session_state.content
        )

        st.markdown(
            f"""
            <div class="preview-box">
            {safe_content}
            </div>
            """,
            unsafe_allow_html=True
        )

    # ========================================================
    # EDIT TAB
    # ========================================================

    with edit_tab:

        edited_content = st.text_area(
            "Edit your document",
            value=st.session_state.content,
            height=600
        )

        if st.button(
            "Apply Changes"
        ):

            st.session_state.content = (
                edited_content
            )

            st.success(
                "Changes applied."
            )

            st.rerun()


    # ========================================================
    # DOWNLOAD SECTION
    # ========================================================

    st.subheader(
        "Download Document"
    )

    content = (
        st.session_state.content
    )

    filename = (
        "legalease_document"
    )

    col1, col2, col3 = st.columns(3)


    # ========================================================
    # TXT
    # ========================================================

    with col1:

        txt_data = to_txt(
            content
        )

        st.download_button(
            label="Download TXT",
            data=txt_data,
            file_name=f"{filename}.txt",
            mime="text/plain"
        )


    # ========================================================
    # DOCX
    # ========================================================

    with col2:

        docx_data = to_docx(
            content,
            document_type
        )

        st.download_button(
            label="Download DOCX",
            data=docx_data,
            file_name=f"{filename}.docx",
            mime=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            )
        )


    # ========================================================
    # PDF
    # ========================================================

    with col3:

        pdf_data = to_pdf(
            content,
            document_type
        )

        st.download_button(
            label="Download PDF",
            data=pdf_data,
            file_name=f"{filename}.pdf",
            mime="application/pdf"
        )


    # ========================================================
    # DISCLAIMER
    # ========================================================

    st.markdown(
        """
        <div class="notice-box">

        <b>Important:</b>

        LegalEase creates AI-assisted legal drafts
        for informational and drafting purposes.

        AI-generated content may contain mistakes,
        omissions, or jurisdiction-specific issues.

        Have a qualified legal professional review
        the document before relying on or signing it.

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.info(
        "Enter your document details in the sidebar "
        "and click Generate Document."
    )
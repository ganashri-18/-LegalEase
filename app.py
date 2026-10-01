"""
LegalEase: AI-Powered Legal Document Generator & Contract Intelligence System
Main Streamlit Application
"""
import streamlit as st
from datetime import date

from src.prompts import (
    MASTER_SYSTEM_PROMPT,
    AUDIT_PROMPT_TEMPLATE,
    SIMPLIFY_PROMPT_TEMPLATE,
    QA_PROMPT_TEMPLATE,
    build_generation_prompt
)
from src.generator import run_ai_task
from src.exporter import export_to_docx, export_to_pdf
from src.presets import PRESETS

st.set_page_config(
    page_title="LegalEase | AI Legal Document Generator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #4B5563;
            margin-bottom: 1.5rem;
        }
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
        }
        .badge {
            display: inline-block;
            padding: 0.25em 0.6em;
            font-size: 75%;
            font-weight: 700;
            line-height: 1;
            text-align: center;
            white-space: nowrap;
            vertical-align: baseline;
            border-radius: 0.375rem;
            background-color: #DBEAFE;
            color: #1E40AF;
            margin-right: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-header">⚖️ LegalEase AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Automated contract generation, multi-jurisdiction drafting, and risk auditing powered by advanced LLMs.</div>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.image(
        "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3",
        caption="LegalEase Intelligence Engine",
        use_container_width=True
    )
    st.header("⚙️ Model Configuration")

    provider = st.selectbox(
        "AI Provider",
        ["DEMO MODE (No Key Required)", "GEMINI", "OPENAI"],
        index=0,
        help="Use Demo Mode for instant offline testing, or connect your API key for live generation."
    )

    api_key = ""
    if provider != "DEMO MODE (No Key Required)":
        api_key = st.text_input(
            "API Key",
            type="password",
            help="Enter your API key here or configure it in .env"
        )

    st.markdown("---")
    st.caption(
        "🔒 LegalEase operates locally. Your drafted contract content is sent directly to your chosen LLM provider and never stored on third-party servers."
    )

tabs = st.tabs([
    "📝 Generate Document",
    "🔍 Contract Risk Auditor",
    "💡 Plain-English Explainer",
    "❓ Contract Q&A",
    "📜 Prompt Engineering Hub",
    "ℹ️ About & Disclaimers"
])

with tabs[0]:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("1. Contract Parameters")

        selected_preset = st.selectbox(
            "⚡ Quick-Fill Preset Template",
            list(PRESETS.keys()),
            index=1
        )
        preset_data = PRESETS[selected_preset]

        doc_options = [
            "Mutual Non-Disclosure Agreement (NDA)",
            "Unilateral Non-Disclosure Agreement",
            "Independent Contractor Agreement",
            "Software Development & IP Assignment Agreement",
            "Employment Agreement",
            "Commercial Lease Agreement",
            "Website Terms of Service & Privacy Policy",
            "Cease and Desist Notice"
        ]

        doc_type = st.selectbox(
            "Document Type",
            doc_options,
            index=doc_options.index(preset_data["doc_type"]) if preset_data.get("doc_type") in doc_options else 0
        )

        jurisdiction = st.text_input("Governing Jurisdiction / State Law", value=preset_data["jurisdiction"])

        p1_col, p2_col = st.columns(2)
        with p1_col:
            party1_name = st.text_input("Party 1 Legal Name", value=preset_data["party1_name"])
            party1_role = st.text_input("Party 1 Role", value=preset_data["party1_role"])
        with p2_col:
            party2_name = st.text_input("Party 2 Legal Name", value=preset_data["party2_name"])
            party2_role = st.text_input("Party 2 Role", value=preset_data["party2_role"])

        eff_col, dur_col = st.columns(2)
        with eff_col:
            effective_date = st.date_input("Effective Date", value=date.today())
        with dur_col:
            duration = st.text_input("Term / Duration", value=preset_data["duration"])

        payment_terms = st.text_input("Financial Consideration / Payment Terms", value=preset_data["payment_terms"])

        bias_options = ["Balanced & Mutual", "Favorable to Party 1", "Favorable to Party 2"]
        bias = st.selectbox(
            "Contract Posture / Bias",
            bias_options,
            index=bias_options.index(preset_data.get("bias", "Balanced & Mutual")) if preset_data.get("bias") in bias_options else 0
        )

        custom_clauses = st.text_area(
            "Special Covenants or Custom Clauses",
            value=preset_data["custom_clauses"],
            height=90,
            placeholder="e.g., Non-solicitation for 12 months, arbitration venue in Delaware..."
        )

        generate_btn = st.button("🚀 Draft Legal Document", type="primary", use_container_width=True)

    with col2:
        st.subheader("2. Document Output & Export")

        if generate_btn:
            with st.spinner("Analyzing parameters and drafting enforceable clauses..."):
                prompt = build_generation_prompt(
                    doc_type=doc_type,
                    jurisdiction=jurisdiction,
                    party1_name=party1_name,
                    party1_role=party1_role,
                    party2_name=party2_name,
                    party2_role=party2_role,
                    effective_date=str(effective_date),
                    duration=duration,
                    payment_terms=payment_terms,
                    custom_clauses=custom_clauses,
                    bias=bias
                )

                result = run_ai_task(
                    MASTER_SYSTEM_PROMPT,
                    prompt,
                    provider=provider,
                    api_key=api_key,
                    task_type="generation"
                )
                st.session_state["generated_doc"] = result
                st.session_state["last_doc_type"] = doc_type

        if "generated_doc" in st.session_state:
            doc_content = st.session_state["generated_doc"]
            word_count = len(doc_content.split())
            char_count = len(doc_content)
            st.caption(f"📊 Document Length: **{word_count} words** | **{char_count} characters**")

            edited_content = st.text_area("Live Editor (Review or adjust clauses)", value=doc_content, height=430)

            exp1, exp2, exp3 = st.columns(3)
            with exp1:
                docx_file = export_to_docx(edited_content)
                st.download_button(
                    label="📄 Download Word (.docx)",
                    data=docx_file,
                    file_name="legalease_document.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            with exp2:
                pdf_file = export_to_pdf(edited_content)
                st.download_button(
                    label="📕 Download PDF",
                    data=pdf_file,
                    file_name="legalease_document.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            with exp3:
                st.download_button(
                    label="📥 Download Markdown",
                    data=edited_content,
                    file_name="legalease_document.md",
                    mime="text/markdown",
                    use_container_width=True
                )
        else:
            st.info("👈 Select your parameters or choose a quick preset on the left, then click **Draft Legal Document**.")

with tabs[1]:
    st.subheader("🔍 Contract Risk Auditor & Redline Assistant")
    st.write("Detect liability traps, one-sided covenants, and missing boilerplate provisions.")

    sample_contract = """INDEPENDENT CONTRACTOR AGREEMENT
    Section 7 (Indemnification): Contractor shall defend, indemnify, and hold harmless Company and its affiliates from and against any and all claims, liabilities, losses, damages, and costs arising out of Contractor's performance.
    Section 8 (Intellectual Property): Company shall own all inventions, code, designs, and derivative works created by Contractor at any time during the term of this Agreement, whether created on or off Company premises.
    Section 9 (Termination): Company may terminate this Agreement immediately at any time without cause. Contractor may not terminate without 60 days advance written notice."""

    audit_col1, audit_col2 = st.columns([1, 1], gap="large")

    with audit_col1:
        load_sample = st.checkbox("Load Sample Risky Agreement", value=False)
        contract_to_audit = st.text_area(
            "Paste Contract or Clause to Audit",
            value=sample_contract if load_sample else "",
            height=300,
            placeholder="Paste contract clauses here..."
        )
        audit_btn = st.button("🔎 Run Comprehensive Risk Audit", type="primary", use_container_width=True)

    with audit_col2:
        if audit_btn:
            if not contract_to_audit.strip():
                st.warning("Please paste or load contract text to audit.")
            else:
                with st.spinner("Analyzing contract risks, indemnities, and balance of power..."):
                    audit_prompt = AUDIT_PROMPT_TEMPLATE.format(contract_text=contract_to_audit)
                    audit_result = run_ai_task(
                        MASTER_SYSTEM_PROMPT,
                        audit_prompt,
                        provider=provider,
                        api_key=api_key,
                        task_type="audit"
                    )
                    st.session_state["audit_result"] = audit_result

        if "audit_result" in st.session_state:
            st.markdown(st.session_state["audit_result"])
        else:
            st.info("Paste contract clauses and run the audit to view the structured risk analysis and redlines.")

with tabs[2]:
    st.subheader("💡 Plain-English Contract Translator")
    st.write("Demystify dense legal language into everyday bullet points (8th-grade reading level).")
    explainer_col1, explainer_col2 = st.columns([1, 1], gap="large")

    with explainer_col1:
        text_to_simplify = st.text_area(
            "Paste Legalese / Confusing Clauses",
            height=280,
            placeholder="Paste dense legal clauses here..."
        )
        simplify_btn = st.button("✨ Explain in Plain English", type="primary", use_container_width=True)

    with explainer_col2:
        if simplify_btn:
            if not text_to_simplify.strip():
                st.warning("Please provide legal text to simplify.")
            else:
                with st.spinner("Translating legalese to simple English..."):
                    simp_prompt = SIMPLIFY_PROMPT_TEMPLATE.format(contract_text=text_to_simplify)
                    simp_result = run_ai_task(
                        MASTER_SYSTEM_PROMPT,
                        simp_prompt,
                        provider=provider,
                        api_key=api_key,
                        task_type="simplify"
                    )
                    st.session_state["simplified_result"] = simp_result

        if "simplified_result" in st.session_state:
            st.markdown(st.session_state["simplified_result"])
        else:
            st.info("Paste any complex clause to receive a 30-second summary, rights, obligations, and red flags.")

with tabs[3]:
    st.subheader("❓ Interactive Contract Assistant (Q&A)")
    st.write("Ask questions directly against your drafted or uploaded contract.")

    qa_contract = st.text_area(
        "Contract Context for Q&A",
        value=st.session_state.get("generated_doc", ""),
        height=180,
        placeholder="Draft a contract in Tab 1 or paste any contract here..."
    )

    qa_question = st.text_input(
        "Ask a question about this contract",
        placeholder="e.g., Can either party terminate without cause? What is the governing law?"
    )

    qa_btn = st.button("💬 Ask Question", type="primary")

    if qa_btn:
        if not qa_contract.strip() or not qa_question.strip():
            st.warning("Please provide both the contract text and a question.")
        else:
            with st.spinner("Reviewing contract provisions..."):
                qa_prompt = QA_PROMPT_TEMPLATE.format(
                    contract_text=qa_contract,
                    user_question=qa_question
                )
                qa_res = run_ai_task(
                    MASTER_SYSTEM_PROMPT,
                    qa_prompt,
                    provider=provider,
                    api_key=api_key,
                    task_type="qa"
                )
                st.markdown("### Answer")
                st.markdown(qa_res)

with tabs[4]:
    st.subheader("📜 Prompt Engineering Suite & Architecture")
    st.write("View the exact prompts used to control LLM outputs, maintain legal structure, and avoid hallucinated clauses.")
    st.markdown("#### 1. Master System Prompt (`MASTER_SYSTEM_PROMPT`)")
    st.code(MASTER_SYSTEM_PROMPT, language="markdown")

    st.markdown("#### 2. Document Generation Prompt Builder")
    st.code(
        """
        # Dynamic Prompt Template used in build_generation_prompt():
        Draft a complete, comprehensive, and execution-ready {doc_type} based on:
        - Governing Law & Jurisdiction: {jurisdiction}
        - Party 1 ({party1_role}): {party1_name}
        - Party 2 ({party2_role}): {party2_name}
        - Effective Date: {effective_date}
        - Term / Duration: {duration}
        - Consideration / Financial Terms: {payment_terms}
        - Strategic Drafting Posture: {bias}
        - Custom Covenants: {custom_clauses}
        """,
        language="markdown"
    )

    st.markdown("#### 3. Contract Risk Audit Prompt (`AUDIT_PROMPT_TEMPLATE`)")
    st.code(AUDIT_PROMPT_TEMPLATE, language="markdown")

    st.markdown("#### 4. Plain-English Explainer Prompt (`SIMPLIFY_PROMPT_TEMPLATE`)")
    st.code(SIMPLIFY_PROMPT_TEMPLATE, language="markdown")

with tabs[5]:
    st.subheader("About LegalEase")
    st.markdown(
        """
        **LegalEase** is an open-source, AI-powered contract drafting, review, and risk mitigation platform built for founders, legal engineers, and software developers.

        ### 🛡️ Why LegalEase?
        - **Jurisdiction-Aware:** Supports California, Delaware, New York, UK, India, and custom common law jurisdictions.
        - **Bias Control:** Adjusts covenants based on whether you represent Party 1, Party 2, or require a neutral mutual agreement.
        - **Multi-Format Export:** Export directly to editable Microsoft Word (`.docx`), formatted PDF, and Markdown.
        - **Open-Source & Privacy Focused:** Run locally on your own machine without sending data to unknown aggregators.

        ### ⚠️ Legal Disclaimer
        *LegalEase is an assistive productivity tool powered by artificial intelligence. It does NOT provide formal legal advice, does NOT create an attorney-client relationship, and is NOT a substitute for qualified legal counsel. Always consult a licensed attorney in your relevant jurisdiction before signing any legal instrument.*
        """
    )
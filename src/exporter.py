"""
Document exporter utility for DOCX, PDF, and plain text formats.
"""
import io
import re
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from fpdf import FPDF

def export_to_docx(markdown_text: str) -> io.BytesIO:
    """Converts markdown text to a styled Word (.docx) document."""
    doc = Document()
    
    # Page setup (1 inch standard margins)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    lines = markdown_text.split("\n")
    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith("# "):
            h = doc.add_heading(stripped.replace("# ", "").strip(), level=1)
            h.paragraph_format.space_before = Pt(12)
            h.paragraph_format.space_after = Pt(6)
        elif stripped.startswith("## "):
            h = doc.add_heading(stripped.replace("## ", "").strip(), level=2)
            h.paragraph_format.space_before = Pt(10)
            h.paragraph_format.space_after = Pt(4)
        elif stripped.startswith("### "):
            h = doc.add_heading(stripped.replace("### ", "").strip(), level=3)
            h.paragraph_format.space_before = Pt(8)
            h.paragraph_format.space_after = Pt(2)
        elif stripped.startswith("- ") or stripped.startswith("* "):
            bullet_text = re.sub(r"^\s*[-*]\s+", "", stripped)
            cleaned_bullet = re.sub(r"\*\*(.*?)\*\*", r"\1", bullet_text)
            p = doc.add_paragraph(cleaned_bullet, style='List Bullet')
            p.paragraph_format.space_after = Pt(3)
        elif stripped.startswith("> "):
            quote_text = stripped.replace("> ", "").strip()
            cleaned_quote = re.sub(r"\*\*(.*?)\*\*", r"\1", quote_text)
            p = doc.add_paragraph(cleaned_quote)
            p.paragraph_format.left_indent = Inches(0.5)
            p.paragraph_format.space_after = Pt(4)
        elif stripped == "---":
            p = doc.add_paragraph("_" * 50)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif stripped:
            cleaned_p = re.sub(r"\*\*(.*?)\*\*", r"\1", stripped)
            p = doc.add_paragraph(cleaned_p)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15

    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return file_stream

def export_to_pdf(markdown_text: str) -> io.BytesIO:
    """Converts markdown text to a clean PDF document with safe character substitution."""
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("helvetica", size=10)

    # Safe character normalization for standard PDF fonts
    replacements = {
        "—": "-",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "•": "-",
        "…": "...",
        "§": "Sec.",
        "©": "(c)",
        "®": "(R)",
        "™": "TM",
        "⚖️": "[LegalEase]",
        "⚠️": "[Warning]",
        "🚀": "",
        "📋": "",
        "🚦": "",
        "🚨": "",
        "🔍": "",
        "✏️": "",
        "🎯": "",
        "✅": "[x]",
        "🎁": "*",
        "⏱️": ""
    }
    
    cleaned = markdown_text
    for char, rep in replacements.items():
        cleaned = cleaned.replace(char, rep)

    # Encode safely to latin-1 compatible ASCII
    cleaned = cleaned.encode("ascii", "replace").decode("latin-1")

    # Render lines with explicit effective page width
    epw = pdf.epw

    for line in cleaned.split("\n"):
        stripped = line.strip()
        if stripped.startswith("# "):
            pdf.ln(3)
            pdf.set_font("helvetica", style="B", size=15)
            clean_title = stripped.replace("# ", "").replace("*", "")
            pdf.multi_cell(epw, 7, text=clean_title)
            pdf.set_font("helvetica", size=10)
        elif stripped.startswith("## "):
            pdf.ln(2)
            pdf.set_font("helvetica", style="B", size=13)
            clean_h2 = stripped.replace("## ", "").replace("*", "")
            pdf.multi_cell(epw, 6, text=clean_h2)
            pdf.set_font("helvetica", size=10)
        elif stripped.startswith("### "):
            pdf.ln(2)
            pdf.set_font("helvetica", style="B", size=11)
            clean_h3 = stripped.replace("### ", "").replace("*", "")
            pdf.multi_cell(epw, 5.5, text=clean_h3)
            pdf.set_font("helvetica", size=10)
        elif stripped.startswith("- ") or stripped.startswith("* "):
            clean_bullet = "  * " + stripped[2:].replace("*", "")
            pdf.multi_cell(epw, 5, text=clean_bullet)
        elif stripped == "---":
            pdf.ln(1)
            pdf.multi_cell(epw, 4, text="---------------------------------------------------------------------------------")
            pdf.ln(1)
        elif stripped:
            clean_text = stripped.replace("**", "").replace("*", "")
            pdf.multi_cell(epw, 5, text=clean_text)
        else:
            pdf.ln(2)

    file_stream = io.BytesIO()
    pdf.output(file_stream)
    file_stream.seek(0)
    return file_stream

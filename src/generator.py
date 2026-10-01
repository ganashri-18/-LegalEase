"""
LLM integration layer supporting Google Gemini, OpenAI, and Mock Demo Mode.
"""
import os
from dotenv import load_dotenv

load_dotenv()

def generate_document_gemini(system_prompt: str, user_prompt: str, api_key: str) -> str:
    """Generates document using Google Gemini API."""
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    
    # Try gemini-1.5-flash as default stable model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt,
        generation_config={"temperature": 0.2, "top_p": 0.9}
    )
    response = model.generate_content(user_prompt)
    return response.text

def generate_document_openai(system_prompt: str, user_prompt: str, api_key: str) -> str:
    """Generates document using OpenAI GPT-4o-mini."""
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content

def get_demo_response(task_type: str = "generation") -> str:
    """Provides a realistic fallback mock contract for demonstration without requiring an API key."""
    if task_type == "audit":
        return """### 1. 📋 Executive Overview & Transaction Summary
- **Document Type:** Independent Contractor Agreement
- **Parties:** Apex Software Corp (Client) & Jane Doe (Contractor)
- **Core Purpose:** Delivery of full-stack software development services over 6 months at $85/hour.

### 2. 🚦 Comprehensive Risk Assessment
- **Overall Risk Rating:** 🟡 MEDIUM RISK
- **Bargaining Stance:** Moderately favorable to Client.

### 3. 🚨 Unfavorable, High-Risk, or Ambiguous Clauses
1. **Uncapped Indemnification (Section 7.2):** Contractor indemnifies Client against any third-party claims without any financial liability cap or exclusion for gross negligence by Client.
   - *Severity:* High
2. **Overbroad IP Assignment (Section 5):** Assigns all inventions created during term without carving out pre-existing open source tools or non-related side projects.
   - *Severity:* Medium

### 4. 🔍 Missing Standard Protective Provisions
- Missing mutual limitation of liability (should cap damages at fees paid in previous 6 months).
- Missing cure period (10 days) prior to termination for breach.
- Missing Force Majeure clause.

### 5. ✏️ Actionable Redline Recommendations
- **Clause 7.2 (Indemnity):**
  - *Current:* "Contractor shall indemnify and hold harmless Client against all claims, damages, and expenses."
  - *Proposed Redline:* "Contractor shall indemnify Client solely against claims arising from Contractor's willful misconduct or gross negligence, capped at the total compensation paid hereunder."
  - *Rationale:* Eliminates existential financial exposure for individual contractors.

---
> ⚠️ **DISCLAIMER:** *Audit generated for demonstration purposes.*
"""

    return """# MUTUAL NON-DISCLOSURE AGREEMENT

This Mutual Non-Disclosure Agreement ("Agreement") is made and entered into as of the Effective Date by and between:

- **Disclosing Party:** Apex Cloud Systems Inc., a Delaware corporation ("Party 1")
- **Receiving Party:** NexGen AI Labs LLC, a Delaware limited liability company ("Party 2")

(Party 1 and Party 2 are collectively referred to as the "Parties" and individually as a "Party".)

---

### RECITALS
WHEREAS, the Parties wish to explore potential business, technical, or commercial opportunities of mutual interest (the "Permitted Purpose"); and

WHEREAS, in connection with the Permitted Purpose, each Party may disclose to the other confidential, technical, financial, and proprietary information;

NOW, THEREFORE, in consideration of the mutual covenants contained herein, the Parties agree as follows:

---

### SECTION 1: CONFIDENTIAL INFORMATION
1.1 **Definition.** "Confidential Information" means all non-public information disclosed by one Party ("Disclosing Party") to the other Party ("Receiving Party"), whether orally, visually, in writing, or electronically, that is marked as proprietary or confidential, or should reasonably be understood to be confidential given the nature of the information.

1.2 **Exclusions.** Confidential Information shall not include information that:
(a) is or becomes publicly available without breach of this Agreement;
(b) was already known to Receiving Party prior to disclosure without confidentiality restrictions;
(c) is independently developed by Receiving Party without reference to Disclosing Party's information; or
(d) is rightfully obtained from a third party without restriction on disclosure.

---

### SECTION 2: OBLIGATIONS & RESTRICTIONS
2.1 **Duty of Care.** Receiving Party agrees to protect Confidential Information using the same degree of care it uses for its own confidential materials, but not less than a reasonable degree of care.
2.2 **Permitted Use.** Receiving Party shall use Confidential Information solely in furtherance of the Permitted Purpose.
2.3 **Non-Disclosure.** Receiving Party shall not disclose Confidential Information to any third party except to its directors, officers, employees, or legal/financial advisors with a need-to-know and who are bound by confidentiality obligations at least as restrictive as those herein.

---

### SECTION 3: TERM & TERMINATION
3.1 This Agreement shall remain in effect for a period of three (3) years from the Effective Date.
3.2 The obligations of confidentiality shall survive termination of this Agreement for an additional two (2) years, except for trade secrets, which shall remain protected perpetually.

---

### SECTION 4: GOVERNING LAW & DISPUTE RESOLUTION
4.1 **Governing Law.** This Agreement shall be governed by and construed in accordance with the laws of the **State of Delaware**, without regard to conflict of law principles.
4.2 **Jurisdiction.** Any legal suit or proceeding arising out of this Agreement shall be instituted exclusively in the federal or state courts located in Wilmington, Delaware.

---

### SECTION 5: INJUNCTIVE RELIEF & REMEDIES
The Parties acknowledge that any breach of this Agreement may cause irreparable harm for which monetary damages alone would be inadequate. Accordingly, the Disclosing Party shall be entitled to seek equitable relief, including injunctions, without necessity of posting bond.

---

### SECTION 6: EXECUTION & COUNTERPARTS
IN WITNESS WHEREOF, the Parties have executed this Mutual Non-Disclosure Agreement by their duly authorized representatives.

**Party 1: Apex Cloud Systems Inc.**  
By: ________________________________  
Name: `[Authorized Representative]`  
Title: `Chief Executive Officer`  
Date: `[Insert Date]`  

**Party 2: NexGen AI Labs LLC**  
By: ________________________________  
Name: `[Authorized Representative]`  
Title: `Managing Director`  
Date: `[Insert Date]`  

---
> ⚠️ **DISCLAIMER:** *This document was generated by LegalEase AI for drafting convenience and informational purposes only. It does not constitute formal legal advice and does not establish an attorney-client relationship. Prior to signing or relying on this document, consult a licensed attorney.*
"""

def run_ai_task(system_prompt: str, user_prompt: str, provider: str = "GEMINI", api_key: str = None, task_type: str = "generation") -> str:
    """Dispatches request to selected provider with automatic fallback and demo handling."""
    if provider.upper() == "DEMO MODE (NO KEY REQUIRED)":
        return get_demo_response(task_type)

    if not api_key:
        api_key = os.getenv(f"{provider.upper()}_API_KEY")

    if not api_key:
        return (
            "⚠️ **API Key Missing**: Please provide your API key in the sidebar, "
            "set it in the `.env` file, or select **'DEMO MODE (No Key Required)'** to test the app."
        )

    try:
        if provider.upper() == "GEMINI":
            return generate_document_gemini(system_prompt, user_prompt, api_key)
        elif provider.upper() == "OPENAI":
            return generate_document_openai(system_prompt, user_prompt, api_key)
        else:
            return f"Error: Unsupported provider '{provider}'."
    except Exception as e:
        return f"❌ An error occurred during AI generation: {str(e)}"

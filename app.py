import streamlit as st
from fpdf import FPDF
import base64


# --- APP CONFIGURATION ---
st.set_page_config(page_title="Educated Investor App", page_icon="🛡️")


# --- PDF GENERATOR LOGIC ---
def create_pdf(name, profile_type, logic_summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "EDUCATED INVESTOR™ | ADVISOR SPEC SHEET", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, f"Prepared for: {name}")
    pdf.multi_cell(0, 10, f"Target Advisor Profile: {profile_type}")
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "YOUR VETTING PROTOCOL QUESTIONS:", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 8, logic_summary)
    return pdf.output(dest='S').encode('latin-1')


# --- USER INTERFACE ---
st.title("🛡️ EDUCATED INVESTOR™")
st.subheader("Financial Self-Defense & Advisor Match")


# STEP 1: SPEC SHEET
st.header("Step 1: Where are you in life?")
life_stage = st.multiselect("Check all that apply:", ["Accumulation", "Pre-Retirement", "Distribution", "Business Owner", "Windfall", "Special Situation"])


# STEP 2: PRIORITIES
st.header("Step 2: Your Top Priorities")
priorities = st.multiselect("Choose up to 3:", ["Tax Reduction", "Retirement Income", "Business Exit", "Estate Planning", "Wealth Growth", "Special Needs Planning"], max_selections=3)


# STEP 3: VETTING CHECKLIST
st.header("Step 3: Internal Vetting Protocol")
st.info("Ask these questions. If they don't answer 'Yes' to the Fiduciary Oath, walk away.")
q1 = st.checkbox("Will you sign a 100% Fiduciary Oath?")
q2 = st.checkbox("Are you dually registered? (Target Answer: No)")


# STEP 4: LEAD GENERATION & EXPORT
st.header("Step 4: Get Your Confidential Spec Sheet")
with st.form("leads"):
    user_name = st.text_input("Name")
    user_email = st.text_input("Email Address")
    submit = st.form_submit_button("Generate My Report")


    if submit:
        if user_name and user_email:
            # Simple Logic for Profile
            res = "Retirement Specialist (RICP)" if "Pre-Retirement" in life_stage else "Wealth Specialist (CFP)"
            summary = "1. Must sign fiduciary oath.\n2. Must disclose all 3rd party payments.\n3. Must match life stage complexity."
            
            pdf_data = create_pdf(user_name, res, summary)
            b64 = base64.b64encode(pdf_data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Investor_Spec_Sheet.pdf">👉 Click Here to Download Your PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("Your Spec Sheet has been generated!")
        else:
            st.warning("Please enter your name and email to download the report.")
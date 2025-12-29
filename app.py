import streamlit as st
from fpdf import FPDF
import base64

# --- SET UP PAGE ---
st.set_page_config(page_title="Educated Investor App", page_icon="🛡️")

# --- PDF GENERATOR FUNCTION ---
def create_pdf(name, match_title, match_desc, credentials, vetting_questions):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "EDUCATED INVESTOR™ | ADVISOR SPEC SHEET", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, f"Confidential Report for: {name}", ln=True, align='C')
    pdf.ln(10)

    # Section: The Match
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "YOUR RECOMMENDED SPECIALIST:", ln=True)
    pdf.set_font("Arial", 'B', 11)
    pdf.multi_cell(0, 10, f"{match_title}")
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 8, f"Why: {match_desc}")
    pdf.multi_cell(0, 8, f"Look for these credentials: {credentials}")
    pdf.ln(5)

    # Section: Vetting Protocol
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "VETTING PROTOCOL - ASK THESE QUESTIONS:", ln=True)
    pdf.set_font("Arial", '', 10)
    for q in vetting_questions:
        pdf.multi_cell(0, 8, f"- {q}")
    
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.multi_cell(0, 5, "CONFIDENTIAL: Trust is not a strategy; it is a liability. Use this to find the right specialist.")
    
    return pdf.output(dest='S').encode('latin-1')

# --- APP UI ---
st.title("🛡️ EDUCATED INVESTOR™")
st.subheader("Financial Self-Defense & Advisor Match")

# --- STEP 1: FINANCIAL LIFE ---
st.header("Step 1: Where are you in life?")
life_stage = st.multiselect(
    "Check all that apply:",
    ["Accumulation", "Pre-Retirement", "Distribution", "Business Owner", "Windfall", "Special Situation"]
)

# --- STEP 2: PRIORITIES ---
st.header("Step 2: Your Top Priorities")
priorities = st.multiselect(
    "Choose up to 3:",
    ["Turning savings into income", "Not outliving money", "Reducing taxes", "Business exit/succession", "Protecting family", "Coordinating complexity", "Special needs planning", "Systematic growth"],
    max_selections=3
)

# --- STEP 3: VETTING PROTOCOL ---
st.header("Step 3: Internal Vetting Protocol")
st.info("Ask these questions. If they don't answer 'Yes' to the Fiduciary Oath, walk away.")
v1 = st.checkbox("Will you sign a 100% Fiduciary Oath?")
v2 = st.checkbox("Are you dually registered? (Target: No)")
v3 = st.checkbox("Do you accept commissions? (Target: No)")

st.divider()

# --- STEP 4: GENERATE RESULTS ---
st.header("Step 4: Get Your Report")
st.write("Enter your details to see your recommended Specialist Profile.")

with st.form("result_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    submit = st.form_submit_button("Generate My Advisor Spec Sheet")

    if submit:
        if name and email and life_stage:
            # --- LOGIC ENGINE ---
            # Default Profile
            title = "PROFILE E: Investment Management & Accumulation Specialist"
            desc = "You are focused on disciplined growth and institutional-style portfolios."
            creds = "CFA® or CIMA® (Baseline: CFP®)"
            
            # Logic overrides based on user input
            if "Pre-Retirement" in life_stage or "Distribution" in life_stage or "Turning savings into income" in priorities:
                title = "PROFILE A: Retirement Income & Distribution Specialist"
                desc = "You need a specialist focused on decumulation and making wealth last."
                creds = "RICP® or RMA® (Baseline: CFP®)"
            elif "Business Owner" in life_stage or "Business exit/succession" in priorities:
                title = "PROFILE B: Business Owner / Exit Planning Specialist"
                desc = "You need to coordinate business valuation and tax mitigation for a future sale."
                creds = "CEPA® or CExP™ (Baseline: CFP®)"
            elif "Windfall" in life_stage or "Reducing taxes" in priorities:
                title = "PROFILE C: High-Net-Worth & Tax-Focused Specialist"
                desc = "Taxes are your largest expense; you need advanced estate and asset protection."
                creds = "CPWA® or CPA/PFS (Baseline: CFP®)"
            elif "Special Situation" in life_stage or "Special needs planning" in priorities:
                title = "PROFILE D: Special Needs & Complex Family Specialist"
                desc = "You are navigating the care of a dependent or complex trust structures."
                creds = "ChSNC® or CTFA (Baseline: CFP®)"

            # Display Result on Screen
            st.success(f"Match Found: {title}")
            st.write(f"**Specialist Focus:** {desc}")
            st.write(f"**Required Credentials:** {creds}")

            # Generate PDF Download
            v_questions = [
                "Are you a fiduciary 100% of the time?",
                "Are you dually registered as a Broker-Dealer?",
                "Do you have a written Investment Policy Statement (IPS)?",
                "Will you provide total revenue disclosure in writing?"
            ]
            pdf_data = create_pdf(name, title, desc, creds, v_questions)
            b64 = base64.b64encode(pdf_data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Educated_Investor_Spec_Sheet.pdf" style="text-decoration:none;"><button style="background-color:#ff4b4b; color:white; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">📥 Download Your Full Spec Sheet PDF</button></a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.error("Please fill out your Name, Email, and at least one life stage to continue.")

import streamlit as st
from fpdf import FPDF
import base64

# --- SET UP PAGE ---
st.set_page_config(page_title="Educated Investor App", page_icon="🛡️")

# --- PDF GENERATOR ---
def create_pdf(name, match_title, match_desc, creds):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "EDUCATED INVESTOR™ | ADVISOR SPEC SHEET", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(200, 10, f"Confidential Report for: {name}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "YOUR RECOMMENDED SPECIALIST PROFILE:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 10, f"Profile: {match_title}\nCredentials to look for: {creds}\nFocus: {match_desc}")
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "THE 27-POINT VETTING PROTOCOL (SUMMARY):", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 7, "1. Verify 10+ years of experience and firm stability.\n2. Ensure 100% Fiduciary standing (No dual-registration).\n3. Demand a written Investment Policy Statement (IPS).\n4. Total transparency on fees, commissions, and third-party kickbacks.")
    
    return pdf.output(dest='S').encode('latin-1')

# --- APP UI ---
st.title("🛡️ EDUCATED INVESTOR™")
st.write("Based on the protocols of Paul Powell")

# STEPS 1 & 2 (Logic remains the same as previous)
st.header("Step 1: Financial Life Stage")
life_stage = st.multiselect("Check all that apply:", ["Accumulation", "Pre-Retirement", "Distribution", "Business Owner", "Windfall", "Special Situation"])

st.header("Step 2: Top Priorities")
priorities = st.multiselect("Choose up to 3:", ["Income Stability", "Tax Reduction", "Business Exit", "Estate Planning", "Wealth Growth"], max_selections=3)

# --- STEP 3: THE FULL 27-POINT VETTING PROTOCOL ---
st.header("Step 3: Internal Vetting Protocol")
st.write("Use these checklists during your interview. If they fail any 'Target Answer,' it is a Red Flag.")

with st.expander("PHASE I: Credentials & Stability (7 Questions)"):
    st.checkbox("1. Licensed and advising for 10+ years?")
    st.checkbox("2. With current firm for 5+ years?")
    st.checkbox("3. Has a written business continuity plan?")
    st.checkbox("4. Assets Under Management (AUM) over $75M?")
    st.checkbox("5. Services at least 50 households like mine?")
    st.checkbox("6. Practice built organically (not inherited)?")
    st.checkbox("7. Clean regulatory record (No formal complaints)?")

with st.expander("PHASE II: Competency Alignment (4 Questions)"):
    st.checkbox("8. Are you a fiduciary 100% of the time?")
    st.checkbox("9. Are you 'Dually Registered' as a Broker-Dealer? (Target: NO)")
    st.checkbox("10. Do you have a clearly defined niche specialty?")
    st.checkbox("11. Do your designations match that specialty?")

with st.expander("PHASE III: Investment Process (8 Questions)"):
    st.checkbox("12. Quantitative method for risk tolerance?")
    st.checkbox("13. Systematic process for limiting losses?")
    st.checkbox("14. Can you show me an Investment Policy Statement (IPS) now?")
    st.checkbox("15. Strategy designed to capture market returns (not beat them)?")
    st.checkbox("16. Is the strategy backed by academic evidence?")
    st.checkbox("17. Preference for low-cost Index Funds/ETFs?")
    st.checkbox("18. Do you invest your own money in these recommendations?")
    st.checkbox("19. Are we using specific benchmarks for accountability?")

with st.expander("PHASE IV: Compensation & Costs (8 Questions)"):
    st.checkbox("20. Do you refuse all third-party payments/kickbacks?")
    st.checkbox("21. Can you provide a written fee schedule now?")
    st.checkbox("22. Are you willing to charge flat fees?")
    st.checkbox("23. Do asset-based fees decline as wealth grows?")
    st.checkbox("24. Do you refuse all commissions?")
    st.checkbox("25. No bonuses based on product volume?")
    st.checkbox("26. No surrender charges or termination fees?")
    st.checkbox("27. Will you provide total revenue disclosure in writing?")

# --- STEP 4: GENERATE ---
st.divider()
st.header("Step 4: Get Your Report")
with st.form("final_report"):
    name = st.text_input("Investor Name")
    email = st.text_input("Email Address")
    if st.form_submit_button("Generate Full Spec Sheet"):
        # Match logic...
        title = "Retirement Specialist" if "Pre-Retirement" in life_stage else "Wealth Specialist"
        creds = "RICP® / RMA®" if "Pre-Retirement" in life_stage else "CFP® / CFA®"
        desc = "Focusing on your specific life stage and vetting requirements."
        
        pdf_data = create_pdf(name, title, desc, creds)
        b64 = base64.b64encode(pdf_data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="Vetting_Protocol.pdf">📥 Download Your 27-Point Vetting Guide</a>'
        st.markdown(href, unsafe_allow_html=True)

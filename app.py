import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime
import openai

st.set_page_config(page_title="HCSC PBM Strategic Command", layout="wide")

# --- SIDEBAR CONTROL ---
st.sidebar.title("🛡️ HCSC ASO Expert Control")
api_key = st.sidebar.text_input("Enter OpenAI Key", type="password")

st.sidebar.divider()
st.sidebar.subheader("View Level")
view_mode = st.sidebar.radio(
    "Select Analysis Depth:", 
    ["Detailed View", "CEO View"], 
    index=0,
    help="Detailed: UNCAPPPED Actuarial nuance and 5-year roadmaps. CEO: Top items only."
)

st.sidebar.divider()
refresh_btn = st.sidebar.button("🚀 EXECUTE FULL MARKET ANALYSIS")

if 'last_refresh' not in st.session_state:
    st.session_state['last_refresh'] = "Never"

def analyze_aso_intel(prompt_type, data, custom_instructions=""):
    if not api_key:
        st.error("Please enter OpenAI Key.")
        return None
    
    client = openai.OpenAI(api_key=api_key)
    
    # PROFESSIONAL/ACTUARIAL TONE SETTING
    if view_mode == "CEO View":
        tone_instruction = "TOP PERTINENT ITEMS ONLY. 30-second summary. Risk indicators (Green/Yellow/Red)."
    else:
        tone_instruction = """
        EXTREME ACTUARIAL DETAIL. You are a Senior Fiduciary Consultant. 
        - Use industry jargon: 'Spread Pricing Erosion', 'Rebate Attestation', 'ERISA Section 402', 'Stop-Loss Attachment Points'.
        - Cite specific Bill Numbers and their exact impact on ASO Audit Rights.
        - Analyze the 1, 3, and 5-year roadmap with quantified risk assessments.
        - Provide 'Sell-Against' scripts for Rightway, ESI, and CVS.
        - UNCAP YOUR LENGTH. Give deep, nuanced strategy.
        """

    system_prompt = f"""You are a Lead Strategic Consultant and Senior PBM Actuary for HCSC/Prime Therapeutics. 
    You manage 150,000 lives for National/Enterprise ASO groups.
    
    YOUR MARQUEE CLIENT: Waste Connections (The Woodlands, TX). 
    - Workforce: 20k+ lives, safety-sensitive industrial labor, heavy CDL driver population.
    - Focus: Fiduciary defense (J&J precedent), Stop-loss volatility, and Texas-specific audit rights.
    
    {tone_instruction}
    
    FILTERS:
    1. ASO FOCUS ONLY: Ignore Medicare/Individual.
    2. COMPETITORS: Surgical analysis of CVS/Caremark, ESI, OptumRx, Rightway, Capital Rx, SmithRx.
    3. THE PRIME PIVOT: Medical+Rx Integration as a Legal and Safety Shield.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=4000, 
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": f"{prompt_type}: {data}"}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- HEADER ---
st.title(f"🛡️ PBM Strategic Command [{view_mode}]")
st.write(f"**Target Market:** Commercial ASO | **Marquee Account:** Waste Connections (TX)")

# --- MASTER EXECUTION LOGIC ---
if refresh_btn:
    st.session_state['last_refresh'] = datetime.now().strftime("%A, %b %d at %I:%M %p")
    
    with st.status("🚀 Executing Deep-Dive Actuarial Analysis...", expanded=True) as status:
        
        # 1. THE 6-POINT PROFESSIONAL PREP
        st.subheader("📞 6-Point Professional Strategic Prep")
        col_gen, col_waste = st.columns(2)
        
        with col_gen:
            st.markdown("### 🌐 General Market/Regulatory (Detailed)")
            gen_sheet = analyze_aso_intel("GENERAL CALL TOPICS", "Provide 3 technical talking points for a general ASO client call. Focus on PBM Reform, ERISA Fiduciary liability, and Rebate Gapping.")
            st.info(gen_sheet)
            
        with col_waste:
            st.markdown("### 🚛 Waste Connections Specific (The Woodlands, TX)")
            waste_sheet = analyze_aso_intel("WASTE CONNECTIONS TOPICS", "Provide 3 high-nuance talking points for Waste Connections. Focus on: 1. TX SB 1137 audit rights. 2. CDL driver safety integration. 3. Stop-loss volatility from GLP-1 spend.")
            st.success(waste_sheet)
        
        tab_gov, tab_comp, tab_glp, tab_rumor, tab_lab = st.tabs([
            "🏛️ Gov & Regulatory (TX/Fed)", 
            "📈 Competitor Strategy", 
            "💉 GLP-1 War Room",
            "🗞️ Breaking News & Rumors",
            "🕵️ Intelligence Lab"
        ])

        with tab_gov:
            st.header("Surgical Legislative Analysis")
            
            # --- FEDERAL SECTION ---
            st.subheader("🇺🇸 Federal Impact Dropdowns")
            f_feeds = feedparser.parse("https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bterm%5D=PBM")
            for entry in f_feeds.entries[:4]:
                with st.expander(f"FED: {entry.title}"):
                    st.markdown(analyze_aso_intel("FEDERAL DEEP DIVE", f"{entry.title}: {entry.summary}"))
            
            st.divider()
            
            # --- TEXAS SECTION (SURGICAL DROPDOWNS) ---
            st.subheader("🇨🇱 Texas State Law Dropdowns (Focus: SB 1137 / HB 1763)")
            st.caption("AI-Powered Legislative Scan for Texas-specific PBM Mandates.")
            # We explicitly define the top TX bills to ensure the AI generates expanders for each
            tx_bills = ["TX SB 1137 (Transparency & Audit Rights)", "TX HB 1763 (PBM Network/Contracting Rules)", "TX SB 1136 (Drug Pricing Transparency)", "TX HB 1914 (Stop-Loss/ASO Provisions)"]
            for bill in tx_bills:
                with st.expander(f"TEXAS: {bill}"):
                    st.markdown(analyze_aso_intel("TX STATE ANALYSIS", f"Execute an exhaustive analysis of {bill}. How does this specifically empower a Texas-based ASO group like Waste Connections to dismantle traditional black-box contracts? Provide 1, 3, and 5 year outlook."))

        with tab_comp:
            st.header("Competitor Tactical Playbook")
            m_feeds = feedparser.parse("https://www.drugchannels.net/feeds/posts/default")
            for entry in m_feeds.entries[:6]:
                with st.expander(f"COMPETITOR MOVE: {entry.title}"):
                    st.markdown(analyze_aso_intel("COMPETITOR STRATEGY", f"{entry.title}: {entry.summary}"))

        with tab_glp:
            st.header("💉 GLP-1 Actuarial War Room")
            st.markdown(analyze_aso_intel("GLP-1 STRATEGIC NUANCE", "Analyze LillyDirect, BMI hurdles, Coupon Gapping, and why Integrated Health Management (Medical+Rx) is the ONLY way to manage GLP-1 stop-loss risk for Waste Connections."))

        with tab_rumor:
            st.header("🗞️ Breaking News & Market Whispers")
            st.markdown(analyze_aso_intel("MARKET RUMOR MILL", "Analyze M&A whispers, Rightway's win/loss ratio in Texas, and CVS Cordavis margin tactics."))

        status.update(label="✅ Strategic Analysis Complete!", state="complete", expanded=False)

else:
    st.info("👈 Click 'EXECUTE FULL MARKET ANALYSIS' to see the 6-Point Prep and Intelligence Data.")

with tab_lab:
    st.header("🕵️ Advanced Intelligence Lab")
    rumor_in = st.text_area("Custom Actuarial/Research Query:", height=150, placeholder="e.g. Compare the 3-year PMPM impact of Rightway's shared savings model vs Prime's pass-through for Waste Connections.")
    if st.button("Execute Lab Research"):
        with st.spinner("Processing Professional Analysis..."):
            st.markdown(analyze_aso_intel("ADVANCED RESEARCH", rumor_in))

st.divider()
st.caption(f"Last Refreshed: {st.session_state['last_refresh']} | Confidential Internal Tool | Waste Connections Fiduciary Focus")

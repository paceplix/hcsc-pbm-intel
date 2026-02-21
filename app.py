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
    help="Detailed: UNCAPPPED Actuarial nuance. CEO: Top items only."
)

st.sidebar.divider()
refresh_btn = st.sidebar.button("🚀 EXECUTE FULL MARKET ANALYSIS")

if 'last_refresh' not in st.session_state:
    st.session_state['last_refresh'] = "Never"

# Function to handle AI Analysis
def analyze_aso_intel(prompt_type, data, custom_instructions=""):
    if not api_key:
        return "⚠️ Please enter OpenAI Key."
    
    client = openai.OpenAI(api_key=api_key)
    
    # BASE TONE SETTINGS
    if view_mode == "CEO View":
        tone_instruction = "TOP PERTINENT ITEMS ONLY. 30-second summary. Risk indicators (Green/Yellow/Red)."
    else:
        tone_instruction = "EXTREME ACTUARIAL DETAIL. Senior Fiduciary Consultant tone. Use technical jargon (Spread Pricing, ERISA 402, PMPM Trend)."

    # SPECIFIC "LEARN MORE" OVERRIDE
    if prompt_type == "TECHNICAL_DEEP_DIVE":
        tone_instruction = """
        ACTUARIAL WHITE PAPER LEVEL. Provide an exhaustive, technical bulleted list of:
        1. Specific subsections of the bill/rule.
        2. Immediate vs. Delayed compliance deadlines.
        3. Specific contractual language changes required for ASO agreements.
        4. Fiduciary liability checklist for Waste Connections' leadership.
        5. Deep-dive impact on PMPM trend lines over 5 years.
        DO NOT BE BRIEF. Use 10-15 detailed bullets.
        """

    system_prompt = f"""You are a Lead Strategic Consultant and Senior PBM Actuary for HCSC/Prime Therapeutics. 
    You manage 150,000 lives for National/Enterprise ASO groups.
    Marquee Client: Waste Connections (The Woodlands, TX).
    
    {tone_instruction}
    
    FILTERS:
    1. ASO FOCUS ONLY.
    2. COMPETITORS: CVS/Caremark, ESI, OptumRx, Rightway, Capital Rx, SmithRx.
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
            st.markdown("### 🌐 General Market/Regulatory")
            st.info(analyze_aso_intel("GENERAL CALL TOPICS", "Provide 3 technical talking points on PBM Reform and ERISA Fiduciary liability."))
        with col_waste:
            st.markdown("### 🚛 Waste Connections Specific")
            st.success(analyze_aso_intel("WASTE CONNECTIONS TOPICS", "Provide 3 high-nuance talking points for Waste Connections focused on TX audit rights and CDL driver safety."))
        
        tab_gov, tab_comp, tab_glp, tab_rumor, tab_lab = st.tabs([
            "🏛️ Gov & Regulatory (TX/Fed)", "📈 Competitor Strategy", "💉 GLP-1 War Room", "🗞️ Breaking News & Rumors", "🕵️ Intelligence Lab"
        ])

        with tab_gov:
            st.header("Surgical Legislative Analysis")
            
            # FEDERAL
            st.subheader("🇺🇸 Federal Impact")
            f_feeds = feedparser.parse("https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bterm%5D=PBM")
            for i, entry in enumerate(f_feeds.entries[:4]):
                with st.expander(f"FED: {entry.title}"):
                    st.markdown(analyze_aso_intel("FEDERAL DEEP DIVE", f"{entry.title}: {entry.summary}"))
                    if st.button(f"🔍 Learn More: Technical Deep Dive", key=f"fed_{i}"):
                        st.markdown("---")
                        st.markdown(analyze_aso_intel("TECHNICAL_DEEP_DIVE", f"BILL: {entry.title}\nCONTEXT: {entry.summary}"))
            
            st.divider()
            
            # TEXAS
            st.subheader("🇨🇱 Texas State Law (Focus: SB 1137 / HB 1763)")
            tx_bills = ["TX SB 1137 (Transparency & Audit Rights)", "TX HB 1763 (PBM Network/Contracting Rules)", "TX SB 1136 (Drug Pricing Transparency)"]
            for j, bill in enumerate(tx_bills):
                with st.expander(f"TEXAS: {bill}"):
                    st.markdown(analyze_aso_intel("TX STATE ANALYSIS", f"Execute an analysis of {bill} for Waste Connections."))
                    if st.button(f"🔍 Learn More: Technical Deep Dive", key=f"tx_{j}"):
                        st.markdown("---")
                        st.markdown(analyze_aso_intel("TECHNICAL_DEEP_DIVE", f"BILL: {bill}"))

        with tab_comp:
            st.header("Competitor Tactical Playbook")
            m_feeds = feedparser.parse("https://www.drugchannels.net/feeds/posts/default")
            for k, entry in enumerate(m_feeds.entries[:6]):
                with st.expander(f"MOVE: {entry.title}"):
                    st.markdown(analyze_aso_intel("COMPETITOR STRATEGY", f"{entry.title}: {entry.summary}"))
                    if st.button(f"🔍 Learn More: Market Deep Dive", key=f"comp_{k}"):
                        st.markdown("---")
                        st.markdown(analyze_aso_intel("TECHNICAL_DEEP_DIVE", f"COMPETITOR MOVE: {entry.title}\nCONTEXT: {entry.summary}"))

        with tab_glp:
            st.header("💉 GLP-1 Actuarial War Room")
            st.markdown(analyze_aso_intel("GLP-1 STRATEGIC NUANCE", "Deep dive into LillyDirect, BMI hurdles, and Stop-loss risk."))

        with tab_rumor:
            st.header("🗞️ Breaking News & Market Whispers")
            st.markdown(analyze_aso_intel("MARKET RUMOR MILL", "Analyze M&A whispers and Rightway's win/loss ratio in Texas."))

        status.update(label="✅ Strategic Analysis Complete!", state="complete", expanded=False)

else:
    st.info("👈 Click 'EXECUTE FULL MARKET ANALYSIS' to see data.")

with tab_lab:
    st.header("🕵️ Advanced Intelligence Lab")
    rumor_in = st.text_area("Custom Actuarial/Research Query:", height=150)
    if st.button("Execute Lab Research"):
        with st.spinner("Processing Professional Analysis..."):
            st.markdown(analyze_aso_intel("ADVANCED RESEARCH", rumor_in))

st.divider()
st.caption(f"Confidential Internal Tool | Waste Connections Fiduciary Focus")

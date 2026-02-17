import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime
import openai

st.set_page_config(page_title="HCSC PBM Strategic Command", layout="wide")

# Sidebar
st.sidebar.title("🛡️ HCSC ASO Expert Control")
st.sidebar.info("HIGH-PROBABILITY FOCUS: Only surfacing regs with 1-2 year implementation viability.")
api_key = st.sidebar.text_input("Enter OpenAI Key", type="password")
refresh_btn = st.sidebar.button("🚀 EXECUTE COMMERCIAL ANALYSIS")

if 'last_refresh' not in st.session_state:
    st.session_state['last_refresh'] = "Never"

def analyze_aso_intel(prompt_type, data):
    if not api_key:
        st.error("Please enter OpenAI Key.")
        return None
    
    client = openai.OpenAI(api_key=api_key)
    
    system_prompt = """You are a Senior PBM Actuary and Lead Strategic Consultant for HCSC/Prime Therapeutics. 
    You manage 150,000 lives for National/Enterprise ASO employer groups.
    
    YOUR RIGOROUS FILTERS:
    1. FEDERAL VS STATE: Clearly distinguish between Federal laws and State-level (specifically Texas) mandates.
    2. 1-2 YEAR VIABILITY: Ignore 'long-shot' bills or political theater. Focus ONLY on legislation/rules with a high probability of material impact in the next 24 months.
    3. ASO MATERIALITY: Focus on PMPM shifts, Stop-loss impact, and ERISA Fiduciary liability (specifically the J&J/Lewandowski case implications).
    4. THE PRIME PIVOT: 
       - Against 'Big 3': Contrast their margin-shifting (Cordavis/Rebate harvesting) with Prime's Lowest-Net-Cost alignment.
       - Against 'Niches' (Rightway/CapRx): Contrast their 'app-navigation' with HCSC's 'Integrated Health Management' (Total Medical + Rx visibility).
    5. TEMPORAL ROADMAP: Always provide a 1-year (immediate) and 3-year (structural) outlook.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": f"{prompt_type}: {data}"}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- HEADER ---
st.title("🛡️ PBM Strategic Command: ASO Expert Mode")
st.write(f"**Target Market:** Commercial ASO (National/Enterprise) | **Last Analysis:** {st.session_state['last_refresh']}")

# --- TABBED INTERFACE ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏛️ Gov: Federal vs. State", 
    "📈 Competitor Tactics", 
    "💉 GLP-1 Strategic Command",
    "🕵️ Rumor & Nuance Lab",
    "🔍 Strategic Search Query"
])

with tab1:
    st.header("High-Probability Regulatory Watch")
    st.caption("Focus: 1-2 Year Implementation Window. Categorized by Federal vs. State Mandates.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🇺🇸 Federal Updates")
        f_feeds = ["https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bterm%5D=PBM"]
        if refresh_btn:
            st.session_state['last_refresh'] = datetime.now().strftime("%A, %b %d at %I:%M %p")
            for url in f_feeds:
                f = feedparser.parse(url)
                for entry in f.entries[:5]:
                    with st.expander(f"FED IMPACT: {entry.title}"):
                        st.markdown(analyze_aso_intel("FEDERAL REGULATORY DEEP-DIVE", f"Title: {entry.title}\nSummary: {entry.summary}"))
        else: st.info("Run analysis to see Federal updates.")

    with col2:
        st.subheader("🇨🇱 State Updates (Focus: Texas)")
        st.caption("Analyzing TX SB 1137, white-bagging bans, and network transparency.")
        if refresh_btn:
            # Note: Specific state RSS are rare, so we use the AI to pull/verify recent TX-specific knowledge
            st.markdown(analyze_aso_intel("TEXAS STATE MANDATE ANALYSIS", "Analyze current high-probability TX PBM legislation (e.g. SB 1137, HB 1763) and network transparency rules affecting ASO groups in the next 18 months."))
        else: st.info("Run analysis to see State updates.")

with tab2:
    st.header("Big 3 vs. Niche Tactics")
    st.caption("Analysis of ESI/CVS margin shifting vs Rightway tech pitches.")
    m_feeds = ["https://www.drugchannels.net/feeds/posts/default"]
    if refresh_btn:
        for url in m_feeds:
            f = feedparser.parse(url)
            for entry in f.entries[:5]:
                with st.expander(f"📈 COMPETITOR MOVE: {entry.title}"):
                    st.markdown(analyze_aso_intel("MARKET DYNAMICS", f"Title: {entry.title}\nSummary: {entry.summary}"))

with tab3:
    st.header("💉 GLP-1 Strategic Command")
    st.write("Specialized ASO analysis of the weight-loss spend crisis.")
    glp_query = st.selectbox("Select GLP-1 Strategy to Analyze:", [
        "Impact of LillyDirect/DTC models on ASO Clinical Oversight",
        "Implementing custom BMI thresholds & 6-month clinical wait-periods",
        "Custom Copay Tiers vs. Manufacturer Coupon 'Gapping' Strategies",
        "Stop-Loss Attachment Point Volatility due to GLP-1 Spend",
        "Selling Prime Integrated Management vs. Rightway Navigation for GLP-1s"
    ])
    if st.button("Execute GLP-1 Analysis"):
        with st.spinner("Analyzing Clinical/Financial viability..."):
            st.markdown(analyze_aso_intel("GLP-1 STRATEGY DEEP-DIVE", glp_query))

with tab4:
    st.header("🕵️ Rumor & Nuance Lab")
    rumor_in = st.text_area("Detail the market rumor/competitor quote:", placeholder="e.g. 'Rightway is pitching a shared-savings GLP-1 model in TX'...", height=150)
    if st.button("Analyze Nuance"):
        with st.spinner("Calculating 1, 3, and 5-year ASO impact..."):
            st.markdown(analyze_aso_intel("ASO RUMOR ANALYSIS", rumor_in))

with tab5:
    st.header("🔍 Strategic Search Query")
    search_query = st.text_input("Ask a specific question (e.g. How does the J&J lawsuit impact my ASO clients?):")
    if st.button("Search & Analyze"):
        with st.spinner("Executing Research..."):
            st.markdown(analyze_aso_intel("ASO RESEARCH QUERY", search_query))

# --- FOOTER ---
st.divider()
st.caption("HCSC/Prime Therapeutics Internal Strategic Analysis Tool. ASO Market Focus (National/Enterprise).")

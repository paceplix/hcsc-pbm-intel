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
st.sidebar.subheader("Global View Mode")
# This toggle now impacts every single analysis in the app
view_mode = st.sidebar.radio(
    "Select Analysis Depth:", 
    ["CEO View", "Detailed View"], 
    help="CEO View: 30-sec bullets & risk levels. Detailed View: Actuarial math, bill numbers, and 5-year roadmaps."
)

st.sidebar.divider()
refresh_btn = st.sidebar.button("🚀 EXECUTE FULL MARKET ANALYSIS")

if 'last_refresh' not in st.session_state:
    st.session_state['last_refresh'] = "Never"

def analyze_aso_intel(prompt_type, data):
    if not api_key:
        st.error("Please enter OpenAI Key.")
        return None
    
    client = openai.OpenAI(api_key=api_key)
    
    # TONAL SETTINGS BASED ON GLOBAL TOGGLE
    if view_mode == "CEO View":
        tone_instruction = "Provide a 30-second Executive Summary. Use Green/Yellow/Red risk indicators. Focus ONLY on the bottom-line financial impact to the ASO group. Use short, punchy bullets."
    else:
        tone_instruction = "Provide a deep-dive actuarial and strategic analysis. Include specific bill numbers, contract nuances, and 1, 3, and 5-year financial impact modeling. Be technical and detailed."

    system_prompt = f"""You are a Senior PBM Actuary and Lead Strategic Consultant for HCSC/Prime Therapeutics. 
    You manage 150,000 lives for National/Enterprise ASO employer groups.
    
    CURRENT VIEW MODE: {view_mode}
    TONE REQUIREMENT: {tone_instruction}
    
    YOUR RIGOROUS FILTERS:
    1. ASO FOCUS ONLY: Ignore Medicare/Medicaid unless material to Commercial ASO cost-shifting.
    2. COMPETITOR SPECIFICITY: You MUST explicitly name-check: CVS/Caremark, ESI (Express Scripts/Cigna), OptumRx, Rightway, Capital Rx, SmithRx, and Navitus.
    3. 1-2 YEAR VIABILITY: Focus on high-probability impact (e.g., TX SB 1137).
    4. THE PRIME PIVOT: Contrast HCSC/Prime's Integrated Health Management (Total Medical + Rx visibility) against competitor 'Margin Shifting' or tech-only 'Navigation' (Rightway).
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
st.title(f"🛡️ PBM Strategic Command [{view_mode}]")
st.write(f"**Target Market:** Commercial ASO (National/Enterprise) | **Last Analysis Run:** {st.session_state['last_refresh']}")

# --- TABS ---
tab_brief, tab_gov, tab_comp, tab_glp, tab_lab = st.tabs([
    "📊 Executive Briefing",
    "🏛️ Gov: Fed vs. State", 
    "📈 Competitor Tactics", 
    "💉 GLP-1 Strategic Command",
    "🕵️ Rumor & Search Lab"
])

with tab_brief:
    st.header(f"Executive Strategic Summary ({view_mode})")
    if refresh_btn:
        st.session_state['last_refresh'] = datetime.now().strftime("%A, %b %d at %I:%M %p")
        with st.spinner("Synthesizing market data..."):
            summary_prompt = "Summarize the most material PBM market changes, legislative updates (TX & Fed), and competitor moves for a Jumbo ASO client."
            st.markdown(analyze_aso_intel("EXECUTIVE SUMMARY", summary_prompt))
    else:
        st.info("Click 'EXECUTE FULL MARKET ANALYSIS' in the sidebar to generate.")

with tab_gov:
    st.header("High-Probability Regulatory Watch")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🇺🇸 Federal Updates")
        f_feeds = feedparser.parse("https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bterm%5D=PBM")
        for entry in f_feeds.entries[:3]:
            with st.expander(f"FED: {entry.title}"):
                if refresh_btn: st.markdown(analyze_aso_intel("FEDERAL REGULATORY", entry.summary))
    with col2:
        st.subheader("🇨🇱 State Updates (Texas Focus)")
        if refresh_btn:
            st.markdown(analyze_aso_intel("TEXAS STATE MANDATE", "Deep analysis of TX SB 1137, HB 1763, and TDI transparency rules impacting ASO audit/network rights."))

with tab_comp:
    st.header("Competitor Dynamics & Tactics")
    st.caption("CVS/Caremark, ESI, OptumRx, Rightway, Capital Rx, SmithRx.")
    m_feeds = feedparser.parse("https://www.drugchannels.net/feeds/posts/default")
    for entry in m_feeds.entries[:5]:
        with st.expander(f"MOVE: {entry.title}"):
            if refresh_btn: st.markdown(analyze_aso_intel("COMPETITOR TACTICS", f"{entry.title}: {entry.summary}"))

with tab_glp:
    st.header("💉 GLP-1 Strategic Command")
    glp_col1, glp_col2 = st.columns([1, 2])
    with glp_col1:
        st.subheader("Select Focus")
        glp_topic = st.radio("Strategy Topic:", [
            "LillyDirect & DTC impact on ASO Clinical Oversight",
            "Custom BMI & Clinical Wait-Periods (Fiduciary Impact)",
            "Manufacturer Coupon Gapping vs. Plan Design",
            "Stop-Loss Attachment Point Volatility (1-5 Year Outlook)",
            "Prime Integration vs. Rightway Navigation for GLP-1s"
        ])
        analyze_glp = st.button("Generate GLP-1 Strategy")
    with glp_col2:
        if analyze_glp:
            with st.spinner("Analyzing..."):
                st.markdown(analyze_aso_intel("GLP-1 STRATEGY", glp_topic))

with tab_lab:
    st.header("🕵️ Strategic Intelligence Lab")
    rumor_in = st.text_area("Market Rumor or Search Question:", placeholder="e.g. 'Hearing Rightway is pitching a Texas Jumbo account with a $0 spread and shared savings on GLP-1s'...")
    if st.button("Execute Lab Research"):
        with st.spinner("Analyzing..."):
            st.markdown(analyze_aso_intel("STRATEGIC LAB QUERY", rumor_in))

# --- FOOTER ---
st.divider()
st.caption(f"HCSC/Prime Therapeutics Internal Strategic Analysis. Current View: {view_mode}")

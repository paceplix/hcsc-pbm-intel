import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime
import openai

# 1. PAGE SETUP (Crucial for a clean load)
st.set_page_config(page_title="HCSC Strategic Command", layout="wide")

# 2. SIDEBAR (Your Control Center)
st.sidebar.title("🛡️ Strategic Command")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

st.sidebar.divider()
view_mode = st.sidebar.select_slider(
    "Analysis Depth",
    options=["CEO View", "Detailed View"],
    value="Detailed View"
)

st.sidebar.divider()
refresh_btn = st.sidebar.button("🚀 GENERATE STRATEGIC BRIEFING")

# 3. THE "BRAIN" (All your talking points and audience logic live here)
def analyze_aso_intel(prompt_type, data):
    if not api_key:
        return "⚠️ API Key Required in Sidebar."
    
    client = openai.OpenAI(api_key=api_key)
    
    # This is the exact prompt we developed—no detail lost.
    system_prompt = f"""
    You are a Tier-1 Health & Welfare Consultant (ex-Mercer/Aon) and a Senior PBM Actuary for HCSC. 
    Audience: CFOs, HR Directors, and Professional PBM Consultants.
    
    REQUIRED OUTPUT STRUCTURE:
    1. STATUS: Mark as [🟢 FACT] or [🟡 SPECULATION].
    2. IMPACT: Rank as HIGH, MEDIUM, or LOW for 150k-life ASO groups.
    3. 🗣️ CONSULTANT SCRIPT (Technical): Talking points on Fiduciary risk, stop-loss attachment, and rebate gapping.
    4. 💼 CFO SCRIPT (Layman): Talking points on PMPM impact, budget predictability, and liability.
    5. THE PRIME PIVOT: Why HCSC Integrated Med+Rx beats standalone competitors (Rightway/CVS/ESI).
    
    MARQUEE CLIENT: Waste Connections (The Woodlands, TX). Industrial/CDL workforce. Safety = Fiduciary risk.
    VIEW MODE: {view_mode}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=3000, 
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": f"{prompt_type}: {data}"}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

# 4. MAIN INTERFACE (The Dashboard)
st.title("🛡️ PBM Strategic Command Center")
st.markdown("---")
st.markdown(f"**Target Market:** National/Enterprise Commercial ASO | **Marquee Account:** Waste Connections")

if refresh_btn:
    st.session_state['last_refresh'] = datetime.now().strftime("%I:%M %p")
    
    # We use a spinner instead of the complex status bar to prevent white screens
    with st.spinner("🔍 Analyzing Market Dynamics..."):
        
        # --- 6-POINT CHEAT SHEET ---
        st.subheader("📞 Strategic Call Prep (6-Point Breakdown)")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.info(analyze_aso_intel("CALL TOPICS", "Provide 3 high-impact talking points for a general PBM Consultant audience."))
        with col_c2:
            st.success(analyze_aso_intel("WASTE CONNECTIONS", "Provide 3 industrial-focused talking points for Waste Connections regarding CDL safety and TX SB 1137."))

        # --- THE TABS (All sections you requested are here) ---
        tab_gov, tab_comp, tab_glp, tab_news, tab_lab = st.tabs([
            "🏛️ Gov & Regulatory", "📈 Competitor Tactics", "💉 GLP-1 War Room", "🗞️ Speculation & Rumors", "🕵️ Research Lab"
        ])

        with tab_gov:
            st.subheader("🏛️ Legislative Impact (1-2 Year Viability)")
            col_fed, col_state = st.columns(2)
            with col_fed:
                st.markdown("#### 🇺🇸 Federal Impact")
                f_feeds = feedparser.parse("https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bterm%5D=PBM")
                for i, entry in enumerate(f_feeds.entries[:3]):
                    with st.expander(f"FED: {entry.title}"):
                        st.markdown(analyze_aso_intel("FEDERAL ANALYSIS", f"{entry.title}: {entry.summary}"))
            
            with col_state:
                st.markdown("#### 🇨🇱 Texas State Impact")
                tx_bills = ["TX SB 1137 (Transparency)", "TX HB 1763 (Network Rules)"]
                for j, bill in enumerate(tx_bills):
                    with st.expander(f"TX: {bill}"):
                        st.markdown(analyze_aso_intel("TEXAS ANALYSIS", bill))

        with tab_comp:
            st.subheader("📈 Competitor Strategic Playbook")
            m_feeds = feedparser.parse("https://www.drugchannels.net/feeds/posts/default")
            for k, entry in enumerate(m_feeds.entries[:5]):
                with st.expander(f"MOVE: {entry.title}"):
                    st.markdown(analyze_aso_intel("COMPETITOR ANALYSIS", f"{entry.title}: {entry.summary}"))

        with tab_glp:
            st.subheader("💉 GLP-1 Commercial Strategy")
            # We specifically trigger a deeper query here for GLP-1
            st.markdown(analyze_aso_intel("GLP1 STRATEGY", "Analyze LillyDirect, Stop-loss Attachment Points, and BMI Custom Tiers for an Industrial workforce like Waste Connections."))

        with tab_news:
            st.subheader("🗞️ Market Whispers & Speculation")
            st.markdown(analyze_aso_intel("RUMORS", "Synthesize rumors on Rightway win/loss momentum and CVS Cordavis margin shifting."))

        st.success(f"✅ Analysis Complete! Last Run: {st.session_state['last_refresh']}")

else:
    # This keeps the app from being a white screen when you first open it
    st.info("👈 Enter your API Key and click 'GENERATE STRATEGIC BRIEFING' to begin.")

with tab_lab:
    st.header("🕵️ Research Lab")
    query = st.text_area("Custom Actuarial/Research Query:", placeholder="e.g. Compare the PMPM impact of Rightway vs Prime for a CDL-heavy workforce.")
    if st.button("Execute Lab Search"):
        with st.spinner("Processing Professional Analysis..."):
            st.markdown(analyze_aso_intel("CUSTOM LAB", query))

st.divider()
st.caption("Confidential Internal Strategic Tool | HCSC/Prime Therapeutics")

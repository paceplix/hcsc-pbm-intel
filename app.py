import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime
import openai

# --- UI CONFIGURATION ---
st.set_page_config(page_title="HCSC Strategic Command", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for a professional "Consultant Dashboard" look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    .stExpander { border-radius: 10px !important; border: 1px solid #e0e0e0 !important; background-color: white !important; }
    .stButton>button { border-radius: 8px; height: 3em; width: 100%; background-color: #004a99; color: white; font-weight: bold; }
    .status-tag { padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .fact-tag { background-color: #d4edda; color: #155724; }
    .spec-tag { background-color: #fff3cd; color: #856404; }
    .impact-high { color: #dc3545; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR CONTROL ---
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

# --- AI ANALYSIS ENGINE ---
def analyze_aso_intel(prompt_type, data):
    if not api_key:
        return "⚠️ API Key Required in Sidebar."
    
    client = openai.OpenAI(api_key=api_key)
    
    # MASTER PROMPT: THE "CONSULTANT" PERSONA
    system_prompt = f"""
    You are a Tier-1 Health & Welfare Consultant (ex-Mercer/Aon) and a Senior PBM Actuary for HCSC. 
    Audience: CFOs, HR Directors, and Professional PBM Consultants.
    
    REQUIRED OUTPUT STRUCTURE:
    1. STATUS: Mark as [🟢 FACT] or [🟡 SPECULATION].
    2. IMPACT: Rank as HIGH, MEDIUM, or LOW for 150k-life ASO groups.
    3. 🗣️ CONSULTANT SCRIPT: Technical talking points (Fiduciary risk, stop-loss, rebate gapping).
    4. 💼 CFO SCRIPT: Financial/Layman talking points (PMPM impact, budget, liability).
    5. THE PRIME PIVOT: Why HCSC Integrated Med+Rx beats standalone competitors.
    
    MARQUEE CLIENT: Waste Connections (Woodlands, TX). Industrial/CDL workforce. Safety = Fiduciary risk.
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

# --- HEADER SECTION ---
st.title("🛡️ PBM Strategic Command Center")
col_h1, col_h2 = st.columns([3,1])
with col_h1:
    st.markdown(f"**Target Market:** National/Enterprise Commercial ASO | **Marquee Account:** Waste Connections")
with col_h2:
    if 'last_refresh' not in st.session_state: st.session_state['last_refresh'] = "Never"
    st.write(f"Last Run: `{st.session_state['last_refresh']}`")

# --- MASTER EXECUTION ---
if refresh_btn:
    st.session_state['last_refresh'] = datetime.now().strftime("%I:%M %p")
    
    with st.status("🔍 Scanning Legislative & Market Feeds...", expanded=True) as status:
        
        # --- 6-POINT CHEAT SHEET ---
        st.subheader("📞 Strategic Call Prep (6-Point Breakdown)")
        c1, c2 = st.columns(2)
        with c1:
            st.info(analyze_aso_intel("GENERAL CALL TOPICS", "Provide 3 high-impact talking points for a general PBM Consultant audience."))
        with c2:
            st.success(analyze_aso_intel("WASTE CONNECTIONS", "Provide 3 industrial-focused talking points for Waste Connections regarding CDL safety and TX SB 1137."))

        # --- TABS ---
        tab_gov, tab_comp, tab_glp, tab_news, tab_lab = st.tabs([
            "🏛️ Gov & Regulatory", "📈 Competitor Tactics", "💉 GLP-1 War Room", "🗞️ Speculation & Rumors", "🕵️ Research Lab"
        ])

        with tab_gov:
            st.markdown("### 🏛️ Legislative Impact (1-2 Year Viability)")
            col_fed, col_state = st.columns(2)
            with col_fed:
                st.subheader("🇺🇸 Federal Impact")
                f_feeds = feedparser.parse("https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bterm%5D=PBM")
                for i, entry in enumerate(f_feeds.entries[:3]):
                    with st.expander(f"FED: {entry.title}"):
                        st.markdown(analyze_aso_intel("FEDERAL ANALYSIS", f"{entry.title}: {entry.summary}"))
            with col_state:
                st.subheader("🇨🇱 Texas State Impact")
                tx_bills = ["TX SB 1137 (Transparency)", "TX HB 1763 (Network Rules)"]
                for j, bill in enumerate(tx_bills):
                    with st.expander(f"TX: {bill}"):
                        st.markdown(analyze_aso_intel("TEXAS ANALYSIS", bill))

        with tab_comp:
            st.markdown("### 📈 Competitor Strategic Playbook")
            m_feeds = feedparser.parse("https://www.drugchannels.net/feeds/posts/default")
            for k, entry in enumerate(m_feeds.entries[:5]):
                with st.expander(f"MOVE: {entry.title}"):
                    st.markdown(analyze_aso_intel("COMPETITOR ANALYSIS", f"{entry.title}: {entry.summary}"))

        with tab_glp:
            st.markdown("### 💉 GLP-1 Commercial Strategy")
            st.markdown(analyze_aso_intel("GLP1 STRATEGY", "Analyze LillyDirect, Stop-loss Attachment Points, and BMI Custom Tiers for an Industrial workforce."))

        with tab_news:
            st.markdown("### 🗞️ Market Whispers & Speculation")
            st.markdown(analyze_aso_intel("RUMORS", "Synthesize rumors on Rightway win/loss and CVS Cordavis margin shifting."))

        status.update(label="✅ Analysis Complete", state="complete", expanded=False)

else:
    st.info("👈 Click 'GENERATE STRATEGIC BRIEFING' in the sidebar to begin.")

with tab_lab:
    st.header("🕵️ Advanced Research Lab")
    query = st.text_area("Custom Actuarial Query:", placeholder="e.g. Compare the PMPM impact of Rightway vs Prime for CDL-heavy workforces.")
    if st.button("Execute Lab Search"):
        with st.spinner("Processing Professional Analysis..."):
            st.markdown(analyze_aso_intel("CUSTOM LAB", query))

st.divider()
st.caption("Confidential Internal Strategic Tool | Audience: HR/CFO/Consultant | HCSC/Prime Therapeutics")

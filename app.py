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
    help="Detailed: Uncapped actuarial nuance and 5-year projections. CEO: Top 2 items only."
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
    
    # UNLIMITED DETAIL PROMPT
    if view_mode == "CEO View":
        tone_instruction = "TOP 2 PERTINENT ITEMS ONLY. 30-second summary. Risk indicators (Green/Yellow/Red)."
    else:
        tone_instruction = """EXPANSIVE ACTUARIAL DETAIL. Provide deep-dive analysis including:
        - Specific Bill Numbers (e.g. TX SB 1137, HB 1763) and their immediate impact on ASO audit rights.
        - Nuanced financial impacts on PMPM and Stop-loss attachment points.
        - 1, 3, and 5-year 'Fiduciary Roadmap' for the employer.
        - DO NOT BE BRIEF. Provide as much nuanced strategy as possible."""

    system_prompt = f"""You are a Lead Strategic Consultant and Senior PBM Actuary for HCSC/Prime Therapeutics. 
    You manage 150,000 lives for National/Enterprise ASO employer groups.
    
    TONE: {tone_instruction}
    
    FILTERS:
    1. ASO FOCUS ONLY: Ruthlessly ignore Medicare/Medicaid.
    2. COMPETITORS: Analyze CVS/Caremark, ESI, OptumRx, Rightway, Capital Rx, SmithRx.
    3. TEXAS SURGERY: Deep focus on TX SB 1137 (Audit rights/Transparency) and HB 1763.
    4. GLP-1 SPECIALIST: Nuance on BMI thresholds, Clinical Wait Periods, DTC models (LillyDirect), and Coupon Gapping.
    5. THE PRIME PIVOT: Highlight why HCSC/Prime's Medical+Rx Integration is a fiduciary hedge that tech-only 'navigators' can't match.
    
    {custom_instructions}
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
st.write(f"**Target Market:** Commercial ASO (National/Enterprise) | **Last Analysis:** {st.session_state['last_refresh']}")

# --- MASTER EXECUTION LOGIC ---
if refresh_btn:
    st.session_state['last_refresh'] = datetime.now().strftime("%A, %b %d at %I:%M %p")
    
    with st.status("🚀 Executing Deep-Dive War Room Analysis...", expanded=True) as status:
        
        # 1. WEEKLY CALL TOPICS
        st.subheader("📞 Weekly Client Call Cheat Sheet")
        cheat_sheet = analyze_aso_intel("WEEKLY CALL TOPICS", "Provide 3 high-value, highly specific talking points for an ASO client call. Include a specific 'Sell-Against' for Rightway in one of them.")
        st.success(cheat_sheet)
        
        tab_gov, tab_comp, tab_glp, tab_rumor, tab_lab = st.tabs([
            "🏛️ Gov & Regulatory (TX/Fed)", 
            "📈 Competitor Strategy", 
            "💉 GLP-1 War Room",
            "🗞️ Breaking News & Rumors",
            "🕵️ Intelligence Lab"
        ])

        with tab_gov:
            st.header("Surgical Regulatory Impact")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🇺🇸 Federal Impact")
                f_feeds = feedparser.parse("https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bterm%5D=PBM")
                for entry in f_feeds.entries[:4]:
                    with st.expander(f"FED: {entry.title}"):
                        st.markdown(analyze_aso_intel("FEDERAL DEEP DIVE", f"{entry.title}: {entry.summary}"))
            with col2:
                st.subheader("🇨🇱 Texas State Deep Dive")
                st.markdown(analyze_aso_intel("TX STATE ANALYSIS", "Focus specifically on SB 1137 and HB 1763. Explain immediate ASO audit impacts and network transparency requirements for 2024-2025."))

        with tab_comp:
            st.header("Competitor Tactical Playbook")
            m_feeds = feedparser.parse("https://www.drugchannels.net/feeds/posts/default")
            for entry in m_feeds.entries[:6]:
                with st.expander(f"COMPETITOR MOVE: {entry.title}"):
                    st.markdown(analyze_aso_intel("COMPETITOR STRATEGY", f"{entry.title}: {entry.summary}"))

        with tab_glp:
            st.header("💉 GLP-1 Actuarial War Room")
            st.markdown(analyze_aso_intel("GLP-1 STRATEGIC NUANCE", "Analyze LillyDirect DTC, BMI clinical hurdles, Stop-lossattachment point volatility, and Prime Integration vs Rightway navigation for GLP-1s. Use specific PBM program names where applicable."))

        with tab_rumor:
            st.header("🗞️ Breaking News & Market Whispers")
            st.markdown(analyze_aso_intel("MARKET RUMOR MILL", "Synthesize recent industry rumors regarding M&A, Rightway wins/losses, CVS Cordavis margin shifting, and potential ESI/Cigna divestitures. Call out what is speculation vs fact."))

        status.update(label="✅ Strategic Analysis Complete!", state="complete", expanded=False)

else:
    st.info("👈 Click 'EXECUTE FULL MARKET ANALYSIS' in the sidebar to begin.")

with tab_lab:
    st.header("🕵️ Advanced Intelligence Lab")
    rumor_in = st.text_area("Custom Research Query:", height=150, placeholder="e.g. 'Compare Rightway's shared savings model vs Prime's traditional ASO rebate pass-through specifically for Jumbo energy clients in Texas.'")
    if st.button("Execute Lab Research"):
        with st.spinner("Processing High-Nuance Analysis..."):
            st.markdown(analyze_aso_intel("ADVANCED RESEARCH", rumor_in))

# --- FOOTER ---
st.divider()
st.caption(f"HCSC/Prime Internal Strategic Analysis. Target Market: National/Enterprise ASO.")

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
# Set Default to Detailed View
view_mode = st.sidebar.radio(
    "Select Analysis Depth:", 
    ["Detailed View", "CEO View"], 
    index=0,
    help="Detailed: Actuarial math, bill numbers, 5-year roadmaps. CEO: Top 2 items only."
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
    
    if view_mode == "CEO View":
        tone_instruction = "TOP 2 PERTINENT ITEMS ONLY. 30-second summary. Risk indicators (Green/Yellow/Red). Immediate financial impact."
    else:
        tone_instruction = "Deep-dive actuarial analysis. Specific bill numbers, 1, 3, and 5-year financial impact modeling. Detailed PMPM/Fiduciary risk focus."

    system_prompt = f"""You are a Senior PBM Actuary and Strategic Consultant for HCSC/Prime Therapeutics. 
    You manage 150,000 lives for National/Enterprise ASO employer groups.
    
    TONE: {tone_instruction}
    
    FILTERS:
    1. ASO FOCUS ONLY.
    2. COMPETITORS: Name-check CVS/Caremark, ESI, OptumRx, Rightway, Capital Rx, SmithRx.
    3. TEXAS: Surgical focus on TX SB 1137 and HB 1763 (Audit/Transparency).
    4. PRIME PIVOT: Medical+Rx Integration advantage.
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
st.write(f"**Last Analysis:** {st.session_state['last_refresh']}")

# --- THE CALL CHEAT SHEET (TOP LEVEL) ---
st.divider()
if refresh_btn:
    st.session_state['last_refresh'] = datetime.now().strftime("%A, %b %d at %I:%M %p")
    
    with st.status("🚀 Executing Deep-Dive Analysis...", expanded=True) as status:
        
        # 1. GENERATE CALL CHEAT SHEET FIRST
        st.subheader("📞 Weekly Client Call Cheat Sheet")
        cheat_sheet = analyze_aso_intel("WEEKLY CALL TOPICS", "Based on current market trends, provide 3 high-value talking points for an ASO client call to show expertise and Prime's advantage.")
        st.success(cheat_sheet)
        
        # 2. POPULATE TABS
        tab_gov, tab_comp, tab_glp, tab_lab = st.tabs([
            "🏛️ Gov & Regulatory (Fed/TX)", 
            "📈 Competitor Strategy", 
            "💉 GLP-1 Solutions Lab",
            "🕵️ Rumor & Nuance Lab"
        ])

        with tab_gov:
            st.header("Regulatory & Legislative Impact")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🇺🇸 Federal Impact")
                f_feeds = feedparser.parse("https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bterm%5D=PBM")
                for entry in f_feeds.entries[:3]:
                    with st.expander(f"FED: {entry.title}"):
                        st.markdown(analyze_aso_intel("FEDERAL REGULATORY", entry.summary))
            with col2:
                st.subheader("🇨🇱 Texas State Impact")
                st.markdown(analyze_aso_intel("TEXAS STATE MANDATE", "Analyze TX SB 1137 and HB 1763 impact on ASO audit rights and transparency."))

        with tab_comp:
            st.header("Competitor Tactics & Market Moves")
            m_feeds = feedparser.parse("https://www.drugchannels.net/feeds/posts/default")
            for entry in m_feeds.entries[:5]:
                with st.expander(f"MOVE: {entry.title}"):
                    st.markdown(analyze_aso_intel("COMPETITOR TACTICS", f"{entry.title}: {entry.summary}"))

        with tab_glp:
            st.header("💉 GLP-1 Clinical & Financial Solutions")
            st.markdown(analyze_aso_intel("GLP-1 SOLUTIONS FEED", "Detailed analysis of LillyDirect, BMI thresholds, Coupon gapping, and Stop-loss impact for ASO groups."))

        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

else:
    st.warning("📞 WEEKLY CALL TOPICS: Analysis pending. Click 'Execute' in sidebar.")
    st.info("👈 Click 'EXECUTE FULL MARKET ANALYSIS' in the sidebar to begin.")

with tab_lab:
    st.header("🕵️ Intelligence & Search Lab")
    rumor_in = st.text_area("Market Rumor or Search Query:", height=100)
    if st.button("Execute Lab Analysis"):
        with st.spinner("Processing Nuance Analysis..."):
            st.markdown(analyze_aso_intel("STRATEGIC LAB QUERY", rumor_in))

# --- FOOTER ---
st.divider()
st.caption(f"HCSC/Prime Internal Strategic Analysis. Current View: {view_mode}")

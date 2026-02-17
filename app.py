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
    help="Detailed: Actuarial math, bill numbers, 5-year roadmaps. CEO: Top 2 pertinent items & bottom-line impact."
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
        tone_instruction = "Identify the TOP 2 most pertinent items only. Provide a 30-second summary. Use Green/Yellow/Red risk indicators. Focus ONLY on the immediate financial impact to the ASO group."
    else:
        tone_instruction = "Provide a deep-dive actuarial analysis. Include specific bill numbers, drug names, and 1, 3, and 5-year financial impact modeling. This is for a sophisticated consultant/actuary audience."

    system_prompt = f"""You are a Senior PBM Actuary and Lead Strategic Consultant for HCSC/Prime Therapeutics. 
    You manage 150,000 lives for National/Enterprise ASO employer groups.
    
    CURRENT VIEW MODE: {view_mode}
    TONE REQUIREMENT: {tone_instruction}
    
    YOUR RIGOROUS FILTERS:
    1. ASO FOCUS ONLY: Ignore Medicare/Medicaid unless material to Commercial ASO.
    2. COMPETITOR SPECIFICITY: Explicitly name-check: CVS/Caremark, ESI (Cigna), OptumRx, Rightway, Capital Rx, SmithRx.
    3. TEXAS ACCURACY: For State updates, specifically analyze TX SB 1137 and HB 1763 regarding ASO audit/transparency rights.
    4. THE PRIME PIVOT: Contrast HCSC/Prime's Integrated Health Management (Medical+Rx) against competitor tech-only models.
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
st.write(f"**Target Market:** Commercial ASO | **Last Analysis:** {st.session_state['last_refresh']}")

# --- TABS ---
tab_gov, tab_comp, tab_glp, tab_lab = st.tabs([
    "🏛️ Gov & Regulatory (Fed/TX)", 
    "📈 Competitor Strategy", 
    "💉 GLP-1 Solutions Lab",
    "🕵️ Rumor & Nuance Lab"
])

# --- MASTER EXECUTION LOGIC ---
if refresh_btn:
    st.session_state['last_refresh'] = datetime.now().strftime("%A, %b %d at %I:%M %p")
    
    # PROGRESS INDICATOR
    with st.status("🚀 Executing Deep-Dive Analysis...", expanded=True) as status:
        
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
                # Scoping specifically for the TX bills you follow
                tx_analysis = analyze_aso_intel("TEXAS STATE MANDATE", "Analyze TX SB 1137 and HB 1763. Focus on ASO audit rights, network transparency, and 2024 implementation hurdles.")
                st.markdown(tx_analysis)

        with tab_comp:
            st.header("Competitor Tactics & Market Moves")
            m_feeds = feedparser.parse("https://www.drugchannels.net/feeds/posts/default")
            for entry in m_feeds.entries[:5]:
                with st.expander(f"MOVE: {entry.title}"):
                    st.markdown(analyze_aso_intel("COMPETITOR TACTICS", f"{entry.title}: {entry.summary}"))

        with tab_glp:
            st.header("💉 GLP-1 Clinical & Financial Solutions")
            st.write("Solutions for ASO groups: BMI hurdles, DTC threats, and Integrated Management.")
            # We use the AI to generate a curated solution feed
            glp_intel = analyze_aso_intel("GLP-1 SOLUTIONS FEED", "Analyze current GLP-1 market trends: LillyDirect impact, Custom BMI thresholds, Coupon gapping, and Stop-loss attachment points for ASO groups.")
            st.markdown(glp_intel)

        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

else:
    st.info("👈 Click 'EXECUTE FULL MARKET ANALYSIS' in the sidebar to begin.")

with tab_lab:
    st.header("🕵️ Intelligence & Search Lab")
    rumor_in = st.text_area("Market Rumor or Search Query:", placeholder="e.g. 'Rightway pitching a Houston Jumbo account with a $0 spread'...")
    if st.button("Execute Lab Analysis"):
        with st.spinner("Processing Nuance Analysis..."):
            st.markdown(analyze_aso_intel("STRATEGIC LAB QUERY", rumor_in))

# --- FOOTER ---
st.divider()
st.caption(f"HCSC/Prime Internal Strategic Analysis. Current View: {view_mode}")

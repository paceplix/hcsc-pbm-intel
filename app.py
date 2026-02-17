import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime
import openai

st.set_page_config(page_title="HCSC Strategic Intel Agent", layout="wide")

# Sidebar for Control
st.sidebar.title("🛡️ HCSC/Prime Control")
api_key = st.sidebar.text_input("Enter OpenAI Key", type="password")
refresh_btn = st.sidebar.button("🔄 REFRESH DATA & ANALYZE")

# State for timestamp
if 'last_refresh' not in st.session_state:
    st.session_state['last_refresh'] = "Never"

def analyze_intel(prompt_type, data):
    if not api_key:
        st.error("Please enter your OpenAI Key in the sidebar.")
        return None
    
    client = openai.OpenAI(api_key=api_key)
    
    system_prompt = """You are the Senior Strategic Consultant for HCSC/Prime Therapeutics. 
    Analyze PBM news for 150k-life ASO accounts (National & Enterprise). 
    Focus on TX and Federal updates.
    
    For every item, provide:
    1. **Layman's Terms:** Simple explanation for an HR Director.
    2. **ASO Client Impact:** Financial risk (PMPM) and Fiduciary impact.
    3. **The Prime Sell-Against:** 
       - Against Big 3 (CVS/ESI/Optum): Focus on lack of alignment vs Prime's Blue ownership.
       - Against Niches (Rightway/SmithRx/CapRx): Focus on their tech-only model vs Prime's Integrated Medical+Rx data.
       - Biosimilars: Address Humira/Stelara lowest-net-cost strategy."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": f"{prompt_type}: {data}"}]
        )
        return response.choices[0].message.content
    except Exception as e:
        if "insufficient_quota" in str(e).lower():
            return "❌ ERROR: Your OpenAI Credits have run out. Please log into platform.openai.com and add funds."
        return f"❌ Error: {str(e)}"

# --- HEADER ---
st.title("🛡️ PBM Strategic Intel Agent")
st.write(f"**Data last refreshed:** {st.session_state['last_refresh']}")

# --- TOP SECTION: CLIENT CALL CHEAT SHEET ---
st.info("### 📞 Today's Client Call Cheat Sheet (Top 3 Topics)")
if refresh_btn:
    st.session_state['last_refresh'] = datetime.now().strftime("%A, %b %d at %I:%M %p")
    cheat_prompt = "Give me 3 high-value talking points for a biweekly ASO client call based on current TX PBM updates, Rightway/Niche competition, and Humira/Stelara biosimilars."
    st.markdown(analyze_intel("CHEAT SHEET", cheat_prompt))
else:
    st.write("Click 'Refresh Data' in the sidebar to generate today's call topics.")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["🏛️ Gov & Regulatory (TX/Fed)", "📈 Market & Competitors", "🕵️ Rumor Mill"])

with tab1:
    st.header("Texas & Federal Updates")
    # Feeds for PBM Regulatory News
    f = feedparser.parse("https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bterm%5D=PBM")
    for entry in f.entries[:3]:
        with st.expander(f"NEWS: {entry.title}"):
            if refresh_btn:
                st.markdown(analyze_intel("REGULATORY ANALYSIS", f"{entry.title}: {entry.summary}"))

with tab2:
    st.header("Market, Biosimilars & Competitors")
    # Feed for Competitor/Industry News
    m_feed = feedparser.parse("https://www.drugchannels.net/feeds/posts/default")
    for entry in m_feed.entries[:5]:
        with st.expander(f"MARKET: {entry.title}"):
            if refresh_btn:
                st.markdown(analyze_intel("MARKET ANALYSIS", f"{entry.title}: {entry.summary}"))

with tab3:
    st.header("🕵️ Rumor Mill")
    st.write("Hear a rumor about Rightway or CVS? Type it below for a strategic counter-argument.")
    rumor_in = st.text_area("Market rumor details:")
    if st.button("Analyze Rumor"):
        with st.spinner("Thinking..."):
            st.markdown(analyze_intel("RUMOR ANALYSIS", rumor_in))

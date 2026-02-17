import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime
import openai

st.set_page_config(page_title="HCSC PBM Intel: Expert Edition", layout="wide")

# Sidebar
st.sidebar.title("🛡️ HCSC/Prime Expert Control")
st.sidebar.info("ON-DEMAND MODE: Analysis only runs when triggered.")
api_key = st.sidebar.text_input("Enter OpenAI Key", type="password")
refresh_btn = st.sidebar.button("🚀 EXECUTE FULL MARKET ANALYSIS")

if 'last_refresh' not in st.session_state:
    st.session_state['last_refresh'] = "Never"

def analyze_expert_intel(prompt_type, data, custom_query=False):
    if not api_key:
        st.error("Please enter OpenAI Key.")
        return None
    
    client = openai.OpenAI(api_key=api_key)
    
    # THE "ACTUARY + STRATEGIST" SYSTEM PROMPT
    system_prompt = """You are a Senior PBM Actuary and Lead Strategic Consultant for HCSC/Prime Therapeutics. 
    You are analyzing the PBM landscape for National/Enterprise ASO-funded employer groups (150k+ lives).
    
    YOUR RIGOROUS STANDARDS:
    1. MATERIALITY: Focus ONLY on events that impact PMPM, Fiduciary risk, or Pharmacy Contract mechanics.
    2. NUANCE & DETAIL: Include specific Bill Numbers (e.g., TX SB 1137, HR 2884), drug names, and competitor tactics.
    3. TEMPORAL IMPACT: For every analysis, you MUST provide:
       - 1-Year Impact: Implementation hurdles, immediate cost shifts, member disruption.
       - 3-Year Impact: Rebate erosion, contract cycle changes, market consolidation.
       - 5-Year Impact: Total structural shift in the PBM model (e.g., the move away from rebates).
    4. THE PRIME SELL-AGAIN: Explain why HCSC/Prime's Blue-aligned, medical-integrated model is a superior hedge against this news compared to the Big 3 (CVS/ESI/Optum) or tech-only 'Navigation' niches (Rightway/CapRx).
    """

    try:
        # If it's a general search query, we want the AI to use its full internal knowledge
        model_to_use = "gpt-4o"
        user_content = f"{prompt_type}: {data}"
        
        response = client.chat.completions.create(
            model=model_to_use,
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_content}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- HEADER ---
st.title("🛡️ PBM Strategic Intel: Expert Mode")
st.write(f"**Data Last Refreshed:** {st.session_state['last_refresh']}")

# --- TABBED INTERFACE ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🏛️ Material Regulatory (TX/Fed)", 
    "📈 Market & Competitor Deep-Dive", 
    "🕵️ Rumor & Nuance Lab",
    "🔍 Strategic Search Query"
])

with tab1:
    st.header("High-Materiality Regulatory Watch")
    st.caption("Focus: Bill Numbers, ERISA Risk, and TX Compliance.")
    # Wider Net for Regulatory
    feeds = [
        "https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bterm%5D=PBM",
        "https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bterm%5D=Pharmacy+Benefit"
    ]
    if refresh_btn:
        st.session_state['last_refresh'] = datetime.now().strftime("%A, %b %d at %I:%M %p")
        for url in feeds:
            f = feedparser.parse(url)
            for entry in f.entries[:5]: # Wide Net
                with st.expander(f"📜 DETAILED IMPACT: {entry.title}"):
                    st.markdown(analyze_expert_intel("REGULATORY DEEP-DIVE", f"Title: {entry.title}\nSummary: {entry.summary}"))
    else:
        st.info("Click 'EXECUTE FULL MARKET ANALYSIS' to pull data.")

with tab2:
    st.header("Market Moves & Competitor Tactics")
    st.caption("Focus: Big 3 Margin Grabs vs. Niche PBM (Rightway) Tech Pitch.")
    m_feeds = ["https://www.drugchannels.net/feeds/posts/default"]
    if refresh_btn:
        for url in m_feeds:
            f = feedparser.parse(url)
            for entry in f.entries[:8]: # Wider Net
                with st.expander(f"📈 STRATEGIC ANALYSIS: {entry.title}"):
                    st.markdown(analyze_expert_intel("MARKET DYNAMICS", f"Title: {entry.title}\nSummary: {entry.summary}"))
    else:
        st.info("Click 'EXECUTE FULL MARKET ANALYSIS' to pull data.")

with tab3:
    st.header("🕵️ Rumor & Nuance Lab")
    st.write("Analyze 'on-the-street' intel with 1, 3, and 5-year impact modeling.")
    rumor_in = st.text_area("Detail the rumor or trend here:", placeholder="e.g. Rightway is moving to a shared-savings model for GLP-1s in Texas...", height=150)
    if st.button("Analyze Nuance"):
        with st.spinner("Calculating long-term impact..."):
            st.markdown(analyze_expert_intel("RUMOR ANALYSIS", rumor_in))

with tab4:
    st.header("🔍 Strategic Search Query")
    st.write("Ask a specific strategic question. The AI will cross-reference its knowledge of PBMs, TX law, and HCSC strategy.")
    search_query = st.text_input("What would you like to research?", placeholder="e.g. Explain the impact of TX SB 1137 on ASO audit rights vs Big 3 PBMs.")
    if st.button("Search & Analyze"):
        with st.spinner("Executing Research..."):
            st.markdown(analyze_expert_intel("STRATEGIC RESEARCH QUERY", search_query))

# --- FOOTER ---
st.divider()
st.caption("Confidential Strategic Tool for HCSC/Prime Therapeutics Internal Use Analysis.")

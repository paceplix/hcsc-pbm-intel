import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime
import openai
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Imperial Setup: Stable and Swift
st.set_page_config(page_title="PBM Imperial Command Center", layout="wide")

# Sidebar Throne
st.sidebar.title("🛡️ Imperial Command")
api_engine = st.sidebar.selectbox("Oracle Engine", ["OpenAI", "Grok (xAI)"])
api_key = st.sidebar.text_input("Oracle Key", type="password")

st.sidebar.divider()
view_mode = st.sidebar.radio("Imperial Gaze", ["Emperor's Glance (Concise)", "Warlord's Tome (Exhaustive)"], index=1)

st.sidebar.divider()
refresh_btn = st.sidebar.button("🚀 Summon Imperial Briefing")

# Fortified Feeds: Targeted for PBM Warfare
FEEDS = {
    "Regulatory Bastion": [
        "https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bterm%5D=PBM",  # Fed PBM
        "https://www.cms.gov/newsroom/rss-feeds/newsroom-all-releases.xml",  # CMS
        "https://capitol.texas.gov/Rss/Rss.aspx?Type=Bill"  # TX Legislature (PBM filter in analysis)
    ],
    "Market Annihilator": [
        "https://www.drugchannels.net/feeds/posts/default",  # Adam Fein
        "https://www.fiercehealthcare.com/rss/healthcare",  # Fierce
        "https://www.statnews.com/topic/pharmaceuticals/feed/"  # Biosimilars/Pharma
    ]
}

# AE/Consulting Oracle: Your Cunning Vizier
def summon_oracle(prompt_type, data):
    if not api_key:
        return "⚠️ Oracle Key Demanded, Grand Duke!"
    
    if api_engine == "Grok (xAI)":
        client = openai.OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
        model = "grok-beta"  # Leverage X wisdom
    else:
        client = openai.OpenAI(api_key=api_key)
        model = "gpt-4o"
    
    system_edict = f"""
    You are the Imperial PBM Vizier—an HCSC/Prime Account Executive with a Mercer/Aon consulting brain. Command 150k ASO lives; fortify Waste Connections (TX industrial/CDL horde: GLP-1 volatility, safety fiduciary shields under SB 1137/HB 1763).
    
    Edicts for Every Decree:
    1. **Layman's Beacon**: Illuminate for HR Directors—simple, punchy.
    2. **Fiduciary Fortress**: Dissect risks/PMPM models (1/3/5-year forecasts, ERISA breaches, stop-loss spikes).
    3. **Prime Onslaught**: Table of sell-against: Big 3 (rebate hoards), Niche (Rightway tech facade—no med integration), Coalitions (rigid formularies).
    4. **AE Arsenal**: 3-5 scripted volleys for client calls ("Grand Duke, deploy thus: 'Consultant, your Rightway app is a mirage—our integration shields $X PMPM...'").
    5. **TX Rampart**: Highlight Texas impacts (audit rights, white bagging).
    
    Mark [🟢 FACT] or [🟡 SPECULATION]. Impact: HIGH/MED/LOW. { 'Concise (2-3 edicts)' if view_mode == "Emperor's Glance (Concise)" else 'Exhaustive (10+ edicts with models/scripts)' }.
    Output Readable: Bullets, tables, no fluff—actionable empire-building.
    """
    
    try:
        response = client.chat.completions.create(
            model=model,
            max_tokens=4000 if view_mode == "Warlord's Tome (Exhaustive)" else 1500,
            messages=[{"role": "system", "content": system_edict}, {"role": "user", "content": f"{prompt_type}: {data}"}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Vizier Treason: {str(e)}. Inspect key/credits."

# Main Citadel
st.title("🛡️ PBM Imperial Command Center")
st.markdown(f"**Empire Focus:** ASO Dominance | **Marquee Citadel:** Waste Connections (TX)")

if refresh_btn:
    with st.spinner("Forging Imperial Decrees..."):
        decrees = {}  # For Exports
        
        # Call Prep Arsenal
        st.subheader("📞 Imperial Call Arsenal")
        col_gen, col_waste = st.columns(2)
        with col_gen:
            gen_decree = summon_oracle("GENERAL WAR COUNCIL", "Forge edicts on PBM reform, biosimilars, ERISA shields.")
            st.info(gen_decree)
            decrees["General Arsenal"] = gen_decree
        with col_waste:
            waste_decree = summon_oracle("WASTE CONNECTIONS SIEGE", "Tailor edicts for Waste: CDL integration, GLP-1 industrial PMPM, TX audit ramparts.")
            st.success(waste_decree)
            decrees["Waste Citadel"] = waste_decree

        # War Rooms (Tabs)
        tab_reg, tab_mkt, tab_glp, tab_rumor, tab_lab = st.tabs(["🏛️ Regulatory Bastion", "📈 Market Annihilator", "💉 GLP-1 Vanguard", "🕵️ Rumor Forge", "🧪 Strategy Lab"])

        with tab_reg:
            st.header("Regulatory Decrees")
            for cat, urls in FEEDS.items():
                st.subheader(cat)
                for url in urls:
                    feed = feedparser.parse(url)
                    for entry in feed.entries[:3]:  # Limit for speed
                        with st.expander(f"Decree: {entry.title}"):
                            analysis = summon_oracle("REGULATORY DISSECTION", f"{entry.title}: {entry.summary}")
                            st.markdown(analysis)
                            decrees[entry.title] = analysis

        with tab_mkt:
            st.header("Competitor Onslaught")
            # Similar feed loop as above, with market-specific prompt
            # Example: analysis = summon_oracle("MARKET ANNIHILATION", ...)

        with tab_glp:
            st.header("GLP-1 Vanguard")
            glp_decree = summon_oracle("GLP1 WARFARE", "Dissect LillyDirect, BMI hurdles, stop-loss for industrial hordes like Waste.")
            st.markdown(glp_decree)
            decrees["GLP-1 Vanguard"] = glp_decree

        with tab_rumor:
            st.header("Rumor Forge")
            rumor_query = st.text_area("Forge Rumor (e.g., 'Rightway TX Jumbo Bid')")
            if st.button("Summon Rumor Decree"):
                rumor_decree = summon_oracle("RUMOR SIEGE", rumor_query)
                st.warning(rumor_decree)  # Yellow for speculation
                decrees["Rumor Forge"] = rumor_decree

        with tab_lab:
            st.header("Strategy Lab")
            lab_query = st.text_area("Imperial Query (e.g., 'PMPM Impact: Rightway vs Prime for CDL')")
            if st.button("Execute Lab Edict"):
                lab_decree = summon_oracle("STRATEGY ALCHEMY", lab_query)
                st.markdown(lab_decree)
                decrees["Strategy Lab"] = lab_decree

        # Export Dominion
        st.subheader("Export Imperial Decrees")
        df = pd.DataFrame.from_dict(decrees, orient='index', columns=['Edict'])
        csv = df.to_csv().encode('utf-8')
        st.download_button("CSV Decree", csv, "imperial_decrees.csv")

        # PDF Export (Simple, readable)
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        y = 750
        for title, text in decrees.items():
            c.drawString(100, y, title)
            y -= 20
            for line in text.split('\n')[:20]:  # Truncate for PDF
                c.drawString(120, y, line)
                y -= 15
            if y < 50:
                c.showPage()
                y = 750
        c.save()
        pdf_buffer.seek(0)
        st.download_button("PDF Scroll", pdf_buffer, "imperial_scroll.pdf", "application/pdf")

    st.success("Decrees Forged, Grand Duke! Timestamp: " + datetime.now().strftime("%Y-%m-%d %H:%M"))

else:
    st.info("Await Your Command: Key the Oracle and Summon the Briefing.")

# Footer Ward
st.divider()
st.caption("Forged for the Grand Duke's Eternal Reign | HCSC/Prime Empire")

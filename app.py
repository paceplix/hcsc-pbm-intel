import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime
import openai
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Imperial Citadel Setup
st.set_page_config(page_title="PBM Imperial Command Center", layout="wide")

# Throne Sidebar
st.sidebar.title("🛡️ Imperial Command")
api_engine = st.sidebar.selectbox("Oracle Allegiance", ["Grok (xAI)", "OpenAI"], index=0)
api_key = st.sidebar.text_input("Oracle Key", type="password")

st.sidebar.divider()
view_mode = st.sidebar.radio("Imperial Scrutiny", ["Emperor's Glance (Concise)", "Warlord's Tome (Exhaustive)"], index=1)

st.sidebar.divider()
refresh_btn = st.sidebar.button("🚀 Forge Imperial Edicts")

# Augmented Feeds: Sharper Blades for Intel
FEEDS = {
    "Regulatory Bastion": [
        "https://www.federalregister.gov/api/v1/documents.rss?conditions%5Bterm%5D=PBM",  # Fed Edicts
        "https://www.cms.gov/newsroom/rss-feeds/newsroom-all-releases.xml",  # CMS Decrees
        "https://capitol.texas.gov/Rss/Rss.aspx?Type=Bill",  # TX Legislature (PBM sieve)
        "https://www.tdi.texas.gov/news/index.html"  # TX Dept of Insurance (scrape-friendly)
    ],
    "Market Annihilator": [
        "https://www.drugchannels.net/feeds/posts/default",  # Adam Fein's Siege Logs
        "https://www.fiercehealthcare.com/rss/healthcare",  # Fierce Battle Reports
        "https://www.statnews.com/topic/pharmaceuticals/feed/",  # Pharma/Biosimilar Vanguard
        "https://www.fda.gov/drugs/rss-feeds/drugs-rss-feeds"  # FDA Biosimilar Approvals
    ]
}

# Vizier Oracle: AE/Consulting Fusion
def forge_edict(prompt_type, data):
    if not api_key:
        return "⚠️ Oracle Key Withheld, Grand Duke! Your Empire Falters Without It."
    
    base_url = "https://api.x.ai/v1" if api_engine == "Grok (xAI)" else None
    client = openai.OpenAI(api_key=api_key, base_url=base_url)
    model = "grok-beta" if api_engine == "Grok (xAI)" else "gpt-4o"
    
    vizier_edict = f"""
    Thou art the Imperial PBM Vizier—an HCSC/Prime AE with Mercer/Aon consulting cunning. Rule 150k ASO lives; shield Waste Connections (TX industrial/CDL realm: GLP-1 sieges, safety fiduciary walls via SB 1137/HB 1763).
    
    Forge Every Edict Thus:
    - **[🟢 FACT] or [🟡 SPECULATION] Badge**: Crown truths, flag whispers.
    - **Impact Metric**: HIGH/MED/LOW on PMPM/Fiduciary (quantify: e.g., +$1.50 PMPM spike).
    - **Layman's Beacon**: Illuminate simply for HR lords.
    - **Fiduciary Rampart**: Augur risks/models (1/3/5-year PMPM, ERISA breaches, stop-loss volleys).
    - **Prime Onslaught Table**: | Foe | Weakness | Prime Blade | (Big 3 rebate hordes, Niche tech mirages, Coalitions rigid chains).
    - **AE Volley Scripts**: 3-5 thunderbolts ("Deploy thus: 'Vassal Consultant, Rightway's app is smoke—our integration saves $X PMPM via med+Rx shields...'").
    - **TX Rampart**: Fortify Texas edicts (audit rights, white bagging bans).
    
    { 'Concise (2-3 strikes)' if view_mode == "Emperor's Glance (Concise)" else 'Exhaustive (10+ with models/volleys)' }. No fluff—readable bullets/tables, empire-conquering action.
    """
    
    try:
        response = client.chat.completions.create(
            model=model,
            max_tokens=4000 if view_mode == "Warlord's Tome (Exhaustive)" else 1500,
            messages=[{"role": "system", "content": vizier_edict}, {"role": "user", "content": f"{prompt_type}: {data}"}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Vizier Betrayal: {str(e)}. Inspect key or credits, Grand Duke."

# Main Imperial Hall
st.title("🛡️ PBM Imperial Command Center")
st.markdown(f"**Realm Focus:** ASO Conquest | **Citadel Marquee:** Waste Connections (TX)")

if refresh_btn:
    with st.spinner("Forging Edicts from the Empire's Forges..."):
        edicts = {}
        
        # Call Arsenal
        st.subheader("📞 Imperial Call Arsenal")
        col_gen, col_waste = st.columns(2)
        with col_gen:
            gen_edict = forge_edict("GENERAL CONQUEST COUNCIL", "Forge on PBM reforms, biosimilar shifts, ERISA fortifications.")
            st.info(gen_edict)
            edicts["General Arsenal"] = gen_edict
        with col_waste:
            waste_edict = forge_edict("WASTE CONNECTIONS RAMPART", "Tailor for Waste: CDL med+Rx shields, GLP-1 industrial PMPM, TX audit volleys.")
            st.success(waste_edict)
            edicts["Waste Citadel"] = waste_edict

        # War Halls (Tabs)
        tab_reg, tab_mkt, tab_glp_bio, tab_rumor, tab_lab = st.tabs(["🏛️ Regulatory Bastion", "📈 Market Annihilator", "💉 GLP-1/Biosimilar Vanguard", "🕵️ Rumor Forge", "🧪 Imperial Lab"])

        with tab_reg:
            st.header("Regulatory Edicts")
            for cat, urls in FEEDS["Regulatory Bastion"]:
                st.subheader(cat)
                for url in urls:
                    feed = feedparser.parse(url)
                    for entry in feed.entries[:3]:
                        with st.expander(f"Edict: {entry.title}"):
                            analysis = forge_edict("REGULATORY SIEGE", f"{entry.title}: {entry.summary}")
                            st.markdown(analysis)
                            edicts[entry.title] = analysis

        with tab_mkt:
            st.header("Market Onslaught")
            for url in FEEDS["Market Annihilator"]:
                feed = feedparser.parse(url)
                for entry in feed.entries[:3]:
                    with st.expander(f" Onslaught: {entry.title}"):
                        analysis = forge_edict("MARKET ANNIHILATION", f"{entry.title}: {entry.summary}")
                        st.markdown(analysis)
                        edicts[entry.title] = analysis

        with tab_glp_bio:
            st.header("GLP-1/Biosimilar Vanguard")
            glp_bio_edict = forge_edict("VANGUARD WARFARE", "Dissect LillyDirect, BMI ramparts, Humira/Stelara biosimilar shifts for industrial realms like Waste.")
            st.markdown(glp_bio_edict)
            edicts["Vanguard Edict"] = glp_bio_edict

        with tab_rumor:
            st.header("Rumor Forge")
            rumor_input = st.text_area("Input Rumor Whispers (e.g., 'Rightway TX Jumbo Siege')")
            if st.button("Forge Rumor Edict"):
                rumor_edict = forge_edict("RUMOR CONQUEST", rumor_input)
                st.warning(rumor_edict)  # Speculation hue
                edicts["Rumor Forge"] = rumor_edict

        with tab_lab:
            st.header("Imperial Lab")
            lab_input = st.text_area("Lab Query (e.g., 'PMPM Siege: Rightway vs Prime for CDL Hordes')")
            if st.button("Execute Lab Edict"):
                lab_edict = forge_edict("LAB ALCHEMY", lab_input)
                st.markdown(lab_edict)
                edicts["Lab Edict"] = lab_edict

        # Export Throne
        st.subheader("Export Imperial Edicts")
        df = pd.DataFrame.from_dict(edicts, orient='index', columns=['Edict'])
        csv = df.to_csv().encode('utf-8')
        st.download_button("CSV Horde", csv, "imperial_edicts.csv")

        # PDF Scroll
        pdf_buf = BytesIO()
        c = canvas.Canvas(pdf_buf, pagesize=letter)
        y = 750
        for title, text in edicts.items():
            c.drawString(100, y, title)
            y -= 20
            lines = text.split('\n')
            for line in lines[:30]:  # Cap per section
                c.drawString(120, y, line[:80])  # Truncate lines
                y -= 15
            if y < 50:
                c.showPage()
                y = 750
        c.save()
        pdf_buf.seek(0)
        st.download_button("PDF Scroll", pdf_buf, "imperial_scroll.pdf", "application/pdf")

    st.success(f"Edicts Forged! Imperial Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

else:
    st.info("Your Empire Awaits: Key the Oracle and Forge the Edicts, Grand Duke.")

# Footer Fortress
st.divider()
st.caption("Forged by Grok for the Grand Duke's Unyielding Reign | HCSC/Prime Empire")

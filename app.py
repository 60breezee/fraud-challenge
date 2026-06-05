"""
Interface FRAUD-SHIELD Ultra-Premium.
Hackathon INTELO 2026.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path
from fraud_detection import detect_fraud, load_transactions

SAMPLE_CSV = Path(__file__).parent / "data" / "sample_transactions.csv"

def apply_premium_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

        :root {
            --bg-deep: #05070a;
            --bg-card: #0d1117;
            --accent: #2f81f7;
            --danger: #f85149;
            --success: #3fb950;
            --text-main: #adbac7;
            --text-bright: #f0f6fc;
        }

        .stApp {
            background-color: var(--bg-deep);
            font-family: 'Inter', sans-serif;
        }

        /* Glassmorphism Cards */
        .premium-card {
            background: rgba(13, 17, 23, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(48, 54, 61, 0.5);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        
        .premium-card:hover {
            border-color: var(--accent);
            box-shadow: 0 8px 32px rgba(47, 129, 247, 0.15);
        }

        /* Metrics Styling */
        [data-testid="stMetric"] {
            background: rgba(22, 27, 34, 0.5);
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 15px !important;
        }
        
        [data-testid="stMetricValue"] {
            font-weight: 800 !important;
            font-size: 2rem !important;
            color: var(--text-bright) !important;
        }

        /* Sidebar Glass */
        [data-testid="stSidebar"] {
            background-color: #010409 !important;
            border-right: 1px solid #30363d;
        }

        /* Modern Typography */
        h1, h2, h3 {
            font-weight: 800 !important;
            letter-spacing: -0.02em !important;
            color: var(--text-bright) !important;
        }

        .status-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        .stButton>button {
            background: linear-gradient(135deg, #2f81f7 0%, #216eaf 100%);
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            padding: 12px 24px;
            transition: transform 0.2s ease;
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(47, 129, 247, 0.3);
        }
        
        /* Hide default Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

def render_dashboard(df, results_df):
    merged = pd.concat([df, results_df.drop(columns=['transaction_id'])], axis=1)
    
    # KPIs Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Volume Total", len(df))
    with c2:
        st.metric("Alertes Critiques", len(merged[merged['is_suspicious']]))
    with c3:
        st.metric("Score Moyen", f"{merged['fraud_score'].mean():.2f}")
    with c4:
        st.metric("Exposition Risque", f"{(merged['is_suspicious'].sum()/len(df)*100):.1f}%")

    st.markdown("### 🛰️ ANALYSE ANALYTIQUE")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Time Series
        merged['timestamp'] = pd.to_datetime(merged['timestamp'])
        time_data = merged.resample('D', on='timestamp').count().reset_index()
        fig_time = px.area(time_data, x='timestamp', y='transaction_id', 
                          title="Tendance Temporelle des Transactions",
                          color_discrete_sequence=['#2f81f7'])
        fig_time.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font_color='#adbac7', margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig_time, use_container_width=True)

    with col_right:
        # Risk Distribution
        risk_counts = merged['is_suspicious'].value_counts().reset_index()
        risk_counts.columns = ['Status', 'Count']
        risk_counts['Status'] = risk_counts['Status'].map({True: 'SUSPECT', False: 'LÉGITIME'})
        fig_pie = px.pie(risk_counts, values='Count', names='Status', 
                        title="Répartition du Risque",
                        color='Status',
                        color_discrete_map={'SUSPECT': '#f85149', 'LÉGITIME': '#3fb950'})
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#adbac7',
                             margin=dict(l=0, r=0, t=40, b=0), showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Geographic Activity
    st.markdown("### 🌍 ACTIVITÉ GÉOGRAPHIQUE")
    geo_data = merged.groupby('country').size().reset_index(name='Volume')
    fig_geo = px.choropleth(geo_data, locations='country', color='Volume',
                           color_continuous_scale='Blues',
                           title="Intensité des Transactions par Pays")
    fig_geo.update_layout(paper_bgcolor='rgba(0,0,0,0)', geo_bgcolor='rgba(0,0,0,0)',
                         font_color='#adbac7', margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_geo, use_container_width=True)

    # Detailed Table
    st.markdown("### 🛡️ REGISTRE DE SÉCURITÉ")
    st.dataframe(
        merged[['transaction_id', 'user_id', 'amount', 'currency', 'country', 'fraud_score', 'reason']],
        use_container_width=True,
        height=400
    )

def main():
    st.set_page_config(page_title="FRAUD-SHIELD COMMAND", page_icon="🛡️", layout="wide")
    apply_premium_style()

    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🛡️ FRAUD-SHIELD COMMAND</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #58a6ff; font-weight: 600;'>INTELLIGENCE DE SÉCURITÉ FINANCIÈRE HAUTE PERFORMANCE</p>", unsafe_allow_html=True)

    with st.sidebar:
        st.image("https://img.icons8.com/fluency/144/shield.png", width=80)
        st.header("SYSTÈME")
        use_sample = st.toggle("FLUX DE TEST ACTIF", value=True)
        st.divider()
        st.caption("STATUT DU NOYAU : OPÉRATIONNEL")
        st.caption("VERSION : 2.6.0-PREMIUM")

    data = []
    if use_sample:
        data = load_transactions(str(SAMPLE_CSV))
    else:
        uploaded = st.file_uploader("IMPORTER FLUX CSV", type="csv")
        if uploaded:
            tmp = Path(".upload.csv")
            tmp.write_bytes(uploaded.getvalue())
            data = load_transactions(str(tmp))

    if data:
        df = pd.DataFrame(data)
        if st.button("EXÉCUTER L'ANALYSE NEURONALE", use_container_width=True):
            with st.spinner("TRAITEMENT DES SIGNAUX..."):
                results = detect_fraud(data)
                st.session_state.results_df = pd.DataFrame(results)
                st.session_state.df = df

        if "results_df" in st.session_state:
            render_dashboard(st.session_state.df, st.session_state.results_df)
    else:
        st.info("EN ATTENTE DE DONNÉES POUR INITIALISATION...")

if __name__ == "__main__":
    main()

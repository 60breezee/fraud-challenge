"""
FRAUD-SHIELD EXECUTIVE COMMAND CENTER
Style : Premium Executive - Typography : Times New Roman
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path
from fraud_detection import detect_fraud, load_transactions

# Configuration de la page
st.set_page_config(page_title="FRAUD-SHIELD | Executive Command", page_icon="🛡️", layout="wide")

def apply_executive_style():
    st.markdown("""
        <style>
        /* Typography : Times New Roman */
        html, body, [class*="st-"] {
            font-family: 'Times New Roman', Times, serif !important;
        }

        :root {
            --executive-dark: #1a1c1e;
            --executive-gold: #c5a059;
            --executive-green: #0b3d2e;
            --paper-white: #fdfdfd;
            --border-subtle: #e1e1e1;
        }

        .stApp {
            background-color: var(--paper-white);
            color: #2c2c2c;
        }

        /* Sidebar Executive Look */
        [data-testid="stSidebar"] {
            background-color: var(--executive-dark) !important;
            color: white !important;
            border-right: 2px solid var(--executive-gold);
        }
        
        [data-testid="stSidebar"] * {
            color: white !important;
            font-family: 'Times New Roman', Times, serif !important;
        }

        /* Executive Headers */
        h1, h2, h3 {
            font-family: 'Times New Roman', Times, serif !important;
            font-weight: 700 !important;
            color: var(--executive-dark) !important;
            border-bottom: 1px solid var(--executive-gold);
            padding-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Premium Metrics */
        [data-testid="stMetric"] {
            background: #ffffff;
            border-left: 4px solid var(--executive-gold);
            padding: 20px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        
        [data-testid="stMetricLabel"] {
            font-style: italic !important;
            font-size: 1.1rem !important;
        }

        /* Executive Buttons */
        .stButton>button {
            background-color: var(--executive-dark) !important;
            color: var(--executive-gold) !important;
            border: 1px solid var(--executive-gold) !important;
            border-radius: 0px !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            padding: 15px 30px !important;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: var(--executive-gold) !important;
            color: white !important;
        }

        /* Status Badges */
        .risk-badge {
            padding: 5px 15px;
            border: 1px solid #d32f2f;
            color: #d32f2f;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 0.8rem;
        }
        
        /* Layout adjustments */
        .main .block-container {
            padding-top: 2rem;
        }
        
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

def render_executive_dashboard(df, results_df):
    merged = pd.concat([df, results_df.drop(columns=['transaction_id'])], axis=1)
    
    # --- TOP ROW : KPI ---
    st.markdown("### Executive Summary")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Portfolio Volume", len(df))
    with c2:
        st.metric("Critical Alerts", len(merged[merged['is_suspicious']]))
    with c3:
        st.metric("Exposure Index", f"{merged['fraud_score'].mean():.2f}")
    with c4:
        st.metric("Asset Safety", f"{(1 - merged['is_suspicious'].sum()/len(df))*100:.1f}%")

    st.divider()

    # --- MIDDLE ROW : PLANISPHERE & DISTRIBUTION ---
    col_map, col_dist = st.columns([2, 1])
    
    with col_map:
        st.markdown("### Global Risk Surveillance")
        geo_data = merged.groupby('country').size().reset_index(name='Volume')
        fig_map = px.choropleth(geo_data, locations='country', color='Volume',
                                color_continuous_scale='YlOrBr',
                                projection="natural earth")
        fig_map.update_layout(
            font_family="Times New Roman",
            paper_bgcolor='rgba(0,0,0,0)',
            geo_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_dist:
        st.markdown("### Verdict Distribution")
        risk_counts = merged['is_suspicious'].value_counts().reset_index()
        risk_counts.columns = ['Status', 'Count']
        risk_counts['Status'] = risk_counts['Status'].map({True: 'HIGH RISK', False: 'SECURE'})
        fig_donut = px.pie(risk_counts, values='Count', names='Status', hole=0.5,
                           color_discrete_sequence=['#c5a059', '#1a1c1e'])
        fig_donut.update_layout(font_family="Times New Roman", showlegend=True,
                               margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_donut, use_container_width=True)

    # --- BOTTOM ROW : ANALYTICS & LOG ---
    st.markdown("### Advanced Risk Analytics")
    col_line, col_table = st.columns([1, 1])
    
    with col_line:
        # Time distribution diagram
        merged['timestamp'] = pd.to_datetime(merged['timestamp'])
        time_data = merged.resample('D', on='timestamp').count().reset_index()
        fig_line = px.line(time_data, x='timestamp', y='transaction_id', 
                           title="Activity Trendline")
        fig_line.update_traces(line_color='#c5a059')
        fig_line.update_layout(font_family="Times New Roman", paper_bgcolor='rgba(0,0,0,0)', 
                               plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_line, use_container_width=True)

    with col_table:
        st.markdown("### Transaction Ledger")
        st.dataframe(
            merged[['transaction_id', 'amount', 'country', 'fraud_score', 'reason']].head(10),
            use_container_width=True
        )

def main():
    apply_executive_style()
    
    # Custom Header
    st.markdown("""
        <div style="text-align: center; border-bottom: 2px solid #c5a059; padding-bottom: 20px; margin-bottom: 30px;">
            <h1 style="font-size: 3rem; margin: 0;">FINANCIAL INTEGRITY COMMAND</h1>
            <p style="font-style: italic; font-size: 1.2rem; color: #666;">High-Level Fraud Surveillance & Neural Auditing</p>
        </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h2 style='color:white; border:none;'>CONTROL PANEL</h2>", unsafe_allow_html=True)
        st.divider()
        use_sample = st.checkbox("Stream Live Data Sample", value=True)
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.info("System Status: OPERATIONAL")
        st.caption("Protocol: INTELO-2026-X")

    # Data Loading
    SAMPLE_CSV = Path(__file__).parent / "data" / "sample_transactions.csv"
    data = load_transactions(str(SAMPLE_CSV)) if use_sample else []

    if data:
        if st.button("AUTHENTICATE & ANALYZE NEURAL FEED", use_container_width=True):
            with st.spinner("Processing Secure Feed..."):
                results = detect_fraud(data)
                render_executive_dashboard(pd.DataFrame(data), pd.DataFrame(results))
    else:
        st.warning("Awaiting secure data feed for initialization.")

if __name__ == "__main__":
    main()

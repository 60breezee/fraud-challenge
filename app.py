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
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

        /* Typography Override */
        html, body, [class*="st-"] {
            font-family: 'Times New Roman', Times, serif !important;
        }

        :root {
            --executive-dark: #0a0b0c;
            --executive-gold: #d4af37;
            --executive-accent: #1e293b;
            --paper-white: #ffffff;
            --risk-high: #dc2626;
            --risk-low: #059669;
        }

        .stApp {
            background-color: #f8fafc;
            color: #1e293b;
        }

        /* Sidebar Glassmorphism */
        [data-testid="stSidebar"] {
            background-color: var(--executive-dark) !important;
            border-right: 2px solid var(--executive-gold);
            box-shadow: 10px 0 30px rgba(0,0,0,0.5);
        }
        
        [data-testid="stSidebar"] * {
            color: #e2e8f0 !important;
        }

        /* Card System */
        .exec-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border-top: 3px solid var(--executive-gold);
        }

        h1, h2, h3 {
            font-weight: 800 !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--executive-dark) !important;
        }

        /* Metric Overrides */
        [data-testid="stMetric"] {
            background: white !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 4px !important;
            padding: 20px !important;
            border-left: 5px solid var(--executive-gold) !important;
        }

        .stButton>button {
            background: var(--executive-dark) !important;
            color: var(--executive-gold) !important;
            border: 1px solid var(--executive-gold) !important;
            border-radius: 0px !important;
            font-weight: 700 !important;
            letter-spacing: 2px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .stButton>button:hover {
            background: var(--executive-gold) !important;
            color: white !important;
            transform: scale(1.02);
        }

        .status-pill {
            padding: 2px 10px;
            font-size: 10px;
            font-weight: bold;
            border-radius: 100px;
            text-transform: uppercase;
        }
        </style>
    """, unsafe_allow_html=True)

def render_radar_chart(merged):
    # Dimensions de risque agrégées pour le radar
    categories = ['Volume', 'Score de Risque', 'Géo-Vélocité', 'Pic de Montant', 'Fréquence']
    
    # Agrégation factice pour l'effet radar
    values = [
        len(merged) / 100,
        merged['fraud_score'].mean() * 10,
        merged[merged['reason'].str.contains('Géo|Incohérence', na=False)]['fraud_score'].count() * 2,
        merged[merged['reason'].str.contains('Montant', na=False)]['fraud_score'].count() * 2,
        merged[merged['reason'].str.contains('fréquentes', na=False)]['fraud_score'].count() * 2
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Profil de Risque',
        line_color=None,
        fillcolor='rgba(212, 175, 55, 0.4)'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=False,
        font_family="Times New Roman",
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def render_executive_dashboard(df, results_df):
    merged = pd.concat([df, results_df.drop(columns=['transaction_id'])], axis=1)
    
    # Traitement des données complètes
    filtered = merged.copy()

    # KPIs
    st.markdown("### INDICATEURS CLÉS D'INTELLIGENCE")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("UNITÉS ANALYSÉES", len(df))
    k2.metric("MENACES NEUTRALISÉES", len(filtered[filtered['is_suspicious']]))
    k3.metric("VECTEUR D'ATTAQUE MOYEN", f"{filtered['fraud_score'].mean():.2f}" if not filtered.empty else "0.00")
    k4.metric("INTÉGRITÉ DU SYSTÈME", f"{(1 - filtered['is_suspicious'].sum()/len(df))*100:.1f}%" if len(df) > 0 else "100%")

    st.divider()

    # Grille d'Analyse Visuelle
    col_a, col_b = st.columns([1.5, 1])
    
    with col_a:
        st.markdown("### SURVEILLANCE GÉOSPATIALE GLOBALE (3D)")
        if not filtered.empty:
            # Agrégation avancée pour le globe
            geo_data = filtered.groupby('country').agg({
                'fraud_score': 'mean',
                'transaction_id': 'count'
            }).reset_index()
            geo_data.columns = ['country', 'Risque Moyen', 'Volume']
            
            fig_map = px.choropleth(
                geo_data, 
                locations='country', 
                color='Risque Moyen',
                hover_name='country',
                hover_data={'Volume': True, 'Risque Moyen': ':.2f'},
                color_continuous_scale='YlOrBr',
                projection="orthographic"  # Passage en mode Globe 3D
            )
            
            fig_map.update_geos(
                showcountries=True, 
                countrycolor="rgba(212, 175, 55, 0.2)",
                showocean=True, 
                oceancolor="rgba(10, 11, 12, 0.05)",
                showlakes=True, 
                lakecolor="rgba(10, 11, 12, 0.05)",
                projection_type="orthographic",
                bgcolor='rgba(0,0,0,0)'
            )
            
            fig_map.update_layout(
                font_family="Times New Roman", 
                paper_bgcolor='rgba(0,0,0,0)', 
                margin=dict(l=0, r=0, t=0, b=0),
                coloraxis_colorbar=dict(title="Risque", thickness=15, len=0.5)
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("Aucune donnée disponible pour la cartographie.")

    with col_b:
        st.markdown("### PROFIL DE RISQUE MULTI-DIMENSIONNEL")
        if not filtered.empty:
            st.plotly_chart(render_radar_chart(filtered), use_container_width=True)
        else:
            st.info("Données insuffisantes pour le profilage de risque.")

    # Registre détaillé
    st.markdown("### REGISTRE FORENSIQUE DES TRANSACTIONS")
    if not filtered.empty:
        # Tri sécurisé
        filtered['fraud_score'] = pd.to_numeric(filtered['fraud_score'], errors='coerce').fillna(0)
        st.dataframe(
            filtered[['transaction_id', 'user_id', 'amount', 'country', 'fraud_score', 'reason']].sort_values('fraud_score', ascending=False),
            use_container_width=True,
            height=500
        )
    else:
        st.warning("Aucune transaction ne correspond aux critères forensiques sélectionnés.")

def main():
    apply_executive_style()
    
    # En-tête personnalisé
    st.markdown("""
        <div style="text-align: center; border-bottom: 2px solid #c5a059; padding-bottom: 20px; margin-bottom: 30px;">
            <h1 style="font-size: 3rem; margin: 0;">COMMANDEMENT DE L'INTÉGRITÉ FINANCIÈRE</h1>
            <p style="font-style: italic; font-size: 1.2rem; color: #666;">Surveillance de Fraude de Haut Niveau & Audit Neuronal</p>
        </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h2 style='color:white; border:none;'>PANNEAU DE CONTRÔLE</h2>", unsafe_allow_html=True)
        st.divider()
        use_sample = st.toggle("Utiliser les données d'exemple", value=True)
        
        data = []
        if use_sample:
            SAMPLE_CSV = Path(__file__).parent / "data" / "sample_transactions.csv"
            data = load_transactions(str(SAMPLE_CSV))
            st.success(f"Flux d'exemple : {len(data)} tx")
        else:
            uploaded = st.file_uploader("IMPORTER FLUX CSV", type="csv")
            if uploaded:
                tmp = Path(".upload_current.csv")
                tmp.write_bytes(uploaded.getvalue())
                data = load_transactions(str(tmp))
                st.success(f"Flux personnalisé : {len(data)} tx")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.info("Statut Système : OPÉRATIONNEL")
        st.caption("Protocole : INTELO-2026-X")

    if data:
        if st.button("AUTHENTIFIER & ANALYSER LE FLUX NEURONAL", use_container_width=True):
            with st.spinner("Traitement du flux sécurisé..."):
                results = detect_fraud(data)
                render_executive_dashboard(pd.DataFrame(data), pd.DataFrame(results))
    else:
        st.warning("En attente du flux de données sécurisé pour initialisation.")

if __name__ == "__main__":
    main()

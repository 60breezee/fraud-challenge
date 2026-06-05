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

# Référentiel géographique : ISO-2 -> (ISO-3, nom, latitude, longitude)
# Permet de convertir les codes pays pour le globe 3D et de positionner les bulles.
COUNTRY_INFO = {
    "FR": ("FRA", "France", 46.2, 2.2), "US": ("USA", "États-Unis", 37.1, -95.7),
    "JP": ("JPN", "Japon", 36.2, 138.3), "GB": ("GBR", "Royaume-Uni", 55.4, -3.4),
    "DE": ("DEU", "Allemagne", 51.2, 10.5), "ES": ("ESP", "Espagne", 40.5, -3.7),
    "IT": ("ITA", "Italie", 41.9, 12.6), "CN": ("CHN", "Chine", 35.9, 104.2),
    "RU": ("RUS", "Russie", 61.5, 105.3), "BR": ("BRA", "Brésil", -14.2, -51.9),
    "CA": ("CAN", "Canada", 56.1, -106.3), "AU": ("AUS", "Australie", -25.3, 133.8),
    "IN": ("IND", "Inde", 20.6, 78.9), "MX": ("MEX", "Mexique", 23.6, -102.5),
    "NL": ("NLD", "Pays-Bas", 52.1, 5.3), "BE": ("BEL", "Belgique", 50.5, 4.5),
    "CH": ("CHE", "Suisse", 46.8, 8.2), "SE": ("SWE", "Suède", 60.1, 18.6),
    "NO": ("NOR", "Norvège", 60.5, 8.5), "PT": ("PRT", "Portugal", 39.4, -8.2),
    "MA": ("MAR", "Maroc", 31.8, -7.1), "DZ": ("DZA", "Algérie", 28.0, 1.7),
    "TN": ("TUN", "Tunisie", 33.9, 9.5), "SN": ("SEN", "Sénégal", 14.5, -14.5),
    "CI": ("CIV", "Côte d'Ivoire", 7.5, -5.5), "NG": ("NGA", "Nigéria", 9.1, 8.7),
    "ZA": ("ZAF", "Afrique du Sud", -30.6, 22.9), "EG": ("EGY", "Égypte", 26.8, 30.8),
    "AE": ("ARE", "Émirats A. U.", 23.4, 53.8), "SA": ("SAU", "Arabie Saoudite", 23.9, 45.1),
    "TR": ("TUR", "Turquie", 38.9, 35.2), "KR": ("KOR", "Corée du Sud", 35.9, 127.8),
    "SG": ("SGP", "Singapour", 1.35, 103.8), "HK": ("HKG", "Hong Kong", 22.3, 114.2),
    "PL": ("POL", "Pologne", 51.9, 19.1), "AT": ("AUT", "Autriche", 47.5, 14.5),
    "IE": ("IRL", "Irlande", 53.4, -8.2), "DK": ("DNK", "Danemark", 56.3, 9.5),
    "FI": ("FIN", "Finlande", 61.9, 25.7), "GR": ("GRC", "Grèce", 39.1, 21.8),
    "AR": ("ARG", "Argentine", -38.4, -63.6), "CL": ("CHL", "Chili", -35.7, -71.5),
    "CO": ("COL", "Colombie", 4.6, -74.3), "TH": ("THA", "Thaïlande", 15.9, 100.9),
    "ID": ("IDN", "Indonésie", -0.8, 113.9), "MY": ("MYS", "Malaisie", 4.2, 101.9),
    "PH": ("PHL", "Philippines", 12.9, 121.8), "VN": ("VNM", "Vietnam", 14.1, 108.3),
    "IL": ("ISR", "Israël", 31.0, 34.9), "LU": ("LUX", "Luxembourg", 49.8, 6.1),
}

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

def render_3d_globe(geo_data):
    """Construit un globe terrestre 3D interactif (orthographique).

    - Choropleth : intensité = risque moyen par pays.
    - Bulles scattergeo : taille = volume de transactions, couleur = risque.
    Le rendu orthographique est rotatif à la souris (vrai effet 3D).
    """
    df = geo_data.copy()
    df = df[df["country"].notna() & (df["country"] != "")]

    # Conversion ISO-2 -> ISO-3 + coordonnées pour le positionnement des bulles.
    df["iso3"] = df["country"].map(lambda c: COUNTRY_INFO.get(str(c).upper(), (None,))[0])
    df["nom"] = df["country"].map(lambda c: COUNTRY_INFO.get(str(c).upper(), (None, str(c)))[1])
    df["lat"] = df["country"].map(lambda c: COUNTRY_INFO.get(str(c).upper(), (None, None, None, None))[2])
    df["lon"] = df["country"].map(lambda c: COUNTRY_INFO.get(str(c).upper(), (None, None, None, None))[3])

    fig = go.Figure()

    # Couche 1 : surface des pays colorée par le risque.
    geo_known = df[df["iso3"].notna()]
    if not geo_known.empty:
        fig.add_trace(go.Choropleth(
            locations=geo_known["iso3"],
            z=geo_known["Risque Moyen"],
            text=geo_known["nom"],
            colorscale=[[0, "#0d3b66"], [0.5, "#d4af37"], [1, "#dc2626"]],
            marker_line_color="rgba(212,175,55,0.5)",
            marker_line_width=0.5,
            colorbar=dict(
                title=dict(text="RISQUE", font=dict(color="#d4af37", size=12)),
                tickfont=dict(color="#e2e8f0"),
                thickness=14, len=0.55, x=0.92, bgcolor="rgba(0,0,0,0)",
            ),
            hovertemplate="<b>%{text}</b><br>Risque moyen : %{z:.2f}<extra></extra>",
        ))

    # Couche 2 : bulles de volume sur chaque pays localisé.
    geo_pts = df[df["lat"].notna()]
    if not geo_pts.empty:
        sizeref = max(geo_pts["Volume"].max(), 1) / 1600.0
        fig.add_trace(go.Scattergeo(
            lon=geo_pts["lon"], lat=geo_pts["lat"],
            text=geo_pts["nom"] + " — " + geo_pts["Volume"].astype(str) + " tx",
            marker=dict(
                size=geo_pts["Volume"], sizemode="area", sizeref=sizeref, sizemin=6,
                color=geo_pts["Risque Moyen"],
                colorscale=[[0, "#059669"], [0.5, "#d4af37"], [1, "#dc2626"]],
                cmin=0, cmax=1, opacity=0.9,
                line=dict(width=1, color="rgba(255,255,255,0.7)"),
            ),
            hovertemplate="<b>%{text}</b><extra></extra>",
            showlegend=False,
        ))

    # Style "vue depuis l'espace".
    fig.update_geos(
        projection_type="orthographic",
        projection_rotation=dict(lon=10, lat=25),
        showland=True, landcolor="#11151c",
        showocean=True, oceancolor="#05070a",
        showcountries=True, countrycolor="rgba(212,175,55,0.18)",
        showcoastlines=True, coastlinecolor="rgba(212,175,55,0.35)",
        showframe=False,
        bgcolor="rgba(0,0,0,0)",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_family="Times New Roman",
        height=520,
        margin=dict(l=0, r=0, t=10, b=0),
        dragmode="orbit",
    )
    return fig


def render_reasons_chart(merged):
    """Histogramme des principaux motifs de suspicion détectés."""
    susp = merged[merged["is_suspicious"] == True]
    if susp.empty:
        return None
    counts = susp["reason"].fillna("Non spécifié").value_counts().head(8).reset_index()
    counts.columns = ["Motif", "Occurrences"]
    fig = px.bar(
        counts.sort_values("Occurrences"), x="Occurrences", y="Motif",
        orientation="h", color="Occurrences",
        color_continuous_scale=[[0, "#d4af37"], [1, "#dc2626"]],
    )
    fig.update_layout(
        font_family="Times New Roman", paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False,
        height=520, margin=dict(l=0, r=10, t=10, b=0),
        yaxis_title=None, xaxis_title="Transactions signalées",
    )
    return fig


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
        line=dict(color='#d4af37', width=2),
        fillcolor='rgba(212, 175, 55, 0.35)'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=False,
        font_family="Times New Roman",
        paper_bgcolor='rgba(0,0,0,0)',
        height=520,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def render_executive_dashboard(df, results_df):
    merged = pd.concat([df, results_df.drop(columns=['transaction_id'])], axis=1)
    
    # Traitement des données complètes
    filtered = merged.copy()

    filtered['fraud_score'] = pd.to_numeric(filtered['fraud_score'], errors='coerce').fillna(0)

    # KPIs
    st.markdown("### INDICATEURS CLÉS D'INTELLIGENCE")
    nb_susp = int(filtered['is_suspicious'].sum())
    taux = (nb_susp / len(df) * 100) if len(df) > 0 else 0
    montant_a_risque = filtered.loc[filtered['is_suspicious'] == True, 'amount']
    montant_a_risque = pd.to_numeric(montant_a_risque, errors='coerce').fillna(0).abs().sum()

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("UNITÉS ANALYSÉES", len(df))
    k2.metric("MENACES DÉTECTÉES", nb_susp, delta=f"{taux:.0f}% du flux", delta_color="inverse")
    k3.metric("MONTANT À RISQUE", f"{montant_a_risque:,.0f}")
    k4.metric("SCORE MOYEN", f"{filtered['fraud_score'].mean():.2f}" if not filtered.empty else "0.00")
    k5.metric("INTÉGRITÉ SYSTÈME", f"{(1 - nb_susp/len(df))*100:.1f}%" if len(df) > 0 else "100%")

    st.divider()

    # Grille d'Analyse Visuelle
    col_a, col_b = st.columns([1.4, 1])

    with col_a:
        st.markdown("### 🌍 SURVEILLANCE GÉOSPATIALE GLOBALE (3D)")
        st.caption("Faites pivoter le globe à la souris. Bulles = volume · Couleur = risque.")
        if not filtered.empty:
            geo_data = filtered.groupby('country').agg({
                'fraud_score': 'mean',
                'transaction_id': 'count'
            }).reset_index()
            geo_data.columns = ['country', 'Risque Moyen', 'Volume']
            st.plotly_chart(render_3d_globe(geo_data), use_container_width=True)
        else:
            st.info("Aucune donnée disponible pour la cartographie.")

    with col_b:
        tab_radar, tab_reasons = st.tabs(["PROFIL DE RISQUE", "MOTIFS DÉTECTÉS"])
        with tab_radar:
            if not filtered.empty:
                st.plotly_chart(render_radar_chart(filtered), use_container_width=True)
            else:
                st.info("Données insuffisantes pour le profilage.")
        with tab_reasons:
            fig_reasons = render_reasons_chart(filtered) if not filtered.empty else None
            if fig_reasons is not None:
                st.plotly_chart(fig_reasons, use_container_width=True)
            else:
                st.success("Aucun motif de fraude détecté sur ce flux.")

    st.divider()

    # Registre détaillé avec mise en couleur du risque
    st.markdown("### REGISTRE FORENSIQUE DES TRANSACTIONS")
    if not filtered.empty:
        only_susp = st.toggle("Afficher uniquement les transactions suspectes", value=False)
        view = filtered.copy()
        if only_susp:
            view = view[view['is_suspicious'] == True]

        cols = ['transaction_id', 'user_id', 'amount', 'currency', 'country', 'fraud_score', 'reason']
        cols = [c for c in cols if c in view.columns]
        view = view[cols].sort_values('fraud_score', ascending=False)

        def _color_score(val):
            try:
                v = float(val)
            except (TypeError, ValueError):
                return ''
            if v >= 0.7:
                return 'background-color: #fee2e2; color: #991b1b; font-weight: bold'
            if v >= 0.4:
                return 'background-color: #fef3c7; color: #92400e; font-weight: bold'
            return 'background-color: #dcfce7; color: #166534'

        styler = view.style
        # Styler.map (pandas >= 2.1) remplace applymap (déprécié/supprimé).
        _apply_cell = getattr(styler, 'map', None) or styler.applymap
        styled = _apply_cell(_color_score, subset=['fraud_score']) \
            .format({'fraud_score': '{:.2f}', 'amount': '{:.2f}'})

        st.dataframe(styled, use_container_width=True, height=460)
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

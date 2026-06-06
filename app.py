"""
FRAUD-SHIELD — Centre de commandement de détection de fraude
Interface Streamlit moderne (thème sombre fintech) pour le hackathon INTELO2026.
"""

import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path
from fraud_detection import detect_fraud, load_transactions

st.set_page_config(
    page_title="FRAUD-SHIELD | Détection de fraude",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Palette
PRIMARY = "#6366f1"
CYAN = "#22d3ee"
SAFE = "#10b981"
WARN = "#f59e0b"
DANGER = "#ef4444"

# Référentiel géographique : ISO-2 -> (ISO-3, nom, latitude, longitude)
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


def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"], [class*="st-"] {
            font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
        }

        .stApp {
            background:
                radial-gradient(1200px 600px at 80% -10%, rgba(99,102,241,0.18), transparent 60%),
                radial-gradient(1000px 500px at 0% 0%, rgba(34,211,238,0.12), transparent 55%),
                linear-gradient(180deg, #0b1220 0%, #0a0f1c 100%);
            color: #e6edf6;
        }

        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1500px;}

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: rgba(10, 15, 28, 0.85);
            border-right: 1px solid rgba(255,255,255,0.06);
            backdrop-filter: blur(12px);
        }
        [data-testid="stSidebar"] * { color: #cdd7e6 !important; }

        h1, h2, h3, h4 { color: #f4f7fb !important; font-weight: 700 !important; letter-spacing: -0.01em; }

        /* Hero */
        .hero {
            background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(34,211,238,0.08));
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 28px 34px;
            margin-bottom: 22px;
            display: flex; align-items: center; gap: 22px;
            box-shadow: 0 20px 50px -20px rgba(99,102,241,0.5);
        }
        .hero .logo {
            font-size: 44px; line-height: 1;
            filter: drop-shadow(0 6px 14px rgba(99,102,241,0.6));
        }
        .hero h1 { margin: 0; font-size: 1.9rem; font-weight: 800; }
        .hero p { margin: 4px 0 0; color: #93a3bd; font-size: 0.98rem; }
        .live {
            margin-left: auto; display: inline-flex; align-items: center; gap: 8px;
            background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.35);
            color: #34d399 !important; padding: 8px 14px; border-radius: 999px;
            font-size: 0.8rem; font-weight: 600;
        }
        .live .dot {
            width: 9px; height: 9px; border-radius: 50%; background: #34d399;
            box-shadow: 0 0 0 0 rgba(52,211,153,0.7); animation: pulse 1.8s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(52,211,153,0.6); }
            70% { box-shadow: 0 0 0 10px rgba(52,211,153,0); }
            100% { box-shadow: 0 0 0 0 rgba(52,211,153,0); }
        }

        /* KPI cards */
        .kpi {
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px; padding: 18px 20px; height: 100%;
            transition: transform .2s ease, border-color .2s ease;
        }
        .kpi:hover { transform: translateY(-3px); border-color: rgba(99,102,241,0.5); }
        .kpi .label { font-size: 0.72rem; letter-spacing: .08em; text-transform: uppercase; color: #8b9bb4; }
        .kpi .value { font-size: 1.9rem; font-weight: 800; margin: 6px 0 2px; }
        .kpi .sub { font-size: 0.8rem; color: #93a3bd; }
        .kpi.accent { border-top: 3px solid var(--c); }

        /* Section title */
        .section { display:flex; align-items:center; gap:10px; margin: 6px 0 10px; }
        .section h3 { margin:0; font-size: 1.05rem; }
        .section .bar { width: 4px; height: 20px; border-radius: 4px;
            background: linear-gradient(180deg, #6366f1, #22d3ee); }

        /* Panel */
        .panel {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 16px; padding: 14px 16px;
        }

        /* Risk row cards */
        .riskcard {
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.08);
            border-left: 4px solid var(--c);
            border-radius: 12px; padding: 12px 14px; margin-bottom: 10px;
        }
        .riskcard .top { display:flex; justify-content:space-between; align-items:center; }
        .riskcard .tid { font-weight: 700; color:#f4f7fb; }
        .riskcard .score { font-weight: 800; color: var(--c); }
        .riskcard .reason { font-size: 0.85rem; color:#aab8cf; margin-top:4px; }
        .riskcard .meta { font-size: 0.78rem; color:#7d8db0; margin-top:2px; }

        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
            color: white !important; border: none !important;
            border-radius: 12px !important; font-weight: 700 !important;
            padding: 12px 18px !important; letter-spacing: .02em;
            box-shadow: 0 10px 24px -10px rgba(99,102,241,0.9);
            transition: transform .15s ease;
        }
        .stButton>button:hover { transform: translateY(-2px); }

        [data-testid="stMetricValue"] { color: #f4f7fb; }
        .stTabs [data-baseweb="tab-list"] { gap: 6px; }
        .stTabs [data-baseweb="tab"] {
            background: rgba(255,255,255,0.04); border-radius: 10px 10px 0 0;
            padding: 8px 14px; color:#aab8cf;
        }
        .stTabs [aria-selected="true"] { background: rgba(99,102,241,0.18); color:#fff; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label, value, sub="", color=PRIMARY):
    return f"""
    <div class="kpi accent" style="--c:{color}">
        <div class="label">{label}</div>
        <div class="value" style="color:{color}">{value}</div>
        <div class="sub">{sub}</div>
    </div>
    """


def section(title, icon=""):
    st.markdown(
        f'<div class="section"><div class="bar"></div><h3>{icon} {title}</h3></div>',
        unsafe_allow_html=True,
    )


def _dark_layout(fig, height=420):
    fig.update_layout(
        font=dict(family="Inter", color="#cdd7e6"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    return fig


def render_3d_globe(geo_data):
    """Globe terrestre 3D interactif : choropleth de risque + bulles de volume."""
    df = geo_data.copy()
    df = df[df["country"].notna() & (df["country"] != "")]
    df["iso3"] = df["country"].map(lambda c: COUNTRY_INFO.get(str(c).upper(), (None,))[0])
    df["nom"] = df["country"].map(lambda c: COUNTRY_INFO.get(str(c).upper(), (None, str(c)))[1])
    df["lat"] = df["country"].map(lambda c: COUNTRY_INFO.get(str(c).upper(), (None, None, None, None))[2])
    df["lon"] = df["country"].map(lambda c: COUNTRY_INFO.get(str(c).upper(), (None, None, None, None))[3])

    fig = go.Figure()
    geo_known = df[df["iso3"].notna()]
    if not geo_known.empty:
        fig.add_trace(go.Choropleth(
            locations=geo_known["iso3"], z=geo_known["Risque Moyen"], text=geo_known["nom"],
            colorscale=[[0, "#1e3a8a"], [0.5, "#f59e0b"], [1, "#ef4444"]],
            marker_line_color="rgba(99,102,241,0.5)", marker_line_width=0.5,
            colorbar=dict(title=dict(text="RISQUE", font=dict(color="#cdd7e6", size=11)),
                          tickfont=dict(color="#cdd7e6"), thickness=12, len=0.5, x=0.95,
                          bgcolor="rgba(0,0,0,0)"),
            hovertemplate="<b>%{text}</b><br>Risque moyen : %{z:.2f}<extra></extra>",
        ))

    geo_pts = df[df["lat"].notna()]
    if not geo_pts.empty:
        sizeref = max(geo_pts["Volume"].max(), 1) / 1600.0
        fig.add_trace(go.Scattergeo(
            lon=geo_pts["lon"], lat=geo_pts["lat"],
            text=geo_pts["nom"] + " — " + geo_pts["Volume"].astype(str) + " tx",
            marker=dict(size=geo_pts["Volume"], sizemode="area", sizeref=sizeref, sizemin=6,
                        color=geo_pts["Risque Moyen"],
                        colorscale=[[0, "#10b981"], [0.5, "#f59e0b"], [1, "#ef4444"]],
                        cmin=0, cmax=1, opacity=0.92, line=dict(width=1, color="rgba(255,255,255,0.7)")),
            hovertemplate="<b>%{text}</b><extra></extra>", showlegend=False,
        ))

    fig.update_geos(
        projection_type="orthographic", projection_rotation=dict(lon=10, lat=25),
        showland=True, landcolor="#0f1a2e", showocean=True, oceancolor="#070b14",
        showcountries=True, countrycolor="rgba(99,102,241,0.18)",
        showcoastlines=True, coastlinecolor="rgba(34,211,238,0.3)",
        showframe=False, bgcolor="rgba(0,0,0,0)",
    )
    return _dark_layout(fig, height=520)


def render_donut(nb_susp, nb_safe):
    fig = go.Figure(go.Pie(
        labels=["Suspectes", "Conformes"], values=[nb_susp, nb_safe], hole=0.68,
        marker=dict(colors=[DANGER, SAFE], line=dict(color="#0b1220", width=2)),
        textinfo="percent", textfont=dict(color="#fff", size=13), sort=False,
    ))
    total = nb_susp + nb_safe
    pct = (nb_susp / total * 100) if total else 0
    fig.update_layout(
        showlegend=True, legend=dict(orientation="h", y=-0.1, font=dict(color="#cdd7e6")),
        annotations=[dict(text=f"<b>{pct:.0f}%</b><br><span style='font-size:11px;color:#93a3bd'>à risque</span>",
                          x=0.5, y=0.5, showarrow=False, font=dict(color="#f4f7fb", size=22))],
    )
    return _dark_layout(fig, height=380)


def render_reasons_chart(merged):
    susp = merged[merged["is_suspicious"] == True]
    if susp.empty:
        return None
    counts = susp["reason"].fillna("Non spécifié").value_counts().head(8).reset_index()
    counts.columns = ["Motif", "Occurrences"]
    fig = px.bar(counts.sort_values("Occurrences"), x="Occurrences", y="Motif",
                 orientation="h", color="Occurrences",
                 color_continuous_scale=[[0, WARN], [1, DANGER]])
    fig.update_layout(coloraxis_showscale=False, yaxis_title=None,
                      xaxis_title="Transactions signalées",
                      xaxis=dict(gridcolor="rgba(255,255,255,0.06)"))
    return _dark_layout(fig, height=380)


def render_radar_chart(merged):
    categories = ['Volume', 'Score de risque', 'Géo-vélocité', 'Pic de montant', 'Fréquence']
    values = [
        len(merged) / 100,
        merged['fraud_score'].mean() * 10,
        merged[merged['reason'].str.contains('pays|géo', case=False, na=False)]['fraud_score'].count() * 2,
        merged[merged['reason'].str.contains('Montant', na=False)]['fraud_score'].count() * 2,
        merged[merged['reason'].str.contains('fréquentes', na=False)]['fraud_score'].count() * 2,
    ]
    fig = go.Figure(go.Scatterpolar(
        r=values, theta=categories, fill='toself', name='Profil de risque',
        line=dict(color=CYAN, width=2), fillcolor='rgba(34,211,238,0.25)'))
    fig.update_layout(
        polar=dict(bgcolor="rgba(255,255,255,0.02)",
                   radialaxis=dict(visible=True, range=[0, 10], gridcolor="rgba(255,255,255,0.1)",
                                   tickfont=dict(color="#8b9bb4")),
                   angularaxis=dict(tickfont=dict(color="#cdd7e6"))),
        showlegend=False)
    return _dark_layout(fig, height=380)


def render_top_risks(merged):
    susp = merged[merged["is_suspicious"] == True].sort_values("fraud_score", ascending=False).head(5)
    if susp.empty:
        st.success("✅ Aucune transaction suspecte sur ce flux — clientèle saine.")
        return
    for _, r in susp.iterrows():
        score = float(r["fraud_score"])
        c = DANGER if score >= 0.8 else (WARN if score >= 0.6 else SAFE)
        amount = r.get("amount")
        amount_str = f"{amount:,.2f} {r.get('currency','')}" if pd.notna(amount) else "—"
        st.markdown(
            f"""
            <div class="riskcard" style="--c:{c}">
                <div class="top">
                    <span class="tid">🔴 {r.get('transaction_id','?')}</span>
                    <span class="score">{score:.2f}</span>
                </div>
                <div class="reason">{r.get('reason','')}</div>
                <div class="meta">Client {r.get('user_id','?')} · {amount_str} · {r.get('country','?')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_dashboard(df, results_df, score_filter):
    merged = pd.concat([df.reset_index(drop=True),
                        results_df.drop(columns=['transaction_id']).reset_index(drop=True)], axis=1)
    merged['fraud_score'] = pd.to_numeric(merged['fraud_score'], errors='coerce').fillna(0)

    nb_total = len(merged)
    nb_susp = int(merged['is_suspicious'].sum())
    nb_safe = nb_total - nb_susp
    taux = (nb_susp / nb_total * 100) if nb_total else 0
    montant_risque = pd.to_numeric(
        merged.loc[merged['is_suspicious'] == True, 'amount'], errors='coerce'
    ).fillna(0).abs().sum()
    score_moyen = merged['fraud_score'].mean() if nb_total else 0
    integrite = (1 - nb_susp / nb_total) * 100 if nb_total else 100

    # --- KPIs ---
    section("Indicateurs clés", "📊")
    cols = st.columns(5)
    cards = [
        kpi_card("Transactions", f"{nb_total}", "analysées", CYAN),
        kpi_card("Menaces", f"{nb_susp}", f"{taux:.0f}% du flux", DANGER),
        kpi_card("Montant à risque", f"{montant_risque:,.0f}", "exposition cumulée", WARN),
        kpi_card("Score moyen", f"{score_moyen:.2f}", "sur 1.00", PRIMARY),
        kpi_card("Intégrité", f"{integrite:.1f}%", "clients sains", SAFE),
    ]
    for col, card in zip(cols, cards):
        col.markdown(card, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Globe + analyses ---
    col_a, col_b = st.columns([1.5, 1])
    with col_a:
        section("Surveillance géospatiale 3D", "🌍")
        st.caption("Faites pivoter le globe à la souris · bulles = volume · couleur = risque")
        geo_data = merged.groupby('country').agg(
            {'fraud_score': 'mean', 'transaction_id': 'count'}).reset_index()
        geo_data.columns = ['country', 'Risque Moyen', 'Volume']
        if not geo_data.empty:
            st.plotly_chart(render_3d_globe(geo_data), use_container_width=True)
        else:
            st.info("Aucune donnée géographique.")

    with col_b:
        section("Vue analytique", "🧭")
        t1, t2, t3 = st.tabs(["Répartition", "Profil", "Motifs"])
        with t1:
            st.plotly_chart(render_donut(nb_susp, nb_safe), use_container_width=True)
        with t2:
            st.plotly_chart(render_radar_chart(merged), use_container_width=True)
        with t3:
            fig_r = render_reasons_chart(merged)
            if fig_r is not None:
                st.plotly_chart(fig_r, use_container_width=True)
            else:
                st.success("Aucun motif de fraude détecté.")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Top risques + table ---
    col_t, col_d = st.columns([1, 2])
    with col_t:
        section("Top alertes", "🚨")
        render_top_risks(merged)
    with col_d:
        section("Registre forensique", "📋")
        only_susp = st.toggle("Suspectes uniquement", value=False)
        view = merged.copy()
        view = view[view['fraud_score'] >= score_filter]
        if only_susp:
            view = view[view['is_suspicious'] == True]
        wanted = ['transaction_id', 'user_id', 'amount', 'currency', 'country',
                  'fraud_score', 'is_suspicious', 'reason']
        wanted = [c for c in wanted if c in view.columns]
        view = view[wanted].sort_values('fraud_score', ascending=False)

        def _color(v):
            try:
                v = float(v)
            except (TypeError, ValueError):
                return ''
            if v >= 0.7:
                return 'background-color: rgba(239,68,68,0.22); color:#fecaca; font-weight:700'
            if v >= 0.4:
                return 'background-color: rgba(245,158,11,0.20); color:#fde68a; font-weight:700'
            return 'background-color: rgba(16,185,129,0.16); color:#bbf7d0'

        styler = view.style
        _apply_cell = getattr(styler, 'map', None) or styler.applymap
        styled = _apply_cell(_color, subset=['fraud_score']).format(
            {'fraud_score': '{:.2f}', 'amount': '{:.2f}'})
        st.dataframe(styled, use_container_width=True, height=430)

        # Export
        flagged = merged[merged['is_suspicious'] == True]
        buff = io.StringIO()
        flagged.to_csv(buff, index=False)
        st.download_button(
            "⬇️ Exporter les transactions suspectes (CSV)",
            data=buff.getvalue(),
            file_name="transactions_suspectes.csv",
            mime="text/csv",
            use_container_width=True,
            disabled=flagged.empty,
        )


def main():
    inject_css()

    st.markdown(
        """
        <div class="hero">
            <div class="logo">🛡️</div>
            <div>
                <h1>FRAUD-SHIELD</h1>
                <p>Centre de commandement — détection de fraude financière par l'IA · INTELO2026</p>
            </div>
            <div class="live"><span class="dot"></span> Système opérationnel</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown("### ⚙️ Panneau de contrôle")
        st.divider()
        use_sample = st.toggle("Utiliser les données d'exemple", value=True)

        data = []
        if use_sample:
            sample = Path(__file__).parent / "data" / "sample_transactions.csv"
            try:
                data = load_transactions(str(sample))
                st.success(f"Flux d'exemple chargé : {len(data)} transactions")
            except Exception as e:
                st.error(f"Erreur de chargement : {e}")
        else:
            uploaded = st.file_uploader("Importer un flux CSV", type="csv")
            if uploaded:
                tmp = Path(".upload_current.csv")
                tmp.write_bytes(uploaded.getvalue())
                data = load_transactions(str(tmp))
                st.success(f"Flux importé : {len(data)} transactions")

        st.divider()
        score_filter = st.slider(
            "Seuil d'affichage du risque", 0.0, 1.0, 0.0, 0.05,
            help="Filtre le registre : n'affiche que les transactions au-dessus de ce score.",
        )
        st.caption("Le moteur signale une transaction dès que son score atteint 0.60.")
        st.divider()
        st.info("Protocole : INTELO-2026-X")
        st.caption("Moteur de règles explicables · 100% local, sans boîte noire")

    if data:
        analyse = st.button("🔍 LANCER L'ANALYSE DU FLUX", use_container_width=True)
        if analyse or st.session_state.get("_analysed"):
            st.session_state["_analysed"] = True
            with st.spinner("Analyse des transactions en cours…"):
                results = detect_fraud(data)
            render_dashboard(pd.DataFrame(data), pd.DataFrame(results), score_filter)
    else:
        st.warning("⏳ En attente d'un flux de données. Activez les données d'exemple ou importez un CSV.")


if __name__ == "__main__":
    main()

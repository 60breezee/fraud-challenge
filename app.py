"""
Interface Streamlit — FRAUD-SHIELD.
Hackathon INTELO 2026.
"""

from pathlib import Path
import streamlit as st
from fraud_detection import detect_fraud, load_transactions

SAMPLE_CSV = Path(__file__).parent / "data" / "sample_transactions.csv"

def render_interface(transactions: list[dict], results: list[dict]) -> None:
    n_total = len(transactions)
    n_alert = sum(1 for r in results if r["is_suspicious"])
    n_clean = n_total - n_alert

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Analysées", n_total)
    col2.metric("Alertes", n_alert, delta_color="inverse")
    col3.metric("Légitimes", n_clean)
    col4.metric("Taux de Risque", f"{n_alert / n_total * 100:.0f}%" if n_total else "—")

    st.divider()

    merged = []
    for tx, res in zip(transactions, results):
        row = {**tx, **res}
        score = row["fraud_score"]
        if score >= 0.8:
            row["niveau"] = "Critique"
            row["couleur"] = "#dc3545"
        elif score >= 0.6:
            row["niveau"] = "Moyen"
            row["couleur"] = "#ffc107"
        else:
            row["niveau"] = "Normal"
            row["couleur"] = "#28a745"
        merged.append(row)

    tab_tout, tab_alertes, tab_detail = st.tabs([
        "📊 Flux de transactions", "🚨 Alertes de sécurité", "🔍 Analyse granulaire"
    ])

    with tab_tout:
        display = []
        for row in merged:
            display.append({
                "ID": row["transaction_id"],
                "Client": row["user_id"],
                "Montant": f'{row["amount"]:,.2f}' if row["amount"] is not None else "—",
                "Devise": row["currency"] or "—",
                "Pays": row["country"] or "—",
                "Date": (row["timestamp"][:19] if row["timestamp"] else "—"),
                "Score": row["fraud_score"],
                "Risque": row["niveau"],
                "Raison": row["reason"],
            })
        st.dataframe(display, use_container_width=True, height=500)

    with tab_alertes:
        alertes = [row for row in merged if row["is_suspicious"]]
        if not alertes:
            st.success("Aucune menace détectée dans le flux actuel.")
        else:
            for row in alertes:
                score = row["fraud_score"]
                lbl = "CRITIQUE" if score >= 0.8 else "SUSPECT"
                border = "#dc3545" if score >= 0.8 else "#ffc107"
                
                st.markdown(
                    f'<div style="background-color: #1c2128; border: 1px solid #30363d; border-left: 5px solid {border}; '
                    f'padding: 20px; border-radius: 8px; margin-bottom: 15px;">'
                    f'<div style="display:flex; justify-content:space-between; align-items:center;">'
                    f'<span style="font-size:1.2rem; font-weight:bold; color:#f0f6fc;">{row["transaction_id"]}</span>'
                    f'<span style="background:{border}; color:white; padding:2px 8px; border-radius:12px; font-size:0.8rem;">{lbl}</span>'
                    f'</div>'
                    f'<div style="margin-top:10px; color:#8b949e;">'
                    f'Client: <strong style="color:#c9d1d9;">{row["user_id"]}</strong> | '
                    f'Montant: <strong style="color:#c9d1d9;">{row["amount"]:,.2f} {row["currency"] or ""}</strong> | '
                    f'Pays: <strong style="color:#c9d1d9;">{row["country"] or "—"}</strong>'
                    f'</div>'
                    f'<div style="margin-top:15px; color:#ff7b72; font-weight:600;">'
                    f'🚩 {row["reason"]}'
                    f'</div>'
                    f'<div style="margin-top:5px; font-size:0.9rem; color:#8b949e;">'
                    f'Score de risque: {score:.2f} / 1.00'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    with tab_detail:
        ids = [r["transaction_id"] for r in results]
        choix = st.selectbox("Sélectionner une transaction pour audit :", ids)
        row = next(r for r in merged if r["transaction_id"] == choix)
        tx_orig = next(t for t in transactions if t["transaction_id"] == choix)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Données d'origine")
            st.json(tx_orig)
        with c2:
            st.subheader("Évaluation de l'IA")
            score = row["fraud_score"]
            if score >= 0.6:
                st.error(f"⚠️ Alerte confirmée ({score:.2f})")
            else:
                st.success(f"✅ Transaction validée ({score:.2f})")
            
            st.info(f"**Raison principale :** {row['reason']}")
            st.markdown(f"**Action recommandée :** {'Bloquer' if row['is_suspicious'] else 'Autoriser'}")

def main() -> None:
    st.set_page_config(
        page_title="FRAUD-SHIELD | Security Suite",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Dark Mode Styling
    st.markdown("""
        <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; }
        header, [data-testid="stSidebar"] { background-color: #161b22 !important; }
        .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
        [data-testid="stMetricValue"] { color: #58a6ff !important; }
        h1, h2, h3 { color: #f0f6fc !important; }
        .stTabs [data-baseweb="tab-list"] { gap: 10px; }
        .stTabs [data-baseweb="tab"] { 
            background-color: #161b22; border: 1px solid #30363d; border-radius: 5px 5px 0 0; color: #8b949e;
        }
        .stTabs [aria-selected="true"] { background-color: #1f6feb !important; color: white !important; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🛡️ FRAUD-SHIELD")
    st.caption("Système avancé de détection de fraude financière")

    with st.sidebar:
        st.header("Configuration")
        use_sample = st.checkbox("Flux de test (Data Sample)", value=True)
        
        if use_sample:
            transactions = load_transactions(str(SAMPLE_CSV))
            st.success(f"📡 Flux actif : {len(transactions)} tx")
        else:
            uploaded = st.file_uploader("Importer flux CSV", type=["csv"])
            if uploaded:
                tmp = Path(".upload.csv")
                tmp.write_bytes(uploaded.getvalue())
                transactions = load_transactions(str(tmp))
                st.success(f"📥 Import réussi : {len(transactions)} tx")
            else:
                transactions = []

    if transactions:
        if st.button("Lancer l'Analyse de Risque", type="primary"):
            st.session_state.results = detect_fraud(transactions)
            st.session_state.transactions = transactions
        
        if "results" in st.session_state:
            render_interface(st.session_state.transactions, st.session_state.results)
    else:
        st.info("Veuillez charger un flux de transactions pour démarrer l'analyse.")

if __name__ == "__main__":
    main()

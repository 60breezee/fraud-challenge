"""
Interface Streamlit — À CRÉER PAR VOUS pour le jury.

Le jury lancera :  streamlit run app.py

Règles :
  - Ne modifiez pas l'appel à detect_fraud / load_transactions (contrat technique).
  - Personnalisez render_interface() : clarté, intuitivité, compréhension pour un public non technique.
  - L'interface n'est PAS notée par la CI ; elle sert au jury pour repêcher et comparer les candidats.
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
    col1.metric("Transactions analysées", n_total)
    col2.metric("Alertes", n_alert, delta_color="inverse")
    col3.metric("Normales", n_clean)
    col4.metric("Taux d'alerte", f"{n_alert / n_total * 100:.0f}%" if n_total else "—")

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
        "Toutes les transactions", "Alertes uniquement", "Détail d'une transaction"
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
        st.dataframe(display, use_container_width=True, height=400,
                     column_order=["ID", "Client", "Montant", "Devise", "Pays",
                                   "Date", "Score", "Risque", "Raison"])

    with tab_alertes:
        alertes = [row for row in merged if row["is_suspicious"]]
        if not alertes:
            st.success("Aucune transaction suspecte détectée.")
        else:
            for row in alertes:
                score = row["fraud_score"]
                if score >= 0.8:
                    bg = "#f8d7da"
                    border = "#dc3545"
                    lbl = "CRITIQUE"
                else:
                    bg = "#fff3cd"
                    border = "#ffc107"
                    lbl = "ATTENTION"
                st.markdown(
                    f'<div class="fraud-card">'
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
        choix = st.selectbox("Choisissez une transaction :", ids)
        row = next(r for r in merged if r["transaction_id"] == choix)
        tx_orig = next(t for t in transactions if t["transaction_id"] == choix)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Transaction**")
            st.write(f'ID : `{tx_orig["transaction_id"]}`')
            st.write(f'Client : `{tx_orig["user_id"]}`')
            st.write(f'Montant : {tx_orig["amount"]:,.2f} {tx_orig["currency"] or ""}'
                     if tx_orig["amount"] is not None else "Montant : —")
            st.write(f'Pays : {tx_orig["country"] or "—"}')
            st.write(f'Commerçant : {tx_orig["merchant"] or "—"}')
            st.write(f'Date : {tx_orig["timestamp"][:19] if tx_orig["timestamp"] else "—"}')
            st.write(f'Carte présente : {"Oui" if tx_orig["card_present"] else "Non"}'
                     if tx_orig["card_present"] is not None else "Carte présente : —")
        with c2:
            st.markdown("**Verdict**")
            score = row["fraud_score"]
            if score == 0:
                st.success("✅ Transaction normale")
            elif score < 0.6:
                st.warning("⚠️ Légèrement atypique")
            else:
                st.error("🚨 Transaction suspecte")
            st.progress(score, text=f"Score de risque : {score:.2f}")
            st.write(f'Raison : _{row["reason"]}_')

            avec_signal = row["is_suspicious"]
            st.write(
                f'Décision : **{"SUSPENDRE" if avec_signal else "AUTORISER"}** la transaction'
            )

        if tx_orig["user_id"]:
            st.divider()
            st.markdown("**Transactions du même client**")
            memes = [t for t, r in zip(transactions, results)
                     if t["user_id"] == tx_orig["user_id"]]
            for m in memes:
                res_m = next(r for r in results if r["transaction_id"] == m["transaction_id"])
                flag = "🚨" if res_m["is_suspicious"] else "✅"
                st.write(
                    f'{flag} `{m["transaction_id"]}`'
                    f' — {m["amount"]:,.2f} {m["currency"] or ""}'
                    f' — {m["country"] or "—"}'
                    f' — {m["timestamp"][:19] if m["timestamp"] else "—"}'
                )
            st.caption("Contexte : l'IA compare chaque transaction à l'historique du client pour décider.")


def main() -> None:
    st.set_page_config(
        page_title="Détection de fraude — Hackathon INTELO2026",
        page_icon="🛡️",
        layout="wide",
    )

    st.title("Détection de fraude financière")
    st.caption("Hackathon INTELO2026 — interface participant · évaluée par le jury")

    with st.sidebar:
        st.header("Charger des données")
        use_sample = st.checkbox("Utiliser le fichier d'exemple", value=True)
        transactions: list[dict] = []

        if use_sample:
            transactions = load_transactions(str(SAMPLE_CSV))
            st.success(f"{len(transactions)} transactions (exemple)")
        else:
            uploaded = st.file_uploader("Importer un CSV", type=["csv"])
            if uploaded:
                tmp = Path(".streamlit_upload.csv")
                tmp.write_bytes(uploaded.getvalue())
                transactions = load_transactions(str(tmp))
                tmp.unlink(missing_ok=True)
                st.success(f"{len(transactions)} transactions importées")

        st.divider()
        st.markdown(
            "**Jury :** évaluez l'ergonomie et la clarté de l'écran principal, "
            "pas seulement le score des tests."
        )

    if not transactions:
        st.info("Chargez des transactions (barre latérale) puis lancez l'analyse.")
        return

    if st.button("Analyser", type="primary"):
        try:
            st.session_state.results = detect_fraud(transactions)
            st.session_state.transactions = transactions
        except NotImplementedError:
            st.error("Implémentez d'abord `detect_fraud` dans `fraud_detection.py`.")
            st.session_state.pop("results", None)
            return
        except Exception as exc:
            st.error(f"Erreur : {exc}")
            st.session_state.pop("results", None)
            return

    if "results" in st.session_state and "transactions" in st.session_state:
        try:
            render_interface(st.session_state.transactions, st.session_state.results)
        except Exception as exc:
            st.error(f"Erreur dans l'interface : {exc}")
            import traceback
            st.code(traceback.format_exc())


if __name__ == "__main__":
    main()

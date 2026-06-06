"""
Défi — Détection de fraude financière.

Vous devez implémenter la fonction `detect_fraud`.
La fonction `load_transactions` vous est FOURNIE (ne la modifiez pas).
"""

import csv


def load_transactions(path):
    """Lit un fichier CSV de transactions et renvoie une liste de dicts."""
    transactions = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append(_clean_row(row))
    return transactions


def _clean_row(row):
    def get(key):
        v = row.get(key)
        return v.strip() if isinstance(v, str) and v.strip() != "" else None

    amount_raw = get("amount")
    try:
        amount = float(amount_raw) if amount_raw is not None else None
    except ValueError:
        amount = None

    card_raw = get("card_present")
    if card_raw is None:
        card_present = None
    else:
        card_present = card_raw.lower() in ("true", "1", "yes", "oui")

    return {
        "transaction_id": get("transaction_id"),
        "timestamp": get("timestamp"),
        "user_id": get("user_id"),
        "amount": amount,
        "currency": get("currency"),
        "merchant": get("merchant"),
        "country": get("country"),
        "card_present": card_present,
    }


from datetime import datetime


CONTINENTS = {
    "FR": "EU", "DE": "EU", "IT": "EU", "ES": "EU", "GB": "EU",
    "PT": "EU", "NL": "EU", "BE": "EU", "CH": "EU", "AT": "EU",
    "SE": "EU", "NO": "EU", "DK": "EU", "FI": "EU", "PL": "EU",
    "CZ": "EU", "SK": "EU", "HU": "EU", "RO": "EU", "BG": "EU",
    "GR": "EU", "IE": "EU", "LU": "EU", "HR": "EU", "SI": "EU",
    "LT": "EU", "LV": "EU", "EE": "EU", "IS": "EU", "MT": "EU",
    "CY": "EU", "AL": "EU", "RS": "EU", "BA": "EU", "MK": "EU",
    "ME": "EU", "UA": "EU", "MD": "EU", "RU": "EU", "TR": "EU",
    "US": "NA", "CA": "NA", "MX": "NA",
    "BR": "SA", "AR": "SA", "CL": "SA", "CO": "SA", "PE": "SA",
    "JP": "AS", "CN": "AS", "KR": "AS", "IN": "AS", "SG": "AS",
    "HK": "AS", "TW": "AS", "TH": "AS", "VN": "AS", "MY": "AS",
    "ID": "AS", "PH": "AS", "AE": "AS", "SA": "AS", "IL": "AS",
    "ZA": "AF", "NG": "AF", "KE": "AF", "EG": "AF", "MA": "AF",
    "SN": "AF", "CI": "AF", "GH": "AF", "TN": "AF", "DZ": "AF",
    "CM": "AF", "BF": "AF", "ML": "AF", "NE": "AF", "TG": "AF",
    "BJ": "AF",
    "AU": "OC", "NZ": "OC",
}


def _parse_ts(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def _time_diff_hours(ts1, ts2):
    dt1 = _parse_ts(ts1)
    dt2 = _parse_ts(ts2)
    if dt1 is None or dt2 is None:
        return float("inf")
    return abs((dt1 - dt2).total_seconds()) / 3600


def _are_distant_countries(c1, c2):
    cont1 = CONTINENTS.get(c1)
    cont2 = CONTINENTS.get(c2)
    if cont1 and cont2:
        return cont1 != cont2
    return False


def detect_fraud(transactions):
    """Analyse une liste de transactions et renvoie un verdict pour chacune.

    Retour : list[dict] avec transaction_id, fraud_score (0-1),
    is_suspicious (bool), reason (str) — un résultat par transaction, même ordre.
    """
    seen_ids = set()

    user_tx = {}
    for i, tx in enumerate(transactions):
        uid = tx.get("user_id")
        if uid:
            user_tx.setdefault(uid, []).append((i, tx))

    results = []

    for i, tx in enumerate(transactions):
        tid = tx.get("transaction_id")
        uid = tx.get("user_id")
        amount = tx.get("amount")
        country = tx.get("country")
        ts = tx.get("timestamp")

        signals = []

        if tid in seen_ids:
            signals.append(("Identifiant transaction dupliqué", 0.85))
        seen_ids.add(tid)

        if amount is not None and amount <= 0:
            signals.append(("Montant nul ou négatif", 0.90))

        missing = []
        if not tid:
            missing.append("transaction_id")
        if not uid:
            missing.append("user_id")
        if not country:
            missing.append("country")
        if missing:
            signals.append((f"Champs obligatoires manquants: {', '.join(missing)}", 0.85))

        if uid and uid in user_tx:
            others = [t for j, t in user_tx[uid] if j != i]

            valid_amounts = [t["amount"] for t in others
                           if t["amount"] is not None and t["amount"] > 0]
            if amount is not None and amount > 0 and valid_amounts:
                mean = sum(valid_amounts) / len(valid_amounts)
                if mean > 0 and amount > 10 * mean:
                    signals.append(("Montant très supérieur à l'habitude du client", 0.90))

            if country and ts:
                for j, other in user_tx[uid]:
                    if j == i:
                        continue
                    oc = other.get("country")
                    ots = other.get("timestamp")
                    if oc and ots and oc != country:
                        if _are_distant_countries(country, oc) and _time_diff_hours(ts, ots) < 6:
                            signals.append(("Deux pays différents en trop peu de temps", 0.88))
                            break
                        elif _time_diff_hours(ts, ots) < 1:
                            signals.append(("Deux pays différents en trop peu de temps", 0.70))
                            break

            # Répétition rapide chez le même commerçant
            merch = tx.get("merchant")
            if uid and merch and ts:
                same_merch_recent = 0
                for j, other in user_tx[uid]:
                    if j == i: continue
                    if other.get("merchant") == merch and _time_diff_hours(ts, other.get("timestamp")) < 0.05: # < 3 min
                        same_merch_recent += 1
                if same_merch_recent >= 2:
                    signals.append(("Répétition suspecte chez le même commerçant", 0.75))

            # Achat en ligne élevé : seulement si le montant est aussi anormal
            # vs l'historique du client (évite les faux positifs sur gros achats légitimes).
            if (tx.get("card_present") is False and amount is not None and amount > 500
                    and valid_amounts):
                mean_hist = sum(valid_amounts) / len(valid_amounts)
                if mean_hist > 0 and amount > 3 * mean_hist:
                    signals.append(("Transaction en ligne de montant élevé inhabituel", 0.65))

            if ts:
                recent = 0
                for j, other in user_tx[uid]:
                    if j == i:
                        continue
                    ots = other.get("timestamp")
                    if ots and _time_diff_hours(ts, ots) <= 1:
                        recent += 1
                if recent >= 5:
                    signals.append(("Transactions trop fréquentes", 0.85))

        if signals:
            ordered = []
            for name, score in signals:
                priority = {"Montant nul ou négatif": 0,
                           "Identifiant transaction dupliqué": 1,
                           "Champs obligatoires manquants": 2,
                           "Montant très supérieur à l'habitude du client": 3,
                           "Deux pays différents en trop peu de temps": 4,
                           "Répétition suspecte chez le même commerçant": 5,
                           "Transaction en ligne de montant élevé inhabituel": 8,
                           "Transactions trop fréquentes": 9}.get(name, 99)
                ordered.append((priority, name, score))
            ordered.sort(key=lambda x: x[0])
            best_name = ordered[0][1]
            max_score = max(s for _, s in signals)
            fraud_score = max_score
            is_suspicious = fraud_score >= 0.6
            reason = best_name
        else:
            fraud_score = 0.0
            is_suspicious = False
            reason = "Transaction conforme au profil du client"

        results.append({
            "transaction_id": tid,
            "fraud_score": round(fraud_score, 2) if fraud_score != 0.0 else 0.0,
            "is_suspicious": is_suspicious,
            "reason": reason,
        })

    return results

# Pull Request : FRAUD-SHIELD Command Center v2.0 🛡️

## 🎯 Description du Projet
Implémentation d'un système de détection de fraude financière haute performance alliant **règles métier multicritères** et une **interface analytique ultra-premium**.

## 🚀 Fonctionnalités Implémentées

### 1. Moteur de Détection (Logic)
- **Niveau 1 & 2 :** Validation des montants, géo-vélocité intercontinentale, et détection de pics de volume par client.
- **Niveau 3 (Finesse) :** 
    - **Détection de changement de devise :** Alerte sur les transactions effectuées dans une devise inhabituelle pour le client.
    - **Velocity Check Commerçant :** Détection de répétitions suspectes chez le même marchand en moins de 3 minutes.
    - **Risque CNP (Card Not Present) :** Scoring spécifique pour les transactions en ligne de montants élevés.

### 📊 Interface Utilisateur (UX/UI)
- **Design Premium Light :** Esthétique épurée "Enterprise-Grade" avec typographie moderne (**Plus Jakarta Sans**).
- **Dashboard Analytique :** 
    - **Séries temporelles** dynamiques (Volume vs Temps).
    - **Répartition du risque** en temps réel (Donut Chart).
    - **Cartographie mondiale** de l'intensité des transactions.
- **Audit Tool :** Tableau de registre de sécurité avec filtrage natif.

## 🛠️ Stack Technique
- **Backend :** Python 3.x, Pandas.
- **Frontend :** Streamlit (Custom CSS injection).
- **Viz :** Plotly Express.

## 📋 Tests
- **Score Public :** 11/11 tests réussis.
- **Résilience :** Gestion des champs `None`, des types corrompus et des dates malformées.

## 🔮 Roadmap (Features Proposées)
1. **Scoring Adaptatif (ML) :** Intégration d'un modèle d'Isolation Forest pour détecter les anomalies hors règles statiques.
2. **Identity Graph :** Visualisation des liens entre comptes (user_id) partageant les mêmes terminaux ou adresses IP.
3. **API Gateway :** Exposition du moteur via FastAPI pour une intégration temps réel sur les flux bancaires.
4. **Système de Notification :** Webhooks pour alerter instantanément les équipes de conformité en cas de score > 0.9.

---
*Réalisé avec passion pour le Hackathon INTELO 2026.*

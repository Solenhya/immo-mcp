# 🏠 Immo-MCP : Agent IA Immobilier Professionnel

Ce projet implémente un système d'intelligence artificielle spécialisé dans l'immobilier. Il utilise l'architecture **MCP (Model Context Protocol)** pour connecter un agent intelligent à un moteur de prédiction de prix basé sur du **Machine Learning réel**.

---

## 🏗️ Architecture du Projet

Le système est découplé en deux composants principaux :

1.  **Le Serveur MCP (`src/server.py`)** : 
    *   Développé avec `FastMCP`. 
    *   **Moteur ML** : Charge dynamiquement un modèle `scikit-learn` (.joblib) depuis **Hugging Face**.
    *   **Outil** : Expose `predict_price` pour calculer des estimations en temps réel.
    *   **Conteneurisation** : Déployé sur un cluster **K3S** via Docker.

2.  **L'Agent IA (`langchain_manager.py`)** : 
    *   Développé avec `LangChain` et `LangGraph`. 
    *   **Cerveau** : Utilise `Mistral AI` (mistral-large-latest).
    *   **Fonctionnement** : Communique avec le serveur distant via **SSE (Server-Sent Events)** pour utiliser les outils de prédiction.

---

## 💻 Développement et Test Local

### 1. Prérequis
*   [uv](https://github.com/astral-sh/uv) (gestionnaire Python ultra-rapide)
*   Docker Desktop (pour le serveur)
*   Clés API dans un fichier `.env` (`MISTRAL_API_KEY`, `HF_USERNAME`, `HF_REPO`, `HF_TOKEN`)

### 2. Lancement du Serveur (Remote ou Local)
Pour tester l'agent localement avec le serveur déployé sur le Datalab :
```bash
# Établir un tunnel SSH sécurisé
ssh -L 8080:localhost:8080 p4g2@datalab.myconnectech.fr

# (Sur le serveur distant) Lancer le port-forward Kubernetes
kubectl port-forward -n g2 service/immo-mcp-service 8080:80
```

### 3. Lancement de l'Agent
```bash
uv run langchain_manager.py
```

---

## ☸️ Déploiement Kubernetes (K3S)

L'infrastructure est automatisée via une chaîne **CI/CD (GitHub Actions)** :
1.  **Build** : L'image est construite et poussée sur **GHCR** (`ghcr.io/solenhya/immo-mcp`).
2.  **Secrets** : Configuration des accès via `ghcr-auth` et `immo-env`.
3.  **Service** : Déploiement via `deployment.yaml` avec une stratégie de `rollout` automatique.

```bash
# Commande pour redéployer après modification du code
kubectl rollout restart deployment/immo-mcp-server -n g2
```

---

## 📊 Capacités de l'Outil de Prédiction
L'outil `predict_price` prend en compte :
*   `surface_reelle_bati` : Surface du logement.
*   `surface_terrain` : Surface du terrain (jardin, etc.).
*   `nombre_pieces_principales` : Nombre de pièces.
*   `type_local` : Maison ou Appartement.

---

## 🚀 Évolutions Possibles (Roadmap)
*   **Géolocalisation** : Intégrer les coordonnées GPS pour des prix plus précis par quartier.
*   **Historique DVF** : Ajout d'un outil de recherche automatique sur les dernières ventes réelles.
*   **Interface Web** : Création d'un tableau de bord avec Streamlit.

---

## 📝 Auteur
Développé par **Arno / Solenhya** - Expertise Immobilière & IA (Datalab).

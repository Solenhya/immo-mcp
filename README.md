# Immo-MCP : Agent IA Immobilier Professionnel

Ce projet implémente un agent d'intelligence artificielle spécialisé dans l'immobilier, utilisant l'architecture **MCP (Model Context Protocol)** pour séparer l'intelligence (l'Agent) des outils métiers (le Serveur).

## 🏗️ Architecture du Projet

Le projet est divisé en deux composants principaux :

1.  **Le Serveur MCP (`server.py`)** : Développé avec `FastMCP`. C'est la "boîte à outils" qui contient les fonctions métiers (calculs, accès base de données DVF). Il tourne dans un conteneur Docker.
2.  **L'Agent IA (`langchain_manager.py`)** : Développé avec `LangChain` et `LangGraph`. C'est le cerveau qui utilise Mistral AI pour comprendre les demandes de l'utilisateur et appeler les outils du serveur.

---

## 💻 Développement Local

### Prérequis
*   [uv](https://github.com/astral-sh/uv) (gestionnaire de paquets Python)
*   Docker Desktop
*   Un fichier `.env` avec vos clés API (`MISTRAL_API_KEY`, etc.)

### Lancement du Serveur (Outils)
Vous pouvez lancer le serveur directement ou via Docker :

**Via Docker (recommandé) :**
```bash
docker build -t immo-mcp-server .
docker run -p 8000:8000 --env-file .env immo-mcp-server
```
Le serveur sera accessible sur `http://localhost:8000/sse`.

### Lancement de l'Agent (Cerveau)
Dans un autre terminal :
```bash
uv run langchain_manager.py
```

---

## 🚀 CI/CD et Docker Registry

Le projet est configuré pour se construire automatiquement via **GitHub Actions**.
*   **Workflow** : À chaque `push` sur la branche `main` ou `kubernetes`, GitHub construit l'image Docker.
*   **Registre** : L'image est stockée sur **GitHub Container Registry (GHCR)** à l'adresse `ghcr.io/solenhya/immo-mcp`.

---

## ☸️ Déploiement Kubernetes (K3S)

Le déploiement s'effectue sur le cluster K3S du Datalab.

### 1. Configuration initiale (Secrets)
Avant de déployer, il faut créer les secrets dans le namespace (`g2` par exemple) :

```bash
# Accès au registre GitHub (nécessite un Personal Access Token)
kubectl create secret docker-registry ghcr-auth \
  --docker-server=ghcr.io \
  --docker-username=VOTRE_PSEUDO \
  --docker-password=VOTRE_TOKEN \
  -n g2

# Variables d'environnement (Clés API)
kubectl create secret generic immo-env --from-env-file=.env -n g2
```

### 2. Déploiement
Appliquez le fichier de configuration :
```bash
kubectl apply -f deployment.yaml
```

### 3. Vérification
```bash
# Voir l'état du serveur
kubectl get pods -n g2

# Voir les logs en direct
kubectl logs -f deployment/immo-mcp-server -n g2
```

---

## 🛠️ Structure des Outils
Les outils sont définis dans `server.py` avec le décorateur `@mcp.tool`. 
Exemple :
```python
@mcp.tool
def add(a: int, b: int) -> str:
    """Additionne deux nombres"""
    return f"{a + b}"
```

---

## 🚀 Améliorations Futures (Roadmap)

Pour faire évoluer ce projet, plusieurs pistes sont envisageables :
1.  **Multi-modèles** : Intégrer d'autres modèles Hugging Face spécialisés par région ou par type de bien (Appartements vs Maisons).
2.  **Interface Web** : Ajouter un front-end (React ou Streamlit) pour rendre l'agent accessible à des utilisateurs non techniques.
3.  **Persistance** : Ajouter une base de données (PostgreSQL) dans le cluster pour mémoriser les estimations passées de chaque utilisateur.
4.  **Monitoring** : Installer Grafana pour visualiser en temps réel la charge du serveur et le nombre de requêtes traitées.

---

## 📝 Auteur
Développé dans le cadre du projet immo-mcp - Expertise Immobilière & IA.

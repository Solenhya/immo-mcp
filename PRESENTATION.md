# Soutenance Technique : Agent IA Immo-MCP

Ce document détaille les justifications techniques et l'analyse des résultats du projet pour la présentation finale.

---

## 🎤 1. Démonstration de l'Application

Le flux de démonstration recommandé est le suivant :
1.  **Vérification Cluster** : Montrer que le pod tourne sur le Datalab (`kubectl get pods -n g2`).
2.  **Lancement Agent** : Lancer `langchain_manager.py` localement.
3.  **Appel Outils** : Demander à l'IA d'additionner deux nombres ou d'estimer un bien pour prouver que l'IA communique bien avec le serveur distant.
4.  **Logs temps réel** : Afficher les logs du serveur en même temps pour montrer les requêtes qui arrivent sur le cluster.

---

## ⚙️ 2. Justification des Choix Techniques

### Pourquoi FastMCP ?
*   **Standardisation** : MCP est le nouveau standard (Open Source) d'Anthropic pour connecter des IA à des outils. Choisir MCP, c'est choisir une technologie d'avenir.
*   **Séparation des responsabilités** : Le serveur contient la logique métier (calculs, accès base de données), tandis que l'agent contient l'intelligence. Cela permet de mettre à jour les outils sans toucher au cerveau de l'IA.
*   **Rapidité de développement** : FastMCP permet d'exposer des fonctions Python en outils IA en seulement 2 lignes de code (décorateur `@mcp.tool`).
*   **Protocoles modernes** : L'utilisation de **SSE (Server-Sent Events)** permet une communication fluide et temps réel entre l'agent et le serveur.

---

## 📊 3. Analyse des Résultats

### Utilisation des outils par l'Agent
L'agent (LangChain) parvient-il à utiliser les outils ? **Oui.**
*   L'agent analyse l'intention de l'utilisateur. S'il détecte un besoin de calcul ou d'estimation, il génère une requête structurée vers le serveur MCP.
*   La boucle de feedback est courte : l'agent reçoit le résultat, l'interprète et le restitue en langage naturel.

### Cohérence avec les données DVF
*   Le modèle hébergé sur Hugging Face a été entraîné sur les données réelles de la DVF (Demandes de Valeurs Foncières).
*   En interrogeant l'outil `estimer_prix`, l'agent fournit des estimations basées sur l'historique réel des ventes, garantissant une meilleure précision qu'une simple supposition de l'IA.

---

## 🚀 4. Pistes d'Amélioration

Pour aller plus loin dans l'expertise immobilière, nous pourrions ajouter les outils suivants :
1.  **Outil de Géolocalisation** : Transformer une adresse textuelle en coordonnées GPS pour affiner la recherche DVF.
2.  **Outil de Comparaison** : Un outil qui cherche les 5 biens les plus similaires vendus dans un rayon de 500m.
3.  **Outil de Diagnostic** : Une fonction qui calcule automatiquement le rendement locatif brut en fonction du prix d'achat et des loyers moyens du quartier.
4.  **Analyse de Marché** : Un outil qui extrait les tendances de prix (hausse/baisse) sur les 2 dernières années pour une ville donnée.

---

## 🛠️ Stack Technique Récapitulative
*   **Langage** : Python 3.12 (gestion via `uv`).
*   **Cerveau** : Mistral AI via LangChain / LangGraph.
*   **Outils** : FastMCP.
*   **Infrastructure** : Docker, GitHub Container Registry (GHCR), K3S (Kubernetes).
*   **Modèle ML** : Scikit-learn, hébergé sur Hugging Face.

# Diagnostic d'incidents DCO

Application Streamlit pour analyser des logs serveur bruts avec le SDK officiel Mistral.

## Architecture

Flux applicatif (version simplifiee) :

1. User: saisit ou colle des logs dans l'interface Streamlit.
2. Streamlit (`app.py`): nettoie la demande, construit le prompt et appelle le SDK Mistral.
3. Docker: encapsule l'application et ses dependances pour une execution reproductible.
4. Mistral API: genere le diagnostic (criticite, resume technique, plan d'action) retourne a l'UI.

Representation rapide :

`User -> Streamlit -> Docker -> Mistral API`

## Choix Technologiques

### Pourquoi Mistral

- Souverainete: acteur europeen, pertinent pour des contextes d'hebergement et de conformite en Europe.
- RGPD: facilite une posture de conformite en limitant les risques de transferts de donnees hors cadre attendu.
- Qualite de generation: suffisamment robuste pour produire des analyses techniques structurees sur des logs.

### Pourquoi Docker

- Portabilite: meme image entre poste local, CI/CD et environnement de production.
- Standard OVH: alignement avec des pratiques de deploiement cloud basees sur des conteneurs.
- Fiabilite operationnelle: reduction des ecarts "ca marche chez moi" via un environnement fige.

## Variables d'environnement

Créer un fichier `.env` avec:

```env
MISTRAL_API_KEY=your_key_here
```

## Lancement local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Lancement Docker

```bash
docker compose up --build
```

## Déploiement Portainer

### Déploiement manuel local

Importer `docker-compose.yml` comme Stack, puis définir `MISTRAL_API_KEY` dans l'environnement de la stack.

### Déploiement automatisé via GHCR

Voir [DEPLOYMENT_GHCR.md](DEPLOYMENT_GHCR.md) pour la configuration de la pipeline GitHub Actions avec déploiement automatique vers GHCR et webhook Portainer.

## Sortie attendue

- Criticité: CRITIQUE, MAJEUR, MINEUR ou INFO
- Résumé technique: 2 phrases maximum
- Plan d'action: 3 étapes

## Ameliorations futures

- Cache Redis: memoriser les analyses de logs similaires pour reduire latence et cout API.
- Monitoring Prometheus/Grafana: exposer des metriques (latence, taux d'erreur, volume de requetes) et des dashboards d'exploitation.
- Queue asynchrone: decoupler l'analyse (ex: Celery/RQ) pour absorber des pics de charge.
- Guardrails de prompt: renforcer la robustesse des sorties avec validation de schema et fallback en cas de reponse invalide.
- Industrialisation: pipeline CI avec tests automatiques, scan securite image, et versionnement semantique des releases.

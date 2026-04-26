# Diagnostic d'incidents DCO

Application Streamlit pour analyser des logs serveur bruts avec le SDK officiel Mistral.

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

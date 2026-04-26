# Pipeline de déploiement GHCR + Portainer

## Configuration requise

### 1. Secrets GitHub

Ajouter dans les **Repository Secrets** (Settings > Secrets and variables > Actions):

- `PORTAINER_WEBHOOK`: URL du webhook Portainer pour déclencher le redéploiement automatique.
  - Format: `https://portainer.example.com/api/webhooks/xxxxx`

### 2. Authentification GHCR

La pipeline utilise automatiquement `${{ secrets.GITHUB_TOKEN }}` fourni par GitHub Actions pour l'authentification GHCR. Aucune configuration supplémentaire requise.

### 3. Configuration Docker Buildx

Le workflow supporte les architectures multi-plateformes:
- `linux/amd64` (serveurs x86-64)
- `linux/arm64` (Raspberry Pi, ARM servers)

Pour restreindre à une seule plateforme, remplacer dans le workflow:
```yaml
platforms: linux/amd64
```

## Flux de déploiement

1. **Push sur main** → GitHub Actions démarre automatiquement
2. **Build** → Docker Buildx compile l'image pour AMD64 et ARM64
3. **Push** → Image taguée `latest` et SHA court vers GHCR
4. **Webhook Portainer** → Déclenche le redéploiement de la stack

## Tags générés

- `ghcr.io/your-org/dco-incident-diagnostic:latest` (branche main)
- `ghcr.io/your-org/dco-incident-diagnostic:sha-xxxxx` (commit SHA)

## Configuration Portainer

1. Accéder à **Portainer > Stacks**
2. Créer une nouvelle stack ou éditer l'existante
3. Utiliser l'image: `ghcr.io/your-org/dco-incident-diagnostic:latest`
4. Ajouter le webhook pour le redéploiement automatique:
   - **Settings > Webhooks**
   - Copier l'URL du webhook dans **Repository Secrets** (voir point 1)

## Variables d'environnement Portainer

Définir dans la stack Portainer:
```yaml
environment:
  - MISTRAL_API_KEY=your_key_here
```

Ne pas utiliser `env_file: .env` dans Portainer, car le fichier local n'est pas résolu dans le dossier interne `/data/compose/...`.

## Dépannage

- **Erreur d'authentification GHCR**: Vérifier les permissions du repository (Settings > Actions > General).
- **Webhook Portainer ne se déclenche pas**: Vérifier l'URL du secret `PORTAINER_WEBHOOK`.
- **Image non trouvable dans Portainer**: Authentifier Portainer vers GHCR via **Settings > Registries**.

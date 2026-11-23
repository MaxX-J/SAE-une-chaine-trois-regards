# Règles de travail

## Branches

`main` est protégée : toute modification passe par une pull request.

| Préfixe | Usage |
|---|---|
| `docs/` | Documentation et rendus |
| `feat/` | Fonctionnalité |
| `fix/` | Correction |
| `chore/` | Configuration, maintenance |

Exemple : `docs/spec-validite`.

## Commits

Format [Conventional Commits](https://www.conventionalcommits.org/fr/), en français :

```text
docs(spec): définir la validité d'un bloc
feat(noeud): valider les messages reçus
```

## Pull requests

1. Partir de `main` à jour et garder une PR par sujet.
2. Demander une relecture à l'autre membre du binôme.
3. Fusionner en squash, la branche est supprimée automatiquement.

La spec engage les six. Les modalités de modification après le 26/11 sont à définir dans son thème 11.

## Secrets

Ce dépôt est **public**. Les clés Tailscale et OpenRouter restent dans un `.env` local. Une clé publiée par erreur doit être révoquée immédiatement : la supprimer du fichier ne suffit pas.

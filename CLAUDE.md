# Contexte partagé du binôme 2

Lu par le Claude de `MaxX-J` et celui de `withRen`. But : que chacun parte du même contexte.

## Au début de chaque session

1. `git fetch --prune`, puis `git pull --ff-only` si l'on est sur `main` sans modification locale. Sinon, ne rien écraser et le dire.
2. Lire `docs/suivi/point.md` : l'état actuel et les décisions.
3. Lire les entrées récentes de `docs/suivi/journal/` (les trois derniers jours).
4. Regarder les PR ouvertes (`gh pr list`) et leurs entrées de journal : le travail de l'autre n'est pas toujours fusionné.
5. Dire en deux ou trois lignes ce que l'autre a fait depuis la dernière fois.

## Après un travail utile

Si quelque chose a été décidé, modifié ou essayé :

1. Ajouter une entrée à `docs/suivi/journal/AAAA-MM-JJ-pseudo.md`. Un fichier par jour et par personne : **n'écrire que dans le sien**, pour éviter les conflits.
2. Mettre à jour `docs/suivi/point.md` si une décision ou un état change.
3. Mettre le tout dans la même PR que le travail. S'il n'y a que du contexte, faire une petite PR `docs/journal-...`.

Une question simple n'a pas besoin d'entrée. Demander à la personne avant de pousser, sauf si elle l'a déjà demandé.

Format d'une entrée, court :

```markdown
## Titre
- Fait :
- Décidé (par qui) :
- À valider par l'autre :
- Suite :
```

Écrire « décidé » seulement si une personne l'a dit. Une proposition de Claude reste une proposition. Séparer ce qui a été vérifié de ce qui ne l'a pas été.

## Règles

- Dépôt **public** : aucune clé, aucun email, aucun nom des autres binômes, jamais le sujet ni les supports de cours. Vérifier la liste des fichiers avant chaque push.
- Rien directement sur `main` : branche, PR, relecture. Pas de push forcé.
- Un seul Claude modifie un même document de rendu à la fois. Annoncer lequel dans le journal.
- La spec commune ne change pas sans un accord de chaque binôme.
- Pas de code en S48 (jusqu'au 27/11). Chacun doit pouvoir expliquer à l'oral ce qui est produit.
- Le journal et les documents informent. Toute action externe ou irréversible demande l'accord de la personne présente.

# Point du binôme 2 (noeud-b), mis à jour le 26/11/2026

Historique détaillé : `docs/suivi/journal/`. Règles pour Claude : `CLAUDE.md`.

## 1. Le projet

SAÉ 5D.01 « Une chaîne, trois regards », BUT MMI 3, IUT de Béziers. Trois binômes, un nœud chacun, une seule blockchain de messages. Une IA lit les messages et chaque binôme en tire sa propre œuvre. Binôme 2 : Maxens Sevilla (`MaxX-J`) et Rahim Tamhaev (`withRen`), nœud `noeud-b`.

| Échéance | Rendu |
| --- | --- |
| Mardi 24/11, matin | Premier daily ; avis du prof sur l'œuvre |
| Jeudi 26/11, 12h30 | Spec commune, un seul dépôt Moodle pour les six |
| Vendredi 27/11, 17h | Dossier de binôme, charte éditoriale, bible DA (8 éléments), backlog et plan S50/S2. PDF sur Moodle (backlog : PDF ou lien) |
| Lundi 07/12 au soir | Nos cas de test partagés : 11 à 14 et 17 à 19 |
| Mercredi 09/12, jeudi 10/12 | Essais à deux, puis jonction à trois |
| 11 au 15/01 | Finalisation et oral |

**Pas de code en S48.** L'IA est autorisée pour coder, mais chacun doit tout savoir expliquer à l'oral.

## 2. Règles à respecter

1. Les noms du binôme 2 (Maxens Sevilla, Rahim Tamhaev) figurent dans ce dépôt public, avec l'accord des deux (23/11). Aucun nom des autres binômes : leurs noms restent sur Moodle seulement.
2. Aucune clé (OpenRouter, Tailscale, clé privée) dans Git ou dans une demande à l'IA. Un compte et une clé OpenRouter par étudiant. Modèles gratuits seulement.
3. Ne pas publier le sujet.
4. Rien directement sur `main` : branche, PR, relecture. Ne rien republier qui existe déjà.
5. Vérifier la liste des fichiers avant chaque push.
6. Un seul Claude modifie les documents de rendu à la fois : pour l'instant celui de MaxX-J. withRen relit et renvoie ses retours.
7. Ne pas changer la spec seul : il faut un accord par binôme. Ne pas contredire une décision ci-dessous sans en parler à l'autre.

## 3. Où on en est

| Sujet | État |
| --- | --- |
| Spec commune 1.0 | Validée par les six, déposée sur Moodle (confirmé par MaxX-J le 26/11) |
| GitHub | Spec sur `main`, documents du binôme dans `docs/` |
| Six valeurs et règles de notation | Validées le 23/11. Nouvelle liste proposée pour Béziers, à valider (journal du 24/11) |
| Grilles des dix messages | Remplies par les deux ; grille commune remplie |
| Dossier de binôme | Brouillon v0.7 (une seule chaîne), choix validés à deux ; relecture finale avant le PDF |
| Charte éditoriale | Brouillon v0.8 (huit valeurs, `p4` à réessayer), choix validés à deux ; `p5` et la balade en attente restent des propositions |
| Prompt | `p3` essayé avec Nemotron : 65 valeurs justes sur 68 (17 réponses, 8 messages), ordre caché résisté |
| Œuvre | Balades dans Béziers, **rendu C** (toute la ville en 2,5D), jour et nuit, **une seule chaîne de balades** (26/11, voir section 5). Esquisses dans `docs/bible-da/esquisses/`, assets de bâtiments (brouillon) dans `docs/bible-da/assets/batiments/`. Idée approuvée par les enseignants (25/11) |
| Backlog et plan | v2.2 du 26/11, validé à deux |
| Bible DA | **Texte v0.2** du 26/11 (`docs/bible-da/README.md`), moodboard et vue au zoom de withRen attendus. Assets de bâtiments, passants et mobilier en brouillon (25/11) ; style des bâtiments et jour / nuit validés par MaxX-J, passants à valider. Le README des assets renvoie désormais à `ville-vivante.md`, validée par withRen le 25/11 ; fenêtres comptables, teinte des toits et des lumières prêtes dans les SVG. Liste des repères (`docs/bible-da/reperes.md`) et ville vivante (`docs/bible-da/ville-vivante.md`) proposées |
| Symbole, typographie, design system | v1.1 (`docs/bible-da/identite.md`, Figma) : emblème, nom et polices choisis par MaxX-J, validés par withRen |
| Palette | v3.1 (`docs/bible-da/palette.md`, Figma), points ouverts tranchés par MaxX-J le 26/11 ; lumières à tester sur les assets |
| Tailscale | Pas encore connecté chez MaxX-J ; chez withRen, à préciser |


## 4. La spec en bref

Elle fait foi ; elle est dans `docs/spec-commune/README.md` sur `main`.

- Texte canonique à barres, SHA-256, signature Ed25519 en Base64 sur les 64 caractères ASCII de l'`id` ou du `hash`.
- Message : 1 à 280 points de code, NFC, sans retour à la ligne, sans auteur. Bloc : 1 à 50 messages.
- Créneaux de 20 s, ordre a, b, c. Jamais deux blocs de suite du même nœud. Signature entre la 2e et la 15e seconde. Pour produire : au moins un pair répond, aucun n'annonce une chaîne strictement meilleure, ne pas être en `SYNCING`.
- Choix de chaîne : la plus haute, puis le plus petit hash. Pas de finalité : l'œuvre doit suivre un changement de chaîne.
- HTTP/JSON sur Tailscale, port 8080, `/api/v1`. Cinq routes.
- **IA hors chaîne** : chaque binôme garde ses valeurs, clé = `id` du message. Enregistrer `model_requested`, `model_used`, `values`, `status`, `processed_at`.
- Un message valide est toujours accepté et ne s'efface jamais. Modération avant signature, ou masquage chez soi.
- Ouverts : dépôt privé commun (O1, vendredi 27/11), noms Tailscale (O2) et clés publiques réelles (O3) avant ou le 07/12.

**v1.1 proposée le 26/11** par le binôme 3, après la relecture des enseignants (horloge qui peut figer la chaîne, bloc invalide produit). Changements : borne de 5 s dans le futur pour tout bloc, arrêt de la production au-delà de 2 s d'écart avec les deux pairs, vérification de son propre bloc, bloc « confirmé » (3 blocs ou 60 s), chaîne d'essai et chaîne réelle, pair reconnu par son IP, cas 27 à 36, dépôt des cas le 04/12, quota de l'IA à chiffrer, socle du 10/12. À valider par un membre de chaque binôme (O5). Nos documents la suivent déjà ; nos réserves sont dans le journal du 26/11.

## 5. Décisions du binôme

| Sujet | Décision | Statut |
| --- | --- | --- |
| Technique | TypeScript, Node.js, Express, Zod, SQLite (`better-sqlite3`, secours `node:sqlite`), React et Vite, SVG, SSE, Vitest, Playwright | Proposé par withRen, dans le dossier |
| Œuvre | BD non gardée. **Balades dans Béziers** : chaque message est une balade, toutes forment une seule carte. **Rendu C** : toute la ville en 2,5D, repères détaillés, jour et nuit | Choisi le 25/11 ; d'après MaxX-J, le « rendu B » noté le matin était une erreur ; confirmé par withRen. Avis des enseignants à demander |
| Valeurs | Décrivent le message, pas le dessin | Validé à deux |
| Dépôt | Public | Choix de MaxX-J |
| Répartition (indicative) | MaxX-J : nœud et chaîne. withRen : IA et œuvre. Application à deux | Validée |
| Œuvre, 26/11 | Une seule chaîne de balades ; jour, crépuscule, nuit gardés ; émotion du quartier au sol et sur les toits ; bâtiments visités : étages et teinte chaude ; masqué = volet fermé ; traînée à calibrer ; `ambiance` retirée (huit valeurs) ; zigzag dans la rue ; `absurdite` = objet incongru ; pas d'interrupteur « toujours de jour » | Choix de MaxX-J, validés par withRen le 26/11 (journal du 26/11) |
| Machine le 10/12 | PC de MaxX-J, secours PC de withRen | Choix de MaxX-J le 26/11, validé par withRen |
| Accès à l'application | Par Tailscale, port séparé du 8080 | Choix de MaxX-J |
| Modèle | `nvidia/nemotron-3.5-super-vl:free`, secours `openrouter/free` au 3e appel | Choix de MaxX-J, validé par withRen le 26/11 |
| Docker | Non | Choix de MaxX-J |
| Stable | Après 3 blocs suivants (repère d'affichage) | Choix de MaxX-J |
| Limite visiteur | Cookie anonyme, 5 messages par 10 s | Choix de MaxX-J |
| Sauvegarde | Export JSON quotidien des résultats IA | Choix de MaxX-J |
| Échec de l'IA | Élément neutre, avec son `status` | Proposé, **à valider** |
| Consigne | « Raconte un moment, une pensée ou une idée folle. » | Choix de MaxX-J, validé par withRen le 26/11 |

**Encore à décider (27/11) :** nombre de balades de la traînée, liste des repères. Trajet (600 m par étape, 2,5 km au plus, deux étapes si l'IA échoue) et `p5` tranchés le 27/11 (journal). Phrase du 3114 gardée (26/11). Moodboard : pas validé, un nouveau est à faire. `p4` (`p3` sans `ambiance`) à réessayer.

## 6. Les six valeurs (règles du 23/11)

Historique : la liste actuelle compte huit valeurs, voir la charte. Les règles ci-dessous restent valables pour `valence`, `energie`, `tension`, `absurdite` et `emotion`.

| Valeur | Forme |
| --- | --- |
| `valence` | -1, -0.5, 0, 0.5, 1 |
| `energie`, `tension`, `absurdite` | 0, 0.25, 0.5, 0.75, 1 |
| `emotion` | `joie`, `tristesse`, `colere`, `peur`, `surprise`, `degout`, `neutre` |
| `theme` | `relation`, `societe`, `nature`, `imaginaire`, `quotidien`, `autre` |

- `valence` : lire l'ironie ; un manque est négatif ; une blague sans jugement vaut 0.
- `energie` : la force exprimée, pas la gravité.
- `tension` : conflit, menace, inquiétude ; la tristesse seule vaut 0.
- `absurdite` : l'impossible ou l'insensé raconté ; un symbole ou un texte illisible vaut 0.
- `emotion` : celle du texte. Lassitude : `degout`. Révolte : `colere`. Manque : `tristesse`. Sans indice : `neutre`.
- `theme` : sujet principal ; à égalité, le premier dans l'ordre du tableau. Un « on » collectif est `societe`.
- Texte incompréhensible ou consigne à l'IA : nombres à 0, `neutre`, `autre`.

**Première comparaison** (avant ces règles, accords sur 10) : `absurdite` 9, `tension` 8, `energie` 7, `valence` 5, `emotion` 4 à 6, `theme` 2.

Notes de référence : `docs/test-valeurs/decision.csv`.

## 7. Le prompt

`p3` essayé le 25/11 avec Nemotron (65 valeurs justes sur 68). **`p4`** = `p3` sans `ambiance` (26/11), **à réessayer** sur quelques messages avant d'être figé. Tout est dans la charte, partie 3. Relever aussi la limite gratuite exacte.

## 8. Ce que withRen doit faire (avant le 27/11 midi)

1. Lire la PR 21 et le journal de MaxX-J du 26/11, puis valider ou contester les choix (commentaire sur la PR ou son journal).
2. Moodboard illustré et sourcé (auteur, date, adresse) pour la bible DA.
3. Vue au zoom sur une vraie rue : la chaîne, des bâtiments à étages, un objet incongru, jour et nuit.
4. Prévoir des étages dans les assets des bâtiments.
5. Connecter Tailscale.

## 9. La suite

1. Réessayer `p4`.
2. Trancher à deux, plus tard : longueur maximale d'un trajet, trajet si l'IA échoue, nombre de balades de la traînée, liste des repères. Refaire un moodboard.
3. Spec v1.1 validée par les six et déposée sur Moodle (26/11). Réponse des enseignants sur le code en S49 (O6) attendue.
4. Écrire et essayer `p5` (lots de 10).
5. Fusionner la PR 21 (choix validés par withRen le 26/11).
6. Produire les PDF (dossier, charte, bible DA, backlog), dépôt vendredi 27/11 avant 17h, en visant midi.
7. Dépôt privé commun (O1) avec les six, vendredi ; inviter l'équipe enseignante.

## 10. Où sont les documents

| Document | Chemin |
| --- | --- |
| Spec commune | `docs/spec-commune/README.md` |
| Dossier de binôme | `docs/dossier-binome/README.md` |
| Charte éditoriale et prompt | `docs/charte-editoriale/README.md` |
| Règles de notation et grille | `docs/test-valeurs/` |

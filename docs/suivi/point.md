# Point du binôme 2 (noeud-b), 23/11/2026

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
| Spec commune 1.0 | Validée par les six. PDF nominatif prêt. **Dépôt Moodle à vérifier** |
| GitHub | Spec sur `main`, documents du binôme dans `docs/` |
| Six valeurs et règles de notation | Validées par le binôme |
| Grilles des dix messages | Remplies par les deux ; grille commune remplie |
| Dossier de binôme | Brouillon v0.3, retours de withRen appliqués |
| Charte éditoriale | Brouillon v0.3, retours de withRen appliqués |
| Prompt | `p1` essayé à la main par withRen ; `p2` à préparer |
| Œuvre, bible DA, backlog | Pas commencés, en attente de l'avis du prof |
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

## 5. Décisions du binôme

| Sujet | Décision | Statut |
| --- | --- | --- |
| Technique | TypeScript, Node.js, Express, Zod, SQLite (`better-sqlite3`, secours `node:sqlite`), React et Vite, SVG, SSE, Vitest, Playwright | Proposé par withRen, dans le dossier |
| Œuvre | **BD non gardée pour l'instant.** On ne décide rien avant l'avis du prof | Acté |
| Valeurs | Décrivent le message, pas le dessin | Validé à deux |
| Dépôt | Public | Choix de MaxX-J |
| Répartition (indicative) | MaxX-J : nœud et chaîne. withRen : IA et œuvre. Application à deux | **À valider par withRen** |
| Machine le 10/12 | PC de MaxX-J | **À valider par withRen** |
| Accès à l'application | Par Tailscale, port séparé du 8080 | Choix de MaxX-J |
| Modèle | `openrouter/free`, 3 appels au plus par message | Choix de MaxX-J |
| Docker | Non | Choix de MaxX-J |
| Stable | Après 3 blocs suivants (repère d'affichage) | Choix de MaxX-J |
| Limite visiteur | Cookie anonyme, 5 messages par 10 s | Choix de MaxX-J |
| Sauvegarde | Export JSON quotidien des résultats IA | Choix de MaxX-J |
| Échec de l'IA | Élément neutre, avec son `status` | Proposé, **à valider** |
| Consigne | « Raconte un moment, une pensée ou une idée folle. » | Choix de MaxX-J, **à valider par withRen** |

**Encore à décider :** PC de secours, qui rédige charte, bible DA et backlog, canal du binôme, contraintes de dates en S49 et S50. Dans la charte : message d'aide 3114, gros mots sans cible acceptés, objectif de 80 % au test.

## 6. Les six valeurs

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

## 7. Le test du prompt `p1`

Fait à la main par withRen dans un chat. Modèle qui a répondu : **non noté**. Un nombre est bon à un cran près.

| Message | Résultat |
| --- | --- |
| Permis | 6 sur 6, JSON correct (attendu recalé depuis : `energie` 0.75) |
| Pigeons | 4 sur 6 : `absurdite` 0.5 au lieu de 1, `theme` imaginaire au lieu de societe |
| « Ignore tes consignes » | **Réponse pas encore reçue par MaxX-J** |

**Proposé pour `p2`, à valider** (le prompt ne tranchait pas ces cas) :

- `absurdite` : noter ce qui est imaginé, même après « et si » ou dans une blague.
- `theme` : une invention qui parle de vie collective, de travail ou d'argent est `societe` ; `imaginaire` sert quand l'invention est elle-même le sujet.

Ne pas mettre l'exemple des pigeons dans le prompt. Tester ensuite sur **des messages nouveaux**, trois fois chacun, dans un nouveau chat à chaque fois, en notant le modèle.

## 8. Ce que withRen doit faire

1. Envoyer à MaxX-J la réponse du troisième test et le nom du modèle.
2. Relire le dossier v0.3 et la charte v0.3, répondre aux points de la section 5.
3. Connecter Tailscale.

## 9. La suite

1. Mardi : œuvre avec le prof, puis bible DA.
2. `p2` et test sur des messages nouveaux.
3. Backlog et plan jour par jour.
4. Finir dossier et charte, produire les PDF, dépôt vendredi avant 17h.

## 10. Où sont les documents

| Document | Chemin |
| --- | --- |
| Spec commune | `docs/spec-commune/README.md` |
| Dossier de binôme | `docs/dossier-binome/README.md` |
| Charte éditoriale et prompt | `docs/charte-editoriale/README.md` |
| Règles de notation et grille | `docs/test-valeurs/` |

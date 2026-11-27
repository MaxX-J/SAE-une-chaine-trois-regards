# Dossier de binôme 2 (noeud-b)

27/11/2026

| | |
| --- | --- |
| Binôme | 2 : Maxens Sevilla (`MaxX-J`) et Rahim Tamhaev (`withRen`) |
| Nœud | noeud-b : un créneau de 20 s sur trois (ordre a, b, c) |
| Spec commune | v1.1 du 26/11/2026, validée par les six |
| Version du dossier | 0.9, rendu du 27/11/2026 |
| Langage | TypeScript, pour le nœud et l'application |

Ce dossier ne recopie pas la spec : « spec 4.2 » renvoie à sa section 4.2. L'œuvre est détaillée dans la bible DA, les valeurs et le prompt dans la charte éditoriale.

## 1. Le projet en bref

**Notre regard.** Une blockchain garde des paroles qu'on ne peut plus effacer. Une ville garde les pas de ceux qui la traversent. **Chaque message devient une balade dans Béziers, qui repart d'où la précédente s'est arrêtée.** Ensemble, elles dessinent le Béziers que les gens ressentent. Les enseignants ont approuvé l'idée.

**L'application.**
- Le visiteur est prévenu : son message ne s'effacera pas, il est partagé avec les deux autres binômes et lu par une IA, il ne doit contenir aucune donnée personnelle (spec 8.1).
- Il écrit 280 caractères au plus.
- Il reçoit sa balade : un titre, des étapes, une distance. Elle est en attente, puis tracée quand le message est dans un bloc et lu par l'IA.
- Il explore la carte, zoome, et retrouve sa balade par un lien qui contient l'id de son message.

**L'œuvre.** Béziers en 2,5D (faux relief, sans 3D). L'IA tire huit valeurs de chaque message : elles choisissent les lieux, la longueur, la couleur et la forme de la balade. Toutes les balades forment **une seule ligne** à travers la ville, comme les blocs de la chaîne. Chaque balade change la ville :
- les rues empruntées prennent sa couleur ;
- les bâtiments où elle s'arrête gagnent des étages ;
- chaque quartier prend l'émotion qui domine chez lui (sol, toits, arbres) et une lumière selon son humeur (jour, crépuscule, nuit).

Les messages des trois binômes suivent les mêmes règles. Seule la forme des étapes rappelle leur nœud.

**Indispensable :** écrire un message et le voir entrer dans la chaîne ; recevoir sa balade et voir la carte changer ; un nœud qui passe les cas de test de la spec ; la trace du modèle d'IA qui a répondu.

**En plus, si le temps le permet :** passants, mobilier, objets incongrus, repères en plus, panneau d'état de la chaîne, carte-souvenir, animation d'apparition (détail dans le backlog).

## 2. L'architecture

![Schéma d'architecture de noeud-b : l'application web parle à l'API application ; dans le processus noeud-b, le module chaîne reçoit l'API application et l'API entre nœuds, le worker IA appelle OpenRouter, le module œuvre lit les données de ville ; tous écrivent dans la base SQLite ; noeud-a et noeud-c échangent avec l'API entre nœuds par HTTP sur Tailscale.](architecture.svg)

Tout ce qui est dans le cadre tourne dans **un seul processus Node.js**, sur l'ordinateur du binôme. Le module chaîne est le centre : rien n'entre dans la chaîne sans lui.

| Composant | Rôle | Parle avec |
| --- | --- | --- |
| Application web | Écrire, voir la ville et les balades | API application (HTTP, SSE) |
| API application | Filtrer et recevoir les messages, servir l'œuvre | Module chaîne, module œuvre |
| Module chaîne | Signer, valider, tenir la file, produire, rattraper | Base, pairs (HTTP) |
| API entre nœuds | Les cinq routes de la spec (6.3), port 8080 | noeud-a, noeud-c |
| Worker IA | Lire les messages par lots, enregistrer les valeurs | Base, OpenRouter (HTTPS) |
| Module œuvre | Calculer les balades et les quartiers | Base, données de ville |
| Base SQLite | Chaîne, file, résultats IA, journaux | Tous les modules |
| Données de ville | Rues, lieux, quartiers, fonds, bâtiments | Lues au démarrage |

**Qui peut joindre quoi.**
- Port 8080 : seulement par Tailscale, sous le nom noeud-b. C'est l'API de la spec.
- L'application a son propre port, joignable par Tailscale seulement : les visiteurs écrivent sur notre PC ou depuis une machine du réseau Tailscale. Rien n'est ouvert sur internet.
- OpenRouter : HTTPS, port 443, ouvert sur eduroam.

**Pourquoi un seul processus.** Node.js est asynchrone : le producteur de blocs n'attend jamais le worker IA. Toutes les erreurs du worker sont rattrapées ; s'il plante quand même, il est relancé sans arrêter le nœud. Si le processus entier s'arrête, il redémarre seul (tâche D01) et reprend la chaîne sur disque. **Écarté :** un processus par module (plus de choses à lancer et à surveiller, pour peu de gain avec Node.js).

## 3. Le parcours d'un message

| Étape | Ce qui se passe | Si ça échoue |
| --- | --- | --- |
| 1. Écriture | Le visiteur lit l'avertissement et valide | Erreur sous le champ, texte gardé |
| 2. Contrôle | NFC, 1 à 280 points de code, caractères interdits, filtre de la charte, 5 messages par 10 s (spec 2.1, 8.2) | Refusé avant signature : aucune trace |
| 3. Signature | Horodatage croissant, id SHA-256, signature Ed25519, entrée dans la file (spec 2.1) | Le visiteur peut réessayer |
| 4. Envoi | Envoi immédiat aux deux pairs (spec 6.4) | Le sondage de 10 s rattrape |
| 5. Production | À notre créneau, si les conditions sont réunies (ci-dessous) | Le message attend le créneau suivant |
| 6. Réception | Un bloc reçu est validé (spec 3.2), ses messages sortent de la file | 409 ou 422, journalisé |
| 7. IA | Lecture par lots de 10 (section 5) | Balade en attente, ou neutre en cas d'échec |
| 8. Œuvre | Ordre de la chaîne (jamais le timestamp, spec 5.3), balade sur les vraies rues | Balade neutre |
| 9. Affichage | La balade apparaît, puis est marquée confirmée | L'application se reconnecte et relit l'état |

**Conditions pour produire un bloc** (spec 4.2) :
- c'est notre créneau et la file n'est pas vide ;
- au moins un pair répond, et aucun n'a une chaîne meilleure ;
- nous ne sommes pas en `SYNCING` et n'avons pas produit le dernier bloc ;
- le créneau est plus récent que celui de la tête ;
- notre horloge est à 2 s au plus d'au moins un pair.

On prend 50 messages au plus et on signe entre la 2e et la 15e seconde. **Avant de l'ajouter, on vérifie notre propre bloc avec les règles d'un bloc reçu.**

**Confirmée** = son bloc a 3 blocs au-dessus de lui, ou rien n'a changé depuis 60 s chez tous les pairs joignables (spec 5.3). La seconde règle sert au dernier message de la journée. Avant, le visiteur voit « en attente », puis « dans un bloc ».

**Fourche.** Les messages de nos blocs abandonnés retournent dans la file (spec 5.2). Leurs valeurs IA restent valables (clé : l'id du message). Les quartiers sont recalculés. Une balade ne change pas de forme, mais peut disparaître un moment. La position d'un message se lit toujours dans la chaîne actuelle.

**Visiteur.** Il est reconnu par un cookie de session anonyme. L'effacer contourne la limite de 5 messages : c'est accepté.

## 4. Les données

Une seule base SQLite, dans un fichier local. Chaque écriture liée est une transaction.

| Table | Ce qu'elle garde |
| --- | --- |
| blocks | Les blocs de notre chaîne |
| messages | Les messages, dans un bloc ou en file |
| ai\_results | Un résultat IA par message : modèle demandé et modèle qui a répondu (spec 9), version du prompt, réponse brute |
| hidden\_messages | Les messages masqués dans l'œuvre (ils restent dans la chaîne) |
| slot\_log | Les créneaux signés, écrits avant de signer (spec 4.2) |
| node\_state | Le dernier horodatage émis, le compteur du quota IA |
| events\_log | Erreurs, doubles signatures, écarts d'horloge (spec 3.4, 8.3) |

Les noms suivent la spec. Deux mots sont réservés en SQL : `index` devient `block_index`, `values` devient `ai_values`.

**Données de ville.** Préparées une fois à partir d'OpenStreetMap, puis triées à la main : réseau de rues, environ 80 lieux avec leur famille, une dizaine de quartiers, fonds de ville de jour et de nuit, bâtiments en SVG. Elles portent un numéro de version (`map_version`), figé avant la jonction. Jamais d'adresse : les logements sont des quartiers. Mention « © les contributeurs OpenStreetMap » sur la carte, licence ODbL.

**Pas stocké.** Les balades et les quartiers se recalculent depuis la base et les données de ville. Une fourche ne laisse rien à nettoyer.

**Deux chaînes.** Le réglage `essai` ou `reelle` choisit ensemble le bloc zéro et les clés (spec 2.3.1). Chaque chaîne a sa base. Les clés publiques des trois nœuds sont dans un fichier de configuration versionné.

**Sauvegarde.** La chaîne se récupère chez les pairs. Les résultats IA n'existent que chez nous : export JSON chaque jour de travail.

**Écarté :** des fichiers JSON (écritures non sûres en cas de coupure) ; PostgreSQL (un serveur de plus, pour rien).

## 5. L'IA

**Quand.** Le worker lit les messages de la chaîne **réelle** qui n'ont pas encore de résultat. Jamais ceux de la chaîne d'essai. Aucun appel à l'écriture : une panne d'IA ne bloque ni l'écriture ni les blocs.

**Quel modèle.** `nvidia/nemotron-3.5-super-vl:free`, fixe pour une lecture régulière. Au 3e appel, secours `openrouter/free`. On enregistre le modèle demandé et celui qui a répondu. **Écarté :** `openrouter/free` seul (il change de modèle, les réponses varient).

**Le prompt.** Les messages partent par lots, encodés en JSON par le code : `{"messages": [{"n": 1, "message": "…"}, …]}`. La consigne demande d'ignorer tout ordre contenu dans un message. Le prompt `p5` et les valeurs sont dans la charte (partie 3). `p5` a été essayé le 27/11 : bon format, et un ordre caché glissé dans un lot ne change rien. `p4`, un message par requête, reste le secours.

**Le quota.** 20 requêtes par minute et **50 par jour** sur un compte gratuit. À vérifier sur la clé de MaxX-J avant le 07/12 (`GET /api/v1/key` d'OpenRouter).

| | Par message (`p4`) | Par lots de 10 (`p5`) |
| --- | --- | --- |
| Messages lus par jour, au mieux | 50 | 500 |
| Au pire (3 appels par lot) | 16 | 160 |

**Quand un lot part.** Dès que 10 messages attendent, ou 2 minutes après l'arrivée du plus ancien. Jamais plus d'une requête par minute. Sans cette règle, chaque bloc enverrait un lot d'un seul message et le quota partirait en une heure.

**Réserve.** 15 requêtes par jour sont gardées pour l'oral, dès le 10/12. Un compteur en base arrête le worker à la réserve. Les messages non lus attendent le lendemain : leur balade est **en attente** (trait fin gris, sans effet sur la ville), puis se colore. **Écarté :** acheter des crédits (le sujet veut des modèles gratuits) ; deux clés sur un même nœud (une clé par étudiant).

**Quand ça se passe mal.** Un lot a droit à **3 appels au plus**.

| Situation | Ce que fait le worker | Statut |
| --- | --- | --- |
| Pas de réponse en 20 s, erreur serveur, 429 | Nouvel appel après 5 s, puis 15 s ; sur 429, pause | timeout |
| Réponse hors format | Nouvel appel avec un rappel du format | invalid\_format |
| Un seul message du lot hors bornes | Les autres sont gardés ; lui seul est redemandé | invalid\_format |
| Refus sur un lot | On coupe le lot en deux, chaque moitié est réessayée une fois | refused |
| Refus sur un message seul | Plus d'appel | refused |
| Réponse correcte | Valeurs enregistrées telles quelles | ok |

Après un échec, la balade est tracée avec les valeurs par défaut de la charte (repère, neutre, nombres à 0). Un refus ne masque rien tout seul : le masquage reste une décision du binôme (charte).

**Contre les injections.** Une réponse passe un schéma strict. Un ordre caché peut au pire choisir des valeurs dans les bornes. Aucun texte de l'IA n'est affiché : le titre d'une balade est composé par le code.

## 6. Des valeurs à l'œuvre

Le module œuvre prend les valeurs et l'ordre de la chaîne, et calcule deux choses : **la balade de chaque message** et **l'état de chaque quartier**.

**La balade** (mêmes valeurs, même id, même carte = même balade) :
1. Elle part de la dernière étape du message précédent. Le premier part d'un repère fixe.
2. `lieu` et `lieu_secondaire` donnent les familles, `energie` le nombre d'étapes (2 à 6).
3. Les étapes sont choisies par l'id, parmi les lieux proches : 600 m au plus entre deux étapes, 2,5 km au plus en tout.
4. Un plus court chemin (A*) suit les vraies rues. Repasser au même endroit est permis.
5. `tension` casse le tracé, sans sortir de la rue.
6. `absurdite` à 0,5 ou plus pose un objet incongru (piano, baignoire…) près d'une étape.

Si l'IA a échoué : deux étapes vers des repères proches, trait gris, sans effet sur la ville. Si la chaîne change, les balades sont recalculées depuis le premier bloc qui diffère.

**Le quartier** regarde ses 20 derniers messages, quel que soit le binôme.

| Valeur | Balade | Ville |
| --- | --- | --- |
| `lieu`, `lieu_secondaire` | Étapes | Bâtiments visités : étages, teinte chaude |
| `emotion` | Couleur et motif | Rues ; sol, toits et arbres du quartier |
| `intensite` | Force de la couleur | |
| `valence` | | Jour (0,12 et plus), crépuscule, nuit (-0,12 et moins) ; jour sans message |
| `energie` | Nombre d'étapes | |
| `tension` | Tracé souple à cassé | |
| `absurdite` | Objet incongru | L'objet reste |
| Sans IA | Forme des étapes selon le nœud | Fenêtres allumées, rues plus claires selon les passages |

Plages, couleurs et motifs : [palette](../bible-da/palette.md) et [ville vivante](../bible-da/ville-vivante.md).

**Le dessin, de bas en haut :**
1. Le fond de ville en images (jour, nuit ; le crépuscule superpose les deux), découpé par quartier.
2. Les bâtiments : dans l'image de loin, en SVG au zoom, avec des fenêtres à allumer.
3. Les tracés en SVG.
4. Les symboles des lieux et l'interface.

**Beaucoup de balades.** Une traînée suit la tête de la chaîne : les dernières balades sont nettes, la plus récente a un point et un halo. Les anciennes ne restent que dans la lumière des rues et la hauteur des bâtiments. Le visiteur retrouve toujours la sienne.

**Message masqué.** Sa balade et ses effets disparaissent, un volet fermé reste dans le quartier. Le message reste dans la chaîne (spec 8.1) ; son texte n'est jamais envoyé à l'application.

**Accessibilité.** Une liste des balades, au clavier et au lecteur d'écran, double la carte. La couleur est toujours doublée d'un motif ou d'un mot. L'humeur des quartiers est écrite. Pas de clignotement ; animations coupées si on demande moins de mouvement.

**Écarté :** une moyenne des tracés ; des balades séparées (illisibles à 300) ; la vraie 3D (longue, moins accessible) ; une carte en ligne ; un rendu fait par l'IA (pas reproductible).

## 7. Les choix techniques

| Sujet | Choix | Pourquoi (écarté) |
| --- | --- | --- |
| Langage | TypeScript strict, Node.js LTS | Un langage partout, SHA-256 et Ed25519 intégrés (PHP, Python) |
| API | Express | Simple pour cinq routes (Fastify) |
| Validation | Zod strict | Refuse champs inconnus et null, comme la spec (écrite à la main) |
| Calculs de la spec | crypto natif, NFC, points de code, listes en dur | `trim()` dépend du langage |
| Stockage | SQLite, better-sqlite3 | Un fichier, des transactions ; `node:sqlite` en secours |
| Appels entre nœuds | fetch natif, délais de la spec | Aucune dépendance |
| Application | React, Vite | Composants : balade, quartier, liste (page sans framework) |
| Temps réel | SSE | Un seul sens suffit (Socket.io) |
| Dessin | Images de fond, SVG au zoom | 11 725 bâtiments ne tiennent pas en SVG (Canvas, Three.js) |
| Carte | OpenStreetMap, gardée dans le dépôt | Vraies rues, pas d'appel en ligne (Google Maps) |
| Chemins | A* écrit par nous | Réseau petit, résultat reproductible |
| Qualité | ESLint, Prettier, pino, Vitest, Playwright | Erreurs et preuves trouvées tôt |
| Exécution | Directement sur le PC, sans Docker | Une couche de moins |

**Machine du nœud.** Le PC de MaxX-J le 10/12, celui de withRen en secours. On y copie alors la base et la clé privée, sans jamais faire tourner les deux en même temps (double signature).

## 8. Les tests

L'horloge du nœud est injectée : les cas à heure simulée se rejouent sans attendre.

| Niveau | Ce qu'on vérifie | Quand |
| --- | --- | --- |
| Nœud seul | Vecteurs de la spec et cas 1 à 14, 18, 19, 22 à 24, 27 à 32, 34 à 36, sans réseau, chaîne d'essai (Vitest) | 07 et 08/12 |
| Nœud et pairs | Cas 15 à 17, 20, 21, 25, 26, 33 : trois instances sur un PC, puis à deux sur Tailscale, puis à trois | 08 au 10/12 |
| Balades | Même message, même balade ; bornes ; fourche et masquage | S50 et S2 |
| Bout en bout | Écriture, bloc, IA, balade, pannes d'IA, accessibilité (Playwright, faux serveur d'IA, axe) | S50 à S2 |

**Nos cas partagés.** Vecteurs 11 à 14, 17 à 19, 28, 29, 31 et scénarios 16, 34. Dépôt le lundi 07/12, ou le 04/12 si les enseignants acceptent un script en S49 (O6).

**Le 10/12.** On vise le socle de la v1.1 (10.0) : formats, validité, nos propres blocs vérifiés, production, cinq routes, sondage, rattrapage simple, disque. Les limites de débit peuvent attendre la S2.

**Notre part dans la v1.1.** Trois points relevés et intégrés : trois nœuds sur un même PC (une adresse `127.0.0.x` par nœud), l'arrêt quand trois horloges sont décalées deux à deux, la date de dépôt des cas.

**Critère de fin.** Un vecteur qui échoue = une erreur de notre code, sauf si deux binômes lisent la spec différemment : on corrige alors la spec (10.3).

## 9. Les risques

| Risque | Parade |
| --- | --- |
| Empreintes différentes des autres nœuds | Vecteurs rejoués dès le 07/12, jamais `trim()` |
| Horloges décalées, chaîne figée | Spec v1.1 ; heure comparée à une source HTTPS et corrigée au début de chaque séance (NTP peut être bloqué sur eduroam) |
| PC en veille ou mise à jour Windows le jour J | Sur secteur, veille coupée, mises à jour suspendues la semaine du 07/12 |
| Le worker IA plante | Erreurs rattrapées, relance sans arrêter le nœud (section 2) |
| Quota IA épuisé | Lots de 10, réserve de 15 requêtes, balades en attente |
| Noms Tailscale non résolus (O2) | Adresses IP en configuration |
| Double signature après un redémarrage | Créneau écrit avant de signer |
| better-sqlite3 ne s'installe pas | Testé sur nos deux PC en S49, `node:sqlite` en secours |
| Fuite d'une clé | `.env` hors de Git ; en cas de fuite, on prévient les six (spec 8.4) |
| Texte choquant | Filtre avant signature, aucun texte de l'IA affiché, masquage |
| Une balade blesse (culte, deuil, domicile) | Rien de moqueur dans ces lieux, aucune adresse |
| Ville lente à afficher | Images de fond, SVG dans la zone visible, essai à 300 messages |
| OpenStreetMap mal classé | 80 lieux triés à la main |
| Trop de balades au même endroit | Plusieurs lieux par famille, choisis par l'id |
| Trop peu de temps en S50 | Indispensable d'abord ; ordre de coupe dans le backlog |
| Un de nous absent, charge inégale | Les deux relisent tout, journal partagé, point chaque semaine |
| Code de l'IA mal compris | Relu, testé et expliqué avant fusion (section 10) |

## 10. L'organisation

| Zone | Responsable | Relecteur |
| --- | --- | --- |
| Calculs, validation, production | MaxX-J | withRen |
| Routes, rattrapage | withRen | MaxX-J |
| Écriture : page, API, filtre | withRen | MaxX-J |
| IA, carte commune, dessin | withRen | MaxX-J |
| Balade calculée, accessibilité | MaxX-J | withRen |
| Tests et jonction | les deux | les deux |
| Documents | les deux | les deux |

Répartition indicative, détaillée dans le backlog.

**À deux.** Daily chaque matin avec l'enseignant, puis un point entre nous le soir. En S49, un message par jour. Discord pour les six, un canal pour nous deux.

**Git.**
- Dépôt GitHub public, nos deux noms seulement, enseignants invités.
- Rien sur main : une branche par tâche, une pull request relue par l'autre.
- Une issue par tâche, suivies dans le tableau GitHub du binôme.
- Commits courts. Secrets dans `.env` seulement.
- `CLAUDE.md` et `docs/suivi/` partagent le contexte entre nous.

**L'IA pour concevoir.** Nous proposons, Claude commente, nous décidons. Le journal dit qui a décidé quoi.
- Nos idées : la ville et les bâtiments (withRen), les balades dans Béziers (piste de l'enseignante d'art), la lumière selon la `valence`, la chaîne unique, les bâtiments qui grandissent (MaxX-J).
- Gardé : l'IA hors de la chaîne, le jour et la nuit par quartier, le contraste de la palette.
- Refusé : la valeur `sociabilite`, le `mot` libre, le ruban de couleurs au sol (jugé laid), l'ordre des tâches et la palette de nuit (corrigés par withRen).

**L'IA pour coder.** Autorisée par le sujet.
- L'IA propose ; nous relisons, testons et comprenons chaque ligne avant de fusionner.
- Aucune clé ni message réel dans une demande.
- Les vecteurs de la spec font foi.
- Un court journal des usages dans `docs/suivi/`.

**Calendrier.** S48 : conception. S49 : environnement et données de ville, sans code du projet. S50 : nœud prêt le 07/12, essai à deux le 08 ou le 09/12 au matin, jonction le 10/12 sur la chaîne d'essai, puis ouverture de la chaîne réelle. S2 : finalisation et oral. Plan jour par jour dans le backlog.

## 11. Démarrer le projet

État visé, confirmé quand le code existera (S50). Le dépôt suit le référentiel : `docs/`, `infra/`, `src/` (nœud, application, code commun), `tests/` (dont `tests/vectors/`), `.env.example`.

**Il faut :** Node.js LTS, Git, Tailscale (`tailscale set --hostname noeud-b`), un compte OpenRouter.

```powershell
npm install
copy .env.example .env
npm run keygen   # crée la clé du nœud et affiche la clé publique à envoyer aux six (O3)
npm run dev      # lance le nœud et l'application
npm test         # rejoue les cas de la spec
```

| Variable du `.env` | Rôle |
| --- | --- |
| `NODE_ID` | `noeud-b` |
| `NODE_SEED` | Graine de la clé privée (secrète) |
| `CHAINE` | `essai` ou `reelle` : bloc zéro et clés (spec 2.3.1) |
| `PEERS` | Adresses des pairs ; en test, une adresse `127.0.0.x` par nœud |
| `PORT_NODE`, `PORT_APP` | 8080, et le port de l'application |
| `DB_PATH` | Fichier SQLite (un par chaîne) |
| `OPENROUTER_API_KEY` | Clé OpenRouter (secrète) |
| `IA_RESERVE` | Requêtes gardées pour l'oral (15) |

**En cas de souci :** `tailscale status` doit lister les autres nœuds ; `/api/v1/status` d'un pair doit répondre ; l'écart d'horloge affiché par le nœud doit rester sous 2 s.

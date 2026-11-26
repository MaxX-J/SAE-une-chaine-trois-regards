# Backlog et plan S50 / S2

Binôme 2 (noeud-b) : Maxens Sevilla (M) et Rahim Tamhaev (R).

**Version 2.2 du 26/11/2026.** v2 validée par M le 26/11 ; choix de l'œuvre du 26/11 validés par R ; spec v1.1 validée par les six le 26/11. Rendu : vendredi 27/11, 17h, PDF ou lien.

## Hypothèses

- 6 heures utiles par personne et par jour. Les estimations sont les nôtres, aucune n'a été vérifiée.
- L'œuvre : **balades dans Béziers, rendu C** (toute la ville en 2,5D), jour et nuit, **une seule chaîne de balades** (M, 26/11). Choix du binôme d'après M, avis des enseignants à demander. Les tâches concernées portent un **★** : si l'œuvre change, elles changent, le reste tient.
- De loin, la ville est une image préparée à l'avance ; au zoom, les bâtiments génériques de R remplacent les blocs de la zone visible ; les repères restent détaillés. Les balades passent par-dessus en transparence.
- Les numéros de section renvoient à la spec commune 1.0. La spec impose que le nœud et l'application soient prêts pour la jonction : la chaîne passe donc **avant** l'œuvre.
- **[À CONFIRMER]** : à trancher à deux.

## 1. Le backlog

### Indispensable

| N° | Tâche | Terminée quand | h | Qui | Jour |
| --- | --- | --- | --- | --- | --- |
| N01 | Projet TypeScript, tests, lint, `.env.example` | `npm test` passe sur les deux machines | 1 | M | 07/12 |
| N02 | Texte canonique, NFC à la création seulement, SHA-256, Ed25519 ; blocs zéro d'essai et réel | Les vecteurs de la section 2 et le bloc zéro réel de test (v1.1, 2.3.1) sont retrouvés à l'identique | 3 | M | 07/12 |
| N03 | Base SQLite : chaîne, file, créneaux écrits **avant** de signer (4.2.3) ; réglage `essai` ou `reelle`, une base par chaîne | Un redémarrage ne perd rien et ne permet aucune double signature | 2 | M | 07/12 |
| A01 | Page d'écriture : consigne, avertissement, compteur, erreurs | Utilisable avec une API simulée, au clavier | 3 | R | 07/12 |
| T01 | Nos cas partagés (v1.1) : vecteurs 11 à 14, 17 à 19, 28, 29, 31 ; scénarios 16 et 34, au format commun | Déposés dans le dépôt commun | 4 | R | 04/12 ou 07/12 |
| N04 | Validation des messages, blocs et chaînes (3.1 à 3.3), borne future de 5 s partout (v1.1) | Les cas 1 à 14, 18, 19, 23 et 27 à 32 passent | 6 | M | 08/12 |
| N06 | Les cinq routes entre nœuds, ordre des refus (6.2, 6.3) ; limites (8.2) en S2 si besoin | Les cas 2, 22 et 36 passent, un autre nœud lit notre `/status` sur Tailscale **le mardi soir** | 4 | R | 08/12 |
| N07a | Choix de chaîne et lecture de la chaîne d'un pair (5.1, 7) | Les cas 15, 26 et 33 passent en local | 2 | R | 08/12 |
| N05 | Production de blocs à notre créneau (4.2), conditions 7 et 8, **vérification de notre propre bloc** avant de l'ajouter | Les cas 24, 34 et 35 simulés passent, y compris après un redémarrage | 4 | M | 09/12 |
| N08 | Envoi aux pairs, sondage de 10 s, écart d'horloge qui arrête la production au-delà de 2 s (6.4) | Le cas 25 passe entre deux instances locales | 2 | M | 09/12 |
| N07b | Fourche, rattrapage, SYNCING (5.2, 7) | Les cas 16, 20 et 21 passent en local | 3 | R | 09/12 |
| A02 | API de l'application : filtre, limite par visiteur, signature | Un message écrit arrive dans la file | 2 | R | 09/12 |
| J01 | Essai à deux sur Tailscale, chaîne d'essai | Un autre nœud et le nôtre ont la même tête | 2 | M, R | 08/12 ou 09/12 matin |
| J02 | **Jonction à trois** : horloges mesurées, cas de test sur la chaîne d'essai, trois messages par binôme, coupure, redémarrage, puis ouverture de la chaîne réelle (10.3) | Les trois chaînes ont la même tête, les trois blocs zéro réels sont identiques | 12 | M, R | 10/12 |
| B01 | ★ Balade calculée depuis les valeurs et l'`id`, sur les vraies rues, à partir de la fin de la précédente | Le même message donne toujours la même balade | 3 | M | 11/12 |
| C01 | ★ Fond de ville en 2,5D, en image, et premier tracé | La ville s'affiche en moins de 2 s, mention OpenStreetMap visible | 2 | M | 11/12 |
| D01 | Démarrage automatique du nœud, port séparé de l'application | Le nœud repart seul après un redémarrage du PC | 1 | M | 11/12 |
| I01 | Worker IA : lots de 10, JSON strict, trois essais par lot, statuts, modèle enregistré, compteur du quota et réserve de 15 requêtes | Les cinq situations passent avec un faux serveur ; le worker s'arrête à la réserve | 5 | R | 11/12 |
| A03 | Suivi du message (SSE) : en attente, dans un bloc, lu, confirmé | L'état se met à jour sans recharger | 1 | R | 11/12 |
| I03 | Export JSON quotidien des résultats de l'IA | Un fichier daté peut être relu | 1 | R | 11/12 |
| A04 | ★ Vue d'un parcours : titre, étapes, distance | Le visiteur retrouve sa balade | 3 | M | 11/01 |
| N09 | Journaux et preuves (3.4, 8.3) | Une double signature reçue est gardée avec ses deux blocs | 1 | M | 11/01 |
| A05 | Message masqué, avant et après la chaîne | Ni texte ni effet visible, la chaîne est intacte | 2 | M | 11/01 |
| C02 | ★ Carte commune : rues colorées par les passages, traînée, sol et toits selon l'émotion du quartier | 0, 10, 60 et 300 messages sont lisibles et fluides | 4 | R | 11/01 |
| C07 | ★ Les repères posés sur la vraie carte | Les 10 repères sont à leur place et dans le bon ordre | 1 | R | 11/01 |
| I02 | Derniers essais du prompt sur messages notés avant l'IA | Résultats et modèle écrits dans la charte | 1 | R | 11/01 |
| B02 | ★ Effets des valeurs sur le tracé | Deux messages opposés donnent deux balades visiblement différentes | 4 | M | 12/01 |
| B03 | ★ Bâtiments visités : étages en plus, teinte chaude | Un bâtiment souvent visité se voit de loin, sans dépasser son plafond | 2 | M | 12/01 |
| C03 | ★ Bâtiments génériques au zoom, allégés, colorés par les messages | Moins de 60 Ko par image, la couleur du message reste visible | 4 | R | 12/01 |
| C05 | ★ Palette fermée et légende | Conforme à la bible DA, lisible sans la couleur seule | 2 | R | 12/01 |
| C06 | L'œuvre suit un changement de chaîne, repère « confirmé » (3 blocs ou 60 s, v1.1) | Une fourche simulée recalcule la carte | 3 | M | 13/01 |
| A06 | Accessibilité : clavier, liste des balades, contraste, mouvement réduit | Contrôle axe sans erreur, parcours complet au clavier | 3 | M | 13/01 |
| C04 | ★ Zoom à trois niveaux | Les détails apparaissent sans ralentir | 3 | R | 13/01 |
| C08 | ★ Jour, crépuscule et nuit par quartier selon `valence` | Un message change la lumière de son quartier ; l'humeur est écrite | 3 | R | 13/01 |
| T02 | Test de bout en bout avec faux serveur IA | Écriture, bloc, IA et balade passent automatiquement | 3 | M | 14/01 |
| T03 | Performance à 300 messages | Affichage fluide sur la machine de démonstration | 3 | R | 14/01 |
| O01 | Répétition de l'oral, scénario de secours | Deux passages complets, questions échangées | 6 | M, R | 14/01 |

Les heures d'une tâche à deux sont le total des deux personnes.

### En plus, si le temps le permet

| N° | Tâche | h | Priorité |
| --- | --- | --- | --- |
| P01 | ★ Fenêtres allumées selon les messages d'un quartier | 2 | 1 |
| P02 | ★ Repères en plus : théâtre, Plateau des Poètes, Madeleine (liste : `docs/bible-da/reperes.md`) | 4 | 2 |
| P03 | Panneau d'état de la chaîne | 3 | 3 |
| P04 | ★ Carte-souvenir de la balade à télécharger | 3 | 4 |
| P05 | Animation d'apparition, désactivable | 2 | 5 |
| P06 | ★ Passage par un lieu cité dans le message | 3 | 6 |
| P07 | ★ Arbres (saison selon l'émotion du quartier), mobilier et densité du décor | 4 | 7 |
| P08 | ★ Passants : nombre, allure et posture | 5 | 8 |
| P09 | ★ Objets incongrus selon `absurdite` (piano, baignoire, taureau, poisson volant) | 2 | 9 |

Si nous prenons du retard, nous coupons dans cet ordre : tout ce qui est en plus, puis les étages des bâtiments visités, puis les bâtiments génériques au zoom, puis la nuit. Le rendu retombe alors sur des blocs simples et les repères. **Jamais** la chaîne, les messages masqués ni l'accessibilité de base.

### Les valeurs de l'IA et leur effet

Chaque valeur demandée à l'IA doit avoir un effet dans une tâche. Validé par M le 26/11, `ambiance` retirée :

| Valeur | Effet | Tâche |
| --- | --- | --- |
| `lieu`, `lieu_secondaire` | Lieux traversés | B01 |
| `emotion`, `intensite` | Couleur du tracé et des rues, sol et toits du quartier, force de la couleur | C02, C05 |
| `energie`, `tension` | Nombre d'étapes, forme du tracé dans la rue | B02 |
| `absurdite` | Objet incongru (en plus : sans P09, elle ne dessine rien) | P09 |
| `valence` | Jour, crépuscule ou nuit du quartier | C08 |

`moment` est remplacée par `valence`, qui décide de la lumière du quartier (`docs/bible-da/ville-vivante.md`). `direction` et `temps`, restées en option, sont retirées.

## 2. La répartition

| Zone | Responsable | Relecteur |
| --- | --- | --- |
| Calculs, validation, production | M | R |
| Routes, rattrapage | R | M |
| Page d'écriture et API de l'application | R | M |
| IA, carte commune, styles, zoom, palette | R | M |
| Balade calculée, vue d'un parcours, accessibilité | M | R |
| Tests et jonction | les deux | les deux |

| | M | R |
| --- | --- | --- |
| S50 (du 07 au 11/12) | 30 h | 30 h |
| S2 (du 11 au 14/01) | 24 h | 24 h |

La répartition validée (M le nœud, R l'IA et l'œuvre) est ajustée sur deux points (accord de M et R le 26/11) : R prend une partie du nœud avant le 10/12, car c'est le plus urgent et chacun doit savoir l'expliquer ; M prend une partie de l'œuvre ensuite. L'autre relit toujours avant fusion.

## 3. Le plan

### S50

| Soir | Ce qui fonctionne | M | R |
| --- | --- | --- | --- |
| Lundi 07/12 | Vecteurs retrouvés, base créée, cas partagés déposés, page d'écriture | N01, N02, N03 | A01, T01 |
| Mardi 08/12 | Validation, cinq routes, **première lecture d'un autre nœud sur Tailscale** | N04 | N06, N07a |
| Mercredi 09/12 | Production, rattrapage, écriture depuis l'application, essai réel à deux (dès le mardi si un autre nœud est prêt) | N05, N08, J01 | N07b, A02, J01 |
| **Jeudi 10/12** | **Les trois nœuds ont la même chaîne** | J02 | J02 |
| Vendredi 11/12 | Parcours complet : message, bloc, IA, première balade | B01, C01, D01 | I01, A03, I03 |

T01 a besoin de N02 : M commence par N01 et N02, R par A01. N07a commence dès le mardi pour laisser une marge au mercredi. Si le mercredi déborde, A02 passe au jeudi matin, jamais J01.

### S2

| Soir | Ce qui fonctionne | M | R |
| --- | --- | --- | --- |
| Lundi 11/01 | Carte commune, repères, vue d'un parcours, message masqué | A04, N09, A05 | C02, C07, I02 |
| Mardi 12/01 | Effets des valeurs, étages des bâtiments visités, bâtiments au zoom, palette | B02, B03 | C03, C05 |
| Mercredi 13/01 | Zoom, jour et nuit, changement de chaîne, accessibilité | C06, A06 | C04, C08 |
| Jeudi 14/01 | Tout est gelé, testé et répété | T02, O01 | T03, O01 |
| Vendredi 15/01 | Réserve et oral (date à préciser par les enseignants) | réserve | réserve |

Pas de nouvelle fonctionnalité après le mercredi 13/01 au soir.

## 4. La S49

Pas de SAÉ cette semaine-là, et **le code du projet commence en S50**. Nous préparons seulement :

| Qui | Préparation | Temps |
| --- | --- | --- |
| Les deux | Node, Git, Tailscale et OpenRouter prêts ; `node:sqlite` et `better-sqlite3` essayés | 1 h chacun |
| Les deux | Relire la spec, sections 2 à 7, et se l'expliquer | 1 h chacun |
| Les deux | Noter huit messages nouveaux chacun, puis essayer `p4` à la main dans le chat OpenRouter | 1 h chacun |
| M | Vrai couple de clés du nœud, clé publique envoyée aux six (O3, avant le 07/12) | 1 h |
| M | PC du nœud : heure automatique, pare-feu, nom Tailscale (O2) ; ★ carte du centre récupérée une fois pour toutes | 1 h |
| R | Décrire nos douze cas sur papier, au format commun de la v1.1 (suite : T01) | 1 h |
| R | ★ Trier environ 80 lieux, leur famille et leurs coordonnées | 1 h |

Soit 5 h chacun. Le dépôt privé commun (O1) se fait à six avant le vendredi 27/11. Pendant les vacances, du travail sur l'œuvre est possible mais n'est pas compté.

**[À CONFIRMER]** La v1.1 demande de déposer les cas le vendredi 04/12, donc de les calculer avec un script en S49, alors que le sujet place le code en S50. Demander aux enseignants si c'est accepté. Sans accord, nous demandons aux six de garder le lundi 07/12 pour nos cas.

## 5. L'oral

| Étape | Ce que nous montrons | Qui |
| --- | --- | --- |
| 1 | La carte vide, puis les balades déjà là | R |
| 2 | Un message écrit en direct, son bloc, sa balade | M |
| 3 | Le même message chez les deux autres nœuds | M |
| 4 | La carte qui change après plusieurs messages, puis un zoom | R |
| 5 | Un nœud coupé puis rallumé, son rattrapage | M |
| 6 | Un message masqué : la chaîne le garde, l'œuvre non | R |
| 7 | Le modèle d'IA qui a répondu, et une réponse refusée | R |

**Secours :** une chaîne de démonstration enregistrée, des résultats d'IA déjà en base et une vidéo du parcours. Garder du quota OpenRouter pour le 10/12 et l'oral. Chacun doit pouvoir expliquer les parties de l'autre.

## Avant vendredi 27/11

| Tâche | Qui propose | État |
| --- | --- | --- |
| Montrer le rendu C aux enseignants, question de la carte commune et de la balade individuelle | les deux | À faire |
| Dépôt privé commun (O1) | les six | À faire |
| Valider la liste des valeurs : huit, dont 10 familles de lieux | les deux | Fait, validé par M et R le 26/11 |
| Prompt `p4` (`p3` sans `ambiance`) à réessayer sur quelques messages | M | À faire |
| Écrire et essayer `p5` (lots de 10), dont un ordre caché glissé dans un lot | M | À faire |
| Valider la v1.1 de la spec (un membre par binôme), avec nos trois réserves | les deux | Fait le 26/11, déposée sur Moodle |
| Dossier : œuvre, dessin, données de carte, risques | M | À faire |
| Bible DA, huit éléments | R | À faire |
| Relire ce backlog, produire les PDF, déposer | les deux | À faire |

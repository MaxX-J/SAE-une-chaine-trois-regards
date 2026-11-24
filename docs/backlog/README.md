# Backlog et plan S50 / S2

Binôme 2 (noeud-b) : Maxens Sevilla (M) et Rahim Tamhaev (R).

**Version 1 du 24/11/2026, proposition à relire par les deux.** Rendu : vendredi 27/11, 17h, PDF ou lien.

## Hypothèses

- 6 heures utiles par personne et par jour. Les estimations sont les nôtres, aucune n'a été vérifiée.
- L'œuvre est la piste des **balades dans Béziers**, pas encore validée par les deux ni par les enseignants. Les tâches concernées portent un **★** : si l'œuvre change, elles changent, le reste tient.
- Les numéros de section renvoient à la spec commune 1.0. La spec impose que le nœud et l'application soient prêts pour la jonction : la chaîne passe donc **avant** l'œuvre.
- **[À CONFIRMER]** : à trancher à deux.

## 1. Le backlog

### Indispensable

| N° | Tâche | Terminée quand | h | Qui | Jour |
| --- | --- | --- | --- | --- | --- |
| N01 | Projet TypeScript, tests, lint, `.env.example` | `npm test` passe sur les deux machines | 1 | M | 07/12 |
| N02 | Texte canonique, NFC, SHA-256, Ed25519 | Les vecteurs de la section 2 sont retrouvés à l'identique | 3 | M | 07/12 |
| N03 | Base SQLite : chaîne, file, créneaux signés | Un redémarrage ne perd rien | 2 | M | 07/12 |
| T01 | Entrées des cas partagés 11 à 14 et 17 à 19 | Déposées dans le dépôt commun le soir même | 3 | R | 07/12 |
| A01 | Page d'écriture : consigne, avertissement, compteur, erreurs | Utilisable avec une API simulée, au clavier | 3 | R | 07/12 |
| N04 | Validation des messages, blocs et chaînes (3.1 à 3.3) | Les cas 1 à 14, 18 et 19 passent | 6 | M | 08/12 |
| N06 | Les cinq routes entre nœuds et leurs limites (6.3, 8.2) | Les cas 2, 17 et 22 passent | 4 | R | 08/12 |
| A02 | API de l'application : filtre, limite par visiteur, signature | Un message écrit arrive dans la file | 2 | R | 08/12 |
| N05 | Production de blocs à notre créneau (4.2) | Les cas 23 et 24 simulés passent | 3 | M | 09/12 |
| N08 | Envoi aux pairs et sondage de 10 s (6.4) | Le cas 25 passe entre deux instances locales | 2 | M | 09/12 |
| N07 | Choix de chaîne, fourche, rattrapage, SYNCING (5, 7) | Les cas 15, 16, 20, 21 et 26 passent en local | 5 | R | 09/12 |
| J01 | Essai à deux sur Tailscale | Un autre nœud et le nôtre ont la même tête | 2 | M, R | 09/12 |
| J02 | **Jonction à trois** : clés comparées, 26 cas, trois messages par binôme, coupure, redémarrage (10.3) | Les trois chaînes ont la même tête | 12 | M, R | 10/12 |
| I01 | Worker IA : appel, JSON strict, trois essais, statuts, modèle enregistré | Les cinq situations passent avec un faux serveur | 4 | R | 11/12 |
| A03 | Suivi du message en direct (SSE) : en attente, dans un bloc, lu | L'état se met à jour sans recharger | 2 | R | 11/12 |
| B01 | ★ Balade calculée depuis les valeurs et l'`id`, sur les vraies rues | Le même message donne toujours la même balade | 3 | M | 11/12 |
| C01 | ★ Carte de Béziers en fond et premier tracé | Une balade s'affiche, la mention OpenStreetMap est visible | 3 | M | 11/12 |
| I02 | Essais du prompt sur messages nouveaux, notés avant l'IA | Résultats et modèle écrits dans la charte | 3 | R | 11/01 |
| C02 | ★ Carte commune : rues et lieux changent avec les passages | 0, 10, 60 et 300 messages sont lisibles | 3 | R | 11/01 |
| A04 | ★ Vue d'un parcours : titre, étapes, distance | Le visiteur retrouve sa balade | 3 | M | 11/01 |
| N09 | Journaux, avertissement d'horloge, arrêt et reprise | Preuves gardées (3.4, 8.3), aucune double signature | 3 | M | 11/01 |
| C03 | ★ Style visuel de chaque famille de lieux | Chaque famille se reconnaît sans texte | 6 | R | 12/01 |
| B02 | ★ Effets des valeurs sur le tracé | Deux messages opposés donnent deux balades visiblement différentes | 4 | M | 12/01 |
| A05 | Message masqué, avant et après la chaîne | Ni texte ni effet visible, la chaîne est intacte | 2 | M | 12/01 |
| C04 | ★ Zoom à trois niveaux | Les détails apparaissent sans ralentir | 4 | R | 13/01 |
| C05 | ★ Palette fermée et légende | Conforme à la bible DA, lisible sans la couleur seule | 2 | R | 13/01 |
| C06 | L'œuvre suit un changement de chaîne ; repère « stable » après 3 blocs | Une fourche simulée recalcule la carte | 3 | M | 13/01 |
| A06 | Accessibilité : clavier, liste des balades, contraste, mouvement réduit | Contrôle axe sans erreur, parcours complet au clavier | 3 | M | 13/01 |
| T02 | Test de bout en bout avec faux serveur IA | Écriture, bloc, IA et balade passent automatiquement | 3 | M | 14/01 |
| T03 | Performance à 300 messages | Affichage fluide sur la machine de démonstration | 3 | R | 14/01 |
| O01 | Répétition de l'oral, scénario de secours | Deux passages complets, questions échangées | 6 | M, R | 14/01 |

Les heures d'une tâche à deux sont le total des deux personnes.

### En plus, si le temps le permet

| N° | Tâche | h | Priorité |
| --- | --- | --- | --- |
| P01 | ★ `moment` : lumière de l'aube, du jour, du soir et de la nuit | 3 | 1 |
| P02 | ★ `ambiance` : textures de pluie, vent, brume, saisons | 4 | 2 |
| P03 | Panneau d'état de la chaîne | 3 | 3 |
| P04 | ★ Carte-souvenir de la balade à télécharger | 3 | 4 |
| P05 | Animation d'apparition, désactivable | 2 | 5 |
| P06 | ★ Passage par un lieu cité dans le message | 3 | 6 |
| P07 | ★ `direction` et `temps` | 4 | 7 |

Si nous prenons du retard, nous coupons dans cet ordre : tout ce qui est en plus, puis le niveau de zoom le plus proche, puis une partie des familles de lieux. **Jamais** la chaîne, les messages masqués ni l'accessibilité de base.

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

La répartition validée (M le nœud, R l'IA et l'œuvre) est ajustée sur deux points, **[À CONFIRMER]** : R prend une partie du nœud avant le 10/12, car c'est le plus urgent et chacun doit savoir l'expliquer ; M prend une partie de l'œuvre ensuite. L'autre relit toujours avant fusion.

## 3. Le plan

### S50

| Soir | Ce qui fonctionne | M | R |
| --- | --- | --- | --- |
| Lundi 07/12 | Vecteurs retrouvés, base créée, cas partagés déposés, page d'écriture | N01, N02, N03 | T01, A01 |
| Mardi 08/12 | Le nœud valide messages et blocs et répond sur ses cinq routes | N04 | N06, A02 |
| Mercredi 09/12 | Production et rattrapage en local, essai réel à deux | N05, N08, J01 | N07, J01 |
| **Jeudi 10/12** | **Les trois nœuds ont la même chaîne** | J02 | J02 |
| Vendredi 11/12 | Parcours complet : message, bloc, IA, première balade | B01, C01 | I01, A03 |

T01 a besoin de N02 : M commence par N01 et N02, R par A01.

### S2

| Soir | Ce qui fonctionne | M | R |
| --- | --- | --- | --- |
| Lundi 11/01 | Carte commune et vue d'un parcours | A04, N09 | I02, C02 |
| Mardi 12/01 | Familles de lieux, effets des valeurs, message masqué | B02, A05 | C03 |
| Mercredi 13/01 | Zoom, palette, changement de chaîne, accessibilité | C06, A06 | C04, C05 |
| Jeudi 14/01 | Tout est gelé, testé et répété | T02, O01 | T03, O01 |
| Vendredi 15/01 | Réserve et oral (date à préciser par les enseignants) | réserve | réserve |

Pas de nouvelle fonctionnalité après le mercredi 13/01 au soir.

## 4. La S49

Pas de SAÉ cette semaine-là, et **le code du projet commence en S50**. Nous préparons seulement :

| Qui | Préparation | Temps |
| --- | --- | --- |
| Les deux | Node, Git, Tailscale et OpenRouter prêts ; `node:sqlite` et `better-sqlite3` essayés | 1 h chacun |
| Les deux | Relire la spec, section 2 à 7, et se l'expliquer | 1 h chacun |
| M | Décrire les cas 11 à 14 et 17 à 19 sur papier ; vérifier l'heure automatique et le pare-feu du PC du nœud | 2 h |
| M | ★ Récupérer une fois pour toutes la carte du centre (rues, bâtiments, eau, parcs) | 1 h |
| R | ★ Trier environ 80 lieux, leur famille et leurs coordonnées | 2 h |
| R | ★ Dessiner à la main un modèle par famille | 2 h |
| R | Noter une quinzaine de messages nouveaux pour tester l'IA, avant de voir ses réponses | 1 h |

**[À CONFIRMER]** La spec place l'essai « seul » en S49 et début de S50, le sujet place le code en S50 : demander aux enseignants si préparer les vecteurs avec un script en S49 est accepté. Sans accord, ils sont faits le lundi 07/12.

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
| Valider la piste de Béziers et poser la question de la carte commune aux enseignants | les deux | À faire |
| Valider la liste des valeurs, dont le nombre de familles de lieux (8 ou 10) | les deux | À faire |
| Prompt `p3`, grille des nouvelles valeurs, charte | M | À faire |
| Dossier : œuvre, dessin, données de carte, risques | M | À faire |
| Bible DA, huit éléments | R | À faire |
| Relire ce backlog, produire les PDF, déposer | les deux | À faire |

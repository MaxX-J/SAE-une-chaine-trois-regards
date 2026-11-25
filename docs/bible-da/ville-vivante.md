# La ville vivante : quelle valeur fait quoi

**Proposition du 25/11/2026, à valider par les deux.** Elle réunit l'idée de MaxX-J et withRen (passants, décor, lumière) et les valeurs de l'IA. Rien n'est codé.

La ville change **par quartier**. Un quartier regarde les 20 derniers messages passés chez lui : chaque nouveau texte modifie donc ce que les précédents avaient fait.

| Valeur | Dans la balade d'un visiteur | Dans la ville commune | Priorité |
| --- | --- | --- | --- |
| `lieu`, `lieu_secondaire` | Étapes | Bâtiments réveillés | Indispensable |
| `emotion` | Couleur du tracé | Couleur des lumières et des toits ; plus tard, posture et vêtements des passants | Indispensable, passants en plus |
| `valence` | Titre et fond | **Jour, crépuscule ou nuit du quartier** | Indispensable |
| `intensite` | Force de la couleur | Plus tard, densité du décor | Indispensable, décor en plus |
| `energie` | Longueur | Plus tard, nombre et allure des passants | Indispensable, passants en plus |
| `tension` | Tracé souple à très cassé, sans quitter la rue ([exemples](palette.md)) | Lumière douce ou dure, ombres plus longues | Indispensable pour le tracé |
| `absurdite` | Sort des rues | Un détail incongru, rare | Indispensable pour le tracé |
| `ambiance` | Texture du parcours | Météo et saison des arbres | Indispensable, en version simple |

## Jour et nuit : la `valence` par quartier

Idée de MaxX-J. On prend la moyenne de `valence` des 20 derniers messages du quartier :

| Moyenne | Quartier |
| --- | --- |
| 0,12 ou plus | Jour |
| Entre -0,12 et 0,12 | Crépuscule (les versions jour et nuit superposées) |
| -0,12 ou moins | Nuit |
| Aucun message | Jour |

Seuils *proposés* après l'essai en rendu C : avec 0,25, presque tout restait au crépuscule.

- La carte mêle donc des quartiers de jour et de nuit, et un nouveau texte peut **rallumer ou éteindre** un quartier.
- La nuit, les **fenêtres allumées comptent les messages** du quartier (accord de MaxX-J).
- Le visiteur peut forcer le jour partout, pour lire plus facilement.

`moment` n'est alors plus utile : la nuit ne peut pas dépendre de deux valeurs. **Décidé par MaxX-J le 25/11 : retirer `moment`, reprendre `valence`**, déjà définie et testée (withRen : à confirmer). `mot` est retirée le 25/11 par MaxX-J : neuf valeurs. Le titre d'une balade est composé par le code.

## Garde-fous

- **Pas de lumière qui clignote vite.** Un lampadaire « qui grésille » est une variation lente, coupée si le visiteur demande moins de mouvement. Jamais plus de trois éclairs par seconde (WCAG 2.3.1).
- L'émotion ne se lit pas seulement à la couleur : la liste accessible des balades l'écrit.
- Les passants sont des silhouettes simples, sans origine ni personne reconnaissable. Une émotion n'est jamais liée à un âge, un genre ou une apparence.
- Aucun détail absurde dans un lieu de culte, un cimetière ou un lieu de mémoire.
- Nombre de passants limité dans la zone visible, images légères : le poids reste le premier risque.
- Tout se calcule depuis la chaîne et l'`id` : même chaîne, même ville. Un message masqué perd son effet.

## Ordre de réalisation

1. Tracés, couleurs, jour et nuit par quartier
2. Fenêtres comptées, `ambiance` simple
3. Arbres et mobilier
4. Passants
5. Détails absurdes

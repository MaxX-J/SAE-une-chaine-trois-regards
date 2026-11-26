# La ville vivante : quelle valeur fait quoi

**Version du 26/11/2026.** Proposition du 25/11 (idée de MaxX-J et withRen : passants, décor, lumière), mise à jour avec les choix de MaxX-J du 26/11, **à valider par withRen**. Rien n'est codé.

**Une seule chaîne** : chaque balade part de la dernière étape de la précédente. La ville change aussi **par quartier** : un quartier regarde les 20 derniers messages passés chez lui, et chaque nouveau texte modifie ce que les précédents avaient fait.

| Valeur | Dans la balade | Dans la ville commune | Priorité |
| --- | --- | --- | --- |
| `lieu`, `lieu_secondaire` | Étapes | Les bâtiments où l'on s'arrête gagnent des étages | Indispensable |
| `emotion` | Couleur et motif du tracé, couleur des rues traversées | Émotion dominante du quartier : sol, toits, saison des arbres ; plus tard, vêtements des passants | Indispensable, passants en plus |
| `valence` | Titre | **Jour, crépuscule ou nuit du quartier** | Indispensable |
| `intensite` | Force de la couleur | Plus tard, densité du décor | Indispensable, décor en plus |
| `energie` | Nombre d'étapes | Plus tard, nombre et allure des passants | Indispensable, passants en plus |
| `tension` | Tracé souple à zigzag serré, toujours dans la rue | Lumière douce ou dure, ombres plus longues | Indispensable pour le tracé |
| `absurdite` | Un objet incongru près d'une étape (piano, baignoire, taureau, poisson volant) | Il reste dans la ville | En plus |

`ambiance` est retirée (MaxX-J, 26/11) : il reste huit valeurs.

## Jour et nuit : la `valence` par quartier

Idée de MaxX-J, gardée le 26/11. On prend la moyenne de `valence` des 20 derniers messages du quartier :

| Moyenne | Quartier |
| --- | --- |
| 0,12 ou plus | Jour |
| Entre -0,12 et 0,12 | Crépuscule (les versions jour et nuit superposées) |
| -0,12 ou moins | Nuit |
| Aucun message | Jour |

Seuils venus de l'essai en rendu C : avec 0,25, presque tout restait au crépuscule.

- La carte mêle des quartiers de jour et de nuit, et un nouveau texte peut **rallumer ou éteindre** un quartier.
- La nuit, les **fenêtres allumées comptent les messages** du quartier (accord de MaxX-J).
- Pas d'interrupteur « toujours de jour » (retiré le 26/11) : l'humeur du quartier est écrite.

## L'émotion du quartier

L'émotion la plus fréquente des 20 derniers messages du quartier (à égalité, la plus récente) :

- **Sol et toits** de tout le quartier, en lumière (choix de MaxX-J le 26/11). Les bâtiments visités gardent leur teinte chaude, ce qui les détache.
- **Arbres** *(proposé)* : joie et surprise en fleurs, neutre en été, colère et dégoût en automne, tristesse et peur en hiver. Aucune vraie date : la saison vient de l'émotion (MaxX-J, 26/11).

## Les bâtiments visités

Une étape sur un bâtiment est une visite. Le bâtiment gagne **des étages** (assets à prévoir par withRen), jusqu'à un plafond, prend une teinte chaude et allume ses fenêtres. Cimetières, nature et eau ne grandissent pas. Un message masqué ne compte plus.

## Garde-fous

- **Pas de lumière qui clignote vite.** Un lampadaire « qui grésille » est une variation lente, coupée si le visiteur demande moins de mouvement. Jamais plus de trois éclairs par seconde (WCAG 2.3.1).
- L'émotion ne se lit pas seulement à la couleur : la liste accessible des balades l'écrit.
- Les passants sont des silhouettes simples, sans origine ni personne reconnaissable. Une émotion n'est jamais liée à un âge, un genre ou une apparence. Leurs vêtements reprennent exactement les teintes des émotions.
- Aucun objet incongru dans un lieu de culte, un cimetière ou un lieu de mémoire.
- Nombre de passants limité dans la zone visible, images légères : le poids reste le premier risque.
- Tout se calcule depuis la chaîne et l'`id` : même chaîne, même ville. Un message masqué perd son effet ; un volet fermé reste dans le quartier où il passait.

## Ordre de réalisation

1. Chaîne, tracés, rues colorées, jour et nuit par quartier
2. Sol et toits du quartier, fenêtres comptées
3. Étages des bâtiments visités
4. Arbres et mobilier
5. Passants
6. Objets incongrus

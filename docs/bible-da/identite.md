# Symbole, typographie et design system

**BROUILLON v1 du 25/11/2026, propositions à choisir à deux.** Planche : [Figma, page « Symbole, typographie, design system »](https://www.figma.com/design/ryY2ksOgkdLQXyIwtDPPKw/Sans-titre?node-id=25-2) (accès selon le partage du fichier). Couleurs : [palette](palette.md).

## Le symbole

| Piste | Idée | Pour | Contre |
| --- | --- | --- | --- |
| **A. Le B en balade** (recommandée) | Un seul trait dessine le B de Béziers. Ses trois étapes, carré, rond et triangle, sont les trois nœuds | Suit les règles de l'œuvre : il prend la couleur, le motif et la forme d'une vraie balade | Devient fouillis à tension 1 |
| B. La fenêtre traversée | Une fenêtre (un message) traversée par un trajet | Très lié à l'œuvre | Moins net en petit |
| C. L'épingle habitée | Une épingle avec une fenêtre | Se comprend tout de suite | Ressemble à toutes les cartes |

**Déclinaisons de A :** sept émotions (couleur et motif), jour, crépuscule et nuit, trois tensions, masqué, une seule couleur, inverse, et de 16 à 96 px. À 32 px et moins, les étapes disparaissent.

## La typographie

| Famille | Rôle | Pourquoi |
| --- | --- | --- |
| Bricolage Grotesque | Titres | Ronde, un peu irrégulière, comme une enseigne de rue |
| Atkinson Hyperlegible Next | Textes et interface | Dessinée pour la lecture malvoyante : lettres et chiffres qui ne se confondent pas |
| JetBrains Mono | Empreintes, identifiants | Chasse fixe, comparaison caractère par caractère |

Tailles : 64, 36 et 24 pour les titres, 18 pour les textes, 15 pour les détails, jamais moins.

**Le texte des messages reste lisible**, dans un panneau. Sur la carte, aucun mot : jamais de texte en texture.

## Le design system

| Composant | Ce qu'il fait |
| --- | --- |
| Bouton | Principal et secondaire ; repos, focus, inactif ; 48 px de haut |
| Champ message | Vide, focus, erreur ; compteur de points de code |
| Statut | En attente, dans un bloc, lue par l'IA, stable, masquée : un signe et un mot |
| Carte balade | Titre composé par le code, émotion écrite et motif, message, étapes, distance, empreinte |
| Avertissement | Non effaçable, partagé, envoyé à une IA |
| Aide | 3114, 15, 112 |
| Légende | Couleur, motif et nom de chaque émotion |
| Quartier | Humeur écrite, car la lumière ne suffit pas |
| Interrupteur | Toujours voir de jour |
| Zoom | Trois boutons de 48 px |

Fondations dans Figma : 15 couleurs d'interface, 6 espacements, 3 rayons et 8 styles de texte. Principes : contraste AA, focus visible, la couleur jamais seule.

## À décider à deux

1. Piste A, B ou C ?
2. Les trois familles de caractères.
3. Vérifier les contrastes des composants et les tester à la taille réelle.
4. Écrans complets : écrire, suivre, carte, balade.

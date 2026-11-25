# Symbole, typographie et design system

**BROUILLON v1 du 25/11/2026, propositions à choisir à deux.** Planche : [Figma, page « Symbole, typographie, design system »](https://www.figma.com/design/ryY2ksOgkdLQXyIwtDPPKw/Sans-titre?node-id=25-2) (accès selon le partage du fichier). Couleurs : [palette](palette.md).

## Le symbole

**v2, le pâté de maisons.** Un *bloc* de la chaîne devient un *bloc* de maisons de Béziers : quatre cases sur quatre, en 2,5D, traversées par une balade.

Planche de construction : [Figma](https://www.figma.com/design/ryY2ksOgkdLQXyIwtDPPKw/Sans-titre?node-id=33-91). Méthode vue avec Visit Nordkyn (Neue) : une idée, un système fixe, des zones, puis la donnée.

| Fixe | Ce qui le change | Donnée |
| --- | --- | --- |
| Grille de 4 × 4, hauteur limitée | | |
| Entrée à gauche, sortie à droite | Nombre de virages de la rue | `tension` |
| Zone haute derrière, zone basse devant la rue | Hauteur des maisons | `energie` |
| | Une maison quitte le sol | `absurdite` |
| | Couleur de la rue, seule couleur du signe | `emotion` |
| | Lumière : jour, crépuscule, nuit | `valence` |
| | Détail des maisons | `id` du message |

**Quand on le voit.** À la fin de l'attente, la personne découvre **le signe de sa balade** ; il reste sur sa carte et dans la liste. L'**emblème** (losange, et pâté « jour, joie ») est fixe : onglet, en-tête, accueil, documents. Pas de symbole sur la carte commune.

**À améliorer.** L'`id` change encore trop peu le signe : plus d'écart entre les maisons et plusieurs rues possibles par tension. `lieu` et `intensite` n'y sont pas. Version simplifiée (losange et trait) à 32 px et moins ; versions encre et inverse.

**Écarté :** la v1 (un B dessiné par le trait, une fenêtre traversée, une épingle), jugée ratée par MaxX-J et gardée dans Figma, à droite de la planche.

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
| Interrupteur | Toujours voir de jour : réglage personnel pour qui lit mal dans les quartiers de nuit, ne change pas l'œuvre des autres |
| Zoom | Trois boutons de 48 px |

Fondations dans Figma : 15 couleurs d'interface, 6 espacements, 3 rayons et 8 styles de texte. Principes : contraste AA, focus visible, la couleur jamais seule.

## À décider à deux

1. Le pâté de maisons, et l'emblème fixe.
2. Les trois familles de caractères.
3. Vérifier les contrastes des composants et les tester à la taille réelle.
4. Écrans complets : écrire, suivre, carte, balade.

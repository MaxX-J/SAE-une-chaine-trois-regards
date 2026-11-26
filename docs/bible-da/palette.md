# Palette de Béziers

**BROUILLON v3.1 du 26/11/2026.** Choix de MaxX-J le 26/11 marqués, à valider par withRen. Planche : [Figma v3](https://www.figma.com/design/ryY2ksOgkdLQXyIwtDPPKw/Sans-titre?node-id=20-2), v1 et v2 gardées à côté (accès selon le partage du fichier).

**L'idée :** la ville est la matière, calme ; l'émotion est la lumière posée dessus.

## Qui choisit quelle couleur

| Valeur | Rôle | Nombre |
| --- | --- | --- |
| `lieu` | Symbole et liseré du toit | 10 familles × 3 tons |
| `emotion` | Tracé et son motif, couleur des rues ; émotion dominante du quartier : sol, toits, saison des arbres ; vêtements des passants | 7 teintes |
| `intensite` | Force de la teinte | 5 crans |
| `tension` | Forme du tracé, souple à cassée | 5 crans |
| `valence` | Jour, crépuscule ou nuit du quartier | 3 lumières |

La couleur ne suffit jamais : symbole pour le lieu, émotion écrite dans la liste des balades.

## Émotions, cinq intensités

| `intensite` | joie | tristesse | colere | peur | surprise | degout | neutre |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | #F5DDAD | #C1C7D2 | #E7B9AF | #C5B7C9 | #B6D8D0 | #D9D9AF | #D9D3C9 |
| 0,25 | #F4CD82 | #98A8C3 | #DC8E86 | #A18CB2 | #87C5BF | #C2C686 | #C2BDB2 |
| 0,5 | #F3BE58 | #7089B4 | #D1645C | #7C609C | #57B3AE | #ACB45C | #ACA79C |
| 0,75 | #F2B134 | #4F6FA8 | #C8413A | #5E3C8A | #2FA3A0 | #9AA53A | #9A948A |
| 1 | #D69520 | #3A5C9E | #B73031 | #4D2D85 | #188F95 | #84912D | #747274 |

`peur` est plus foncée et `degout` plus clair qu'en v2 (proposition de withRen) : les assets des passants sont à mettre à jour. Écart de couleur (CIEDE2000) d'au moins 5 entre toutes les émotions aux crans 0,5, 0,75 et 1, en vue normale et dans trois daltonismes simulés (Machado 2009). Aux crans 0 et 0,25, des paires se confondent : le motif porte alors l'émotion.

### Le tracé : liseré et motif

De jour et au crépuscule, un liseré encre #1C2140 passe sous le tracé (contraste 10 sur la rue de jour, 6,4 au crépuscule). La nuit, pas de liseré.

| joie | tristesse | colere | peur | surprise | degout | neutre |
| --- | --- | --- | --- | --- | --- | --- |
| plein, épais | longs tirets | tirets courts | points | tiret et point | double trait | plein, fin |

Ces motifs sont des propositions.

### La tension : la forme du tracé

La couleur et le motif disent l'émotion, **la forme dit la tension** : plus elle monte, plus le tracé se casse et part dans tous les sens.

| `tension` | Forme |
| --- | --- |
| 0 | Souple, arrondie |
| 0,25 | Légèrement brisée |
| 0,5 | Zigzag net |
| 0,75 | Zigzag fort |
| 1 | Zigzag très serré, irrégulier |

- Les écarts viennent de l'`id` du message : toujours les mêmes.
- Le tracé reste toujours dans la largeur de la rue (MaxX-J, 26/11). `absurdite` ne déforme plus le tracé : elle pose un objet incongru.
- Les tirets sont découpés le long du tracé. Aux tensions fortes, ils se lisent moins bien : à tester à la taille réelle.
- Le tracé est fixe : aucun tremblement animé.

### La nuit

| | joie | tristesse | colere | peur | surprise | degout | neutre |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tracé | #FBE8C2 | #7C9FF2 | #DB847F | #9E8AB9 | #A8FEF0 | #9AA53A | #BDB9B3 |
| Contraste sur la rue (#393B4B) | 9,2 | 4,3 | 4,0 | 3,6 | 9,5 | 4,1 | 5,7 |
| Fenêtre | #FBD785 | #CAC3A8 | #EEB587 | #CFB49F | #C1D3A6 | #E1D387 | #E1CE9F |
| Contraste sur le mur sable (#5F5D67) | 4,7 | 3,7 | 3,6 | 3,3 | 4,0 | 4,3 | 4,2 |

- **Tracé** : chaque émotion est éclaircie à sa mesure. Écart d'au moins 10 entre toutes, dans les quatre visions simulées.
- **Fenêtre** : 30 % d'émotion, 70 % de lumière chaude (#FFE7A8). Elles se ressemblent, car elles servent à compter les messages.
- **Halo** : la nuit, couleur du tracé en transparence (remarque de withRen) ; de jour, émotion pleine. Décoratif.
- **Sol et toits du quartier** (MaxX-J, 26/11) : l'émotion la plus fréquente des 20 derniers messages du quartier, large et floue au sol, en teinte sur les toits (`--toit`, `--toit-force` des assets), plus légère le jour. Une seule émotion par quartier, pour que 300 émotions ne se mélangent pas. Force à régler à l'œil.
- **Bâtiments visités** : teinte chaude (fenêtre chaude #FFA957) sur la façade et fenêtres allumées. Entourés d'un quartier coloré, ils se lisent.
- **Sol de nuit** : papier #404253, place #3D3E4D, rue #393B4B, pavé #353646. Le mur se détache de la rue de 1,2 à 1,9 selon l'enduit, contre 1,02 avant sur le mur sable.

Calculé au cran 0,75, sur ces fonds. Seuil visé : 3 (WCAG 1.4.11).

### Beaucoup de balades

Une seule chaîne (MaxX-J, 26/11) : chaque balade part de la fin de la précédente.

- **Traînée** : les dernières balades sont nettes et s'estompent ; la plus récente est la plus forte, avec un point et un halo. Nombre à calibrer sur l'œuvre (12 est trop peu).
- **Rues** : une rue prend l'émotion de son dernier passage ; plus elle est empruntée, plus elle brille, en se tassant. Le ruban de couleurs, essayé par withRen, reste abandonné.
- **Retrouver sa balade** (retour de withRen) : lien vers l'`id` du message, donné après l'écriture, et liste accessible. La balade remonte au premier plan, même ancienne.

## Familles de lieux (ton moyen)

| culte | cimetiere | nature | art | commerce | savoir | fete | repere | habitat | eau |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| #B79AD6 | #8FA0B3 | #7FB069 | #E58FB1 | #E9A15B | #A6B8A0 | #F0746E | #C9A227 | #D8B08C | #6FB3D9 |

Le symbole porte le lieu : la couleur ne suffit pas, notamment en daltonisme. La grille lieu × émotion est retirée, ses cases étaient trop proches.

## Matières, de jour

| Groupe | Teintes |
| --- | --- |
| Enduits | #EFE5CF, #E2D2B2, #D9B07A, #D2B98E, #E3A48E, #C98B5E |
| Toits | #C46A43, #DB8F66, #9E4F33, #6E7C8F, #93A0B0, #BDB6AA |
| Volets et portes | #7E97A8, #9A94BC, #8FA98A, #4F6B55, #7D4A3A, #5B3A2A |
| Végétation | #7F9F55, #97A383, #5D7A48, #6F9152, #3D5A3C, #9A8A70 |
| Sol et eau | #F6F1E6, #E8DFCB, #D6CEBF, #BFB5A4, #7FB1BD, #4F8C9E |

Crépuscule : 38 % de #8A5672. Nuit : 66 % de #1C2140, sauf le sol (voir la nuit). Calculés, à retoucher à l'œil.

## Ambiances

Retirées avec la valeur `ambiance` (MaxX-J, 26/11).

## Lumières et interface

Fenêtre claire #FFE7A8, fenêtre chaude #FFA957, halo #FFCF86, encre et nuit #1C2140 (un seul jeton), nuit profonde #0D0E18, texte discret #5C5A66, papier #F6F1E6, erreur #A5322C, masqué #B8B4AB.

## À tester et à décider

Validés par MaxX-J le 26/11 : `peur`, `degout` et le liseré ; `eau` en bleu ciel et `savoir` en gris sauge ; `commerce` et `habitat` gardés malgré leur écart de 9,4. Les vêtements des passants reprennent exactement les teintes des émotions.

1. Prendre toutes les lumières (sol, toits, rues) dans cette palette.
2. Régler à l'œil l'opacité des voiles la nuit, adoucir la limite entre deux quartiers.
3. Essayer sur un vrai écran, avec trois quartiers voisins. « Masqué » sert de fond, jamais de texte ; le texte discret est à éviter la nuit.

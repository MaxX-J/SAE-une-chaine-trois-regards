# Palette de Béziers

**BROUILLON v2 du 25/11/2026, après le test de withRen, rien n'est validé.** Planches : [Figma v2](https://www.figma.com/design/ryY2ksOgkdLQXyIwtDPPKw/Sans-titre?node-id=17-2), la [v1](https://www.figma.com/design/ryY2ksOgkdLQXyIwtDPPKw/Sans-titre?node-id=5-2) est gardée à côté (accès selon le partage du fichier).

**L'idée :** la ville est la matière, calme ; l'émotion est la lumière posée dessus.

## Qui choisit quelle couleur

| Valeur | Rôle | Nombre |
| --- | --- | --- |
| `lieu` | Symbole et liseré du toit | 10 familles × 3 tons |
| `emotion` | Tracé, fenêtres, halo au sol | 7 teintes |
| `intensite` | Force de la teinte | 5 crans |
| `valence` | Jour, crépuscule ou nuit du quartier | 3 lumières |
| `ambiance` | Voile du parcours | 9 × 2 tons |

La couleur ne suffit jamais : symbole pour le lieu, émotion écrite dans la liste des balades.

## Émotions (reprises des passants)

| joie | tristesse | colere | peur | surprise | degout | neutre |
| --- | --- | --- | --- | --- | --- | --- |
| #F2B134 | #4F6FA8 | #C8413A | #7A5AA0 | #2FA3A0 | #7E8F3A | #9A948A |

Cette teinte est le cran 0,75. Crans plus faibles : mélange avec #F6F1E6 (68 % pour 0, 44 % pour 0,25, 20 % pour 0,5). Cran 1 : plus saturé (sauf `neutre`, plus foncé), voir Figma.

### La nuit seulement

Les teintes ci-dessus ne ressortent pas la nuit : contraste de 1,2 à 2,2 pour six émotions sur sept (constat de withRen, vérifié par calcul).

- **Fenêtre** : 30 % d'émotion, 70 % de lumière chaude (#FFE7A8). Elle reste claire, pour pouvoir compter les messages.
- **Tracé** : émotion éclaircie de 55 % de blanc.
- **Halo au sol** : émotion pleine, décoratif, il ne porte pas l'information seul.

| | joie | tristesse | colere | peur | surprise | degout | neutre |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fenêtre | #FBD785 | #CAC3A8 | #EEB587 | #D7BDA6 | #C1D3A6 | #D8CD87 | #E1CE9F |
| Contraste sur le mur sable de nuit (#5F5D67) | 4,7 | 3,7 | 3,6 | 3,6 | 4,0 | 4,0 | 4,2 |
| Tracé | #F9DCA4 | #B0BED8 | #E6AAA6 | #C3B5D4 | #A1D6D4 | #C5CDA6 | #D2CFCA |
| Contraste sur la rue de nuit (#5B5C6B) | 5,0 | 3,5 | 3,3 | 3,4 | 4,1 | 4,0 | 4,2 |

Seuil visé : 3, celui des éléments graphiques (WCAG 1.4.11). Calculé sur ces deux fonds et au cran 0,75 seulement. Les fenêtres se ressemblent : la nuit, l'émotion se lit surtout sur le tracé.

## Familles de lieux (ton moyen)

| culte | cimetiere | nature | art | commerce | savoir | fete | repere | habitat | eau |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| #B79AD6 | #8FA0B3 | #7FB069 | #E58FB1 | #E9A15B | #6FB3D9 | #F0746E | #C9A227 | #D8B08C | #0F4C5C |

Halo d'un lieu traversé : 35 % du lieu, 65 % de l'émotion.

## Matières, de jour

| Groupe | Teintes |
| --- | --- |
| Enduits | #EFE5CF, #E2D2B2, #D9B07A, #D2B98E, #E3A48E, #C98B5E |
| Toits | #C46A43, #DB8F66, #9E4F33, #6E7C8F, #93A0B0, #BDB6AA |
| Volets et portes | #7E97A8, #9A94BC, #8FA98A, #4F6B55, #7D4A3A, #5B3A2A |
| Végétation | #7F9F55, #97A383, #5D7A48, #6F9152, #3D5A3C, #9A8A70 |
| Sol et eau | #F6F1E6, #E8DFCB, #D6CEBF, #BFB5A4, #7FB1BD, #4F8C9E |

Crépuscule : 38 % de #8A5672. Nuit : 66 % de #1C2140. Calculés, à retoucher à l'œil.

## Ambiances (clair, soutenu)

| soleil | pluie | vent | brume | froid | chaleur | floraison | feuilles | neutre |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| #FFE3A3, #F2C35B | #9DB4C4, #5F7C92 | #D5E0DD, #A3B8B4 | #E3E1E2, #BDBBC4 | #DCEBF2, #A9C9DB | #F7C9A0, #E58D5A | #F6D3DC, #E79BB2 | #DDA35C, #A9632F | #F6F1E6, #E3DCCC |

## Lumières et interface

Fenêtre claire #FFE7A8, fenêtre chaude #FFA957, halo #FFCF86, nuit et encre #1C2140, nuit profonde #0D0E18, texte discret #5C5A66, papier #F6F1E6, erreur #A5322C, masqué #B8B4AB.

## À tester et à décider

1. Refaire le test de nuit avec tristesse, peur et colère, aux crans faibles aussi ; le jour et le crépuscule marchent.
2. `eau` passe de #4FB0B8 à #0F4C5C (pétrole) : elle était presque identique à `surprise`. À vérifier la nuit.
3. Adoucir la limite entre deux quartiers de lumière différente ; voile d'ambiance plus large et plus flou.
4. La grille lieu × émotion : des cases voisines se ressemblent beaucoup.
5. Contraste et daltonisme : daltonisme pas encore vérifié, surtout `colere` et `degout`. Liseré des toits et vraie portion de carte à tester.

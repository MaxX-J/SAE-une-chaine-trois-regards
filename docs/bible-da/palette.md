# Palette de Béziers

**BROUILLON v1 du 25/11/2026, rien n'est validé.** withRen fait un test avec. Planche complète, 253 échantillons : [Figma](https://www.figma.com/design/ryY2ksOgkdLQXyIwtDPPKw/Sans-titre?node-id=5-2) (accès selon le partage du fichier).

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

## Familles de lieux (ton moyen)

| culte | cimetiere | nature | art | commerce | savoir | fete | repere | habitat | eau |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| #B79AD6 | #8FA0B3 | #7FB069 | #E58FB1 | #E9A15B | #6FB3D9 | #F0746E | #C9A227 | #D8B08C | #4FB0B8 |

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

1. Les émotions doivent-elles être plus vives (joie, peur) ?
2. `surprise` et `eau` sont trop proches : en changer une.
3. Crépuscule plus rose ou plus orangé ; nuit un peu terne.
4. La grille lieu × émotion : des cases voisines se ressemblent beaucoup.
5. Contraste et daltonisme : pas encore vérifiés, surtout `colere` et `degout`.

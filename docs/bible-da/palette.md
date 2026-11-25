# Palette de Béziers

**BROUILLON v3 du 25/11/2026, après la review de withRen, rien n'est validé.** Planche : [Figma v3](https://www.figma.com/design/ryY2ksOgkdLQXyIwtDPPKw/Sans-titre?node-id=20-2), v1 et v2 gardées à côté (accès selon le partage du fichier).

**L'idée :** la ville est la matière, calme ; l'émotion est la lumière posée dessus.

## Qui choisit quelle couleur

| Valeur | Rôle | Nombre |
| --- | --- | --- |
| `lieu` | Symbole et liseré du toit | 10 familles × 3 tons |
| `emotion` | Tracé et son motif, halo au sol, légère teinte des fenêtres | 7 teintes |
| `intensite` | Force de la teinte | 5 crans |
| `tension` | Forme du tracé, souple à cassée | 5 crans |
| `valence` | Jour, crépuscule ou nuit du quartier | 3 lumières |
| `ambiance` | Voile du parcours | 9 × 2 tons |

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

Ces motifs sont des propositions. Un tracé absurde qui quitte les rues garde son motif : il ne doit pas être montré par des pointillés, comme dans les premières esquisses.

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
- Le tracé reste dans la largeur de la rue : il ne la quitte que si `absurdite` est forte. Ce sont deux effets différents.
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
- **Sol de nuit** : papier #404253, place #3D3E4D, rue #393B4B, pavé #353646. Le mur se détache de la rue de 1,2 à 1,9 selon l'enduit, contre 1,02 avant sur le mur sable.

Calculé au cran 0,75, sur ces fonds. Seuil visé : 3 (WCAG 1.4.11).

### Beaucoup de balades

Pas de moyenne des tracés : chaque balade garde sa forme. Principe accepté par les deux le 25/11, seuils à régler à l'œil.

- **Balades récentes, par quartier** (retour de withRen) : 4 séparées et nettes vues de loin, 12 au zoom. *Chiffres proposés.*
- **Balades plus anciennes** : elles se fondent dans la rue, qui s'épaissit avec les passages. La rue devient un **ruban découpé en tronçons de couleur**, proportionnels aux émotions : 60 % de joie donne 60 % de tronçons jaunes. *Proposé* : mélanger les couleurs donnerait un brun, et la seule plus fréquente effacerait les émotions rares (retour de withRen).
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

## Ambiances (clair, soutenu)

| soleil | pluie | vent | brume | froid | chaleur | floraison | feuilles | neutre |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| #FFE3A3, #F2C35B | #9DB4C4, #5F7C92 | #D5E0DD, #A3B8B4 | #E3E1E2, #BDBBC4 | #DCEBF2, #A9C9DB | #F7C9A0, #E58D5A | #F6D3DC, #E79BB2 | #DDA35C, #A9632F | #F6F1E6, #E3DCCC |

Vent, brume et froid se ressemblent : c'est le motif qui les sépare. La nuit, opacité nettement plus basse, à régler.

## Lumières et interface

Fenêtre claire #FFE7A8, fenêtre chaude #FFA957, halo #FFCF86, encre et nuit #1C2140 (un seul jeton), nuit profonde #0D0E18, texte discret #5C5A66, papier #F6F1E6, erreur #A5322C, masqué #B8B4AB.

## À tester et à décider

1. Valider `peur`, `degout` et le liseré sur une vraie rue.
2. Valider l'échange : `eau` en bleu ciel, `savoir` en gris sauge.
3. `commerce` et `habitat` restent proches (écart 9,4).
4. Régler à l'œil l'opacité des voiles la nuit, adoucir la limite entre deux quartiers.
5. Essayer sur un vrai écran, avec trois quartiers voisins. « Masqué » sert de fond, jamais de texte ; le texte discret est à éviter la nuit.

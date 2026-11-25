# Bâtiments de Béziers en relief (rendu B)

**BROUILLON du 25/11/2026**, à valider par MaxX-J et withRen. Pour le rendu B : la carte reste plate et les repères passent en relief 2,5D.

| Jour | Nuit |
| --- | --- |
| ![Planche jour](apercu/planche-jour.jpg) | ![Planche nuit](apercu/planche-nuit.jpg) |

Une rue composée uniquement d'assets génériques, pour montrer qu'ils s'assemblent :

![Une rue de Béziers, jour et nuit](apercu/scene-rue.jpg)

Les trois teintes de chaque générique : [planche-variantes.jpg](apercu/planche-variantes.jpg).

## Ce qu'il y a

| Dossier | Contenu | Fichiers |
| --- | --- | --- |
| `reperes/` | 10 repères dessinés sur mesure | 20 (jour + nuit) |
| `generiques/` | 10 types de bâtiments × 3 teintes | 60 (jour + nuit) |
| `vegetation/` | platane, cyprès, palmier, olivier, pin parasol, lampadaire | 12 |
| `manifest.json` | la liste de tous les assets, leur emprise en mètres et leurs couleurs | |

**Repères :** cathédrale Saint-Nazaire, hôtel de ville, Polygone, gare, Cimetière Vieux, arènes, halles, Pont-Vieux, écluses de Fonseranes, allées Paul-Riquet.

**Génériques :** maison de ville R+2 et R+3, maison étroite, immeuble à commerces, immeuble bourgeois XIXe (toit à la Mansart), maison d'angle, maison de faubourg, maison de maître avec jardin, résidence des années 60-70, chai viticole.

## Règles communes à tous les fichiers

- **Isométrie 2:1** : 1 m au sol = 10 px. Un point du monde `(x, y, z)` en mètres se place à l'écran en `px = (x − y) × 10`, `py = (x + y) × 5 − z × 11,2`.
- **Ancre** : le point `(0, 0)` du `viewBox` est le centre de l'emprise au sol. Pour poser un asset sur la carte, on place ce point sur la position projetée du bâtiment.
- **Lumière** : elle vient de la gauche. Face gauche éclairée, face droite à l'ombre, ombre portée vers la droite.
- **Jour / nuit** : chaque asset existe en deux versions. La nuit, les murs passent au bleu nuit, certaines fenêtres s'allument (au hasard, mais toujours les mêmes) et les vitrines, lampadaires et portes éclairent le sol.
- **Ordre d'affichage** : dessiner d'abord ce qui est loin, c'est-à-dire trier par `x + y` croissant (le coin avant de l'emprise).
- Fond transparent, aucun texte, aucune marque ni logo.

## Ce qui est fidèle, et ce qui ne l'est pas

Observé sur des photos (Google Images), la vue satellite de Google Maps et les fiches patrimoine, le 25/11 :

- **Ville :** enduits ocre, sable, rose saumon et crème ; volets persiennés bleu-gris, verts ou lavande ; toits en tuiles canal orangées et peu pentus ; génoises sous les toits ; immeubles XIXe en pierre de taille avec toits en zinc gris-bleu, lucarnes et balcons en fer.
- **Cathédrale :** façade fortifiée entre deux tours crénelées, grande rosace, portail ogival sous un gâble, mâchicoulis, clocher carré crénelé avec tourelles d'angle et campanile en fer. Les proportions sont simplifiées et le clocher est déplacé pour rester visible.
- **Hôtel de ville :** pierre de taille, avant-corps central, tour avec blason, horloge, balustrade à pots à feu et campanile en fer forgé. Le nombre de travées et le toit sont supposés.
- **Polygone :** gradins blancs, rue à ciel ouvert sous une pergola blanche et vitrée, rotonde avec un grand écran. L'écran est un dégradé sans texte.
- **Gare :** long bâtiment en pierre ocre clair, baies cintrées, pavillon central plus haut avec fronton et horloge, marquise sur les voies.
- **Arènes :** mur de brique à deux rangs d'arcades, pavillon d'entrée à bandes brique et pierre surmonté d'une tourelle.
- **Halles :** structure Baltard en fer, persiennes claires, soubassement en brique, lanterneau, portail en pierre.
- **Cimetière Vieux :** enclos, portail cintré à fronton, tombes blanches, chapelles, beaucoup de cyprès.
- **Inventé ou simplifié :** les mesures exactes, le nombre de baies, l'arrière des bâtiments, les arènes plus petites que les vraies, le kiosque et la statue des allées, le Pont-Vieux dessiné seul (sans la cathédrale au-dessus).

## Comment ils ont été faits

Les SVG sont produits par un petit script de dessin en Python, dans [`outil/`](outil). Ce n'est pas du code de l'application : il sert seulement à dessiner les assets. Il permet de changer une teinte, une hauteur ou l'éclairage, puis de tout régénérer :

```sh
cd docs/bible-da/assets/batiments/outil
python3 construire.py ..   # SVG + manifest.json
python3 planche.py ..      # pages HTML des planches
```

- `iso.py` : projection, lumière, couleurs jour/nuit, murs, toits, fenêtres, arbres.
- `generiques.py` : les bâtiments génériques et leurs teintes.
- `reperes.py` : les repères, un par fonction.

## Questions ouvertes

1. Le style vous va-t-il (niveau de détail, jour / nuit) ?
2. Faut-il un repère de plus (théâtre, Plateau des Poètes, stade, pont-canal de l'Orb, église de la Madeleine) ?
3. La nuit correspond-elle à une valeur (par exemple `valence` ou l'heure du message) ou à un réglage d'affichage ?
4. Les fenêtres allumées la nuit pourraient compter les messages d'un quartier.

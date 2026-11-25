# Bâtiments de Béziers en relief (rendu C)

**BROUILLON du 25/11/2026**, à valider par MaxX-J et withRen. Pour le rendu C (validé par withRen le 25/11) : toute la ville est en 2,5D, avec des repères détaillés, de jour et de nuit. Les bâtiments génériques remplissent la ville, les repères sont dessinés sur mesure.

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
| `vie/personnages/` | 11 poses de passants : 5 allures + 6 émotions | 22 |
| `vie/mobilier/` | poubelles, bancs, arbustes, potelets, feux, fontaine, vélo, terrasse, lampadaires éteint et grésillant, platane des 4 saisons, flaque, feuilles, pigeons, chat | 48 |
| `vie/incongrus/` | piano, baignoire, taureau, poisson volant | 8 |
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

## La vie de la carte (brouillon du 25/11)

![Gens, mobilier et incongrus](apercu/planche-vie-jour.jpg)

Trois rues de démonstration, générées par `outil/scenes.py` à partir de valeurs :

| Joie, énergie forte, printemps | Tristesse, énergie faible, pluie, nuit | Colère, tension forte, hiver, absurdité |
| --- | --- | --- |
| ![](apercu/scene-joie.jpg) | ![](apercu/scene-tristesse.jpg) | ![](apercu/scene-colere.jpg) |

**Personnages.** Ils mesurent environ 1,8 m (20 px). Leurs couleurs sont des variables CSS, avec une valeur par défaut : `--haut`, `--bas`, `--peau`, `--cheveux`, `--objet`. Pour les changer, il faut insérer le SVG dans la page (ou passer par `<use>`) : une balise `<img>` affiche toujours les couleurs par défaut. Les couleurs des émotions sont dans `manifest.json` (`couleurs_emotions`).

**Lampadaire grésillant.** Sa lumière varie lentement (cycle de 5 s, aucun éclair), et l'animation s'arrête si le visiteur a demandé moins de mouvement (`prefers-reduced-motion`).

### Quelle valeur change quoi

La correspondance qui fait foi est dans [`ville-vivante.md`](../../ville-vivante.md) (validée par withRen le 25/11, à confirmer par MaxX-J là où elle le demande). En résumé, pour ces assets : `valence` donne le jour, le crépuscule ou la nuit du quartier ; `emotion` la couleur des lumières et des toits, puis la pose et les vêtements des passants ; `energie` le nombre et l'allure des passants ; `intensite` la densité du décor ; `tension` une lumière plus dure ; `absurdite` un élément incongru, rare ; `ambiance` la météo et la saison des arbres ; `lieu` le mobilier.

Ce que les assets couvrent déjà pour `ambiance` : soleil (platane d'été), pluie (flaques, parapluies), floraison (printemps), feuilles (automne), froid (hiver). Il manque le vent, la brume et la chaleur.

## Réglages pour le code

![Réglages : fenêtres, toits et lumières](apercu/reglages.jpg)

Ces réglages ne marchent que si le SVG est inséré dans la page (pas avec une balise `<img>`). Si le même SVG est inséré plusieurs fois, il faut préfixer ses `id` à chaque fois (comme le fait SVGR), sinon toutes les copies prennent les couleurs de la première.

- **Même cadre jour et nuit.** Les deux versions d'un asset ont exactement le même `viewBox`. Pour le crépuscule, on peut donc superposer la nuit sur le jour avec une opacité de 0,5.
- **Fenêtres qui comptent les messages** (versions nuit). Chaque fenêtre est un groupe `class="fen"` avec un numéro `data-n` (0, 1, 2…), dans un ordre mélangé pour que les fenêtres allumées soient réparties sur la façade. Une fenêtre est allumée quand elle a aussi la classe `on`. Pour N messages : mettre `on` sur les fenêtres dont `data-n` est inférieur à N. Par défaut, environ 6 fenêtres sur 10 sont allumées. Les vitrines et les portes restent toujours éclairées.
- **Couleur des toits.** `--toit` (couleur) et `--toit-force` (de 0 à 1, 0 par défaut). La teinte garde l'ombre et la lumière du toit.
- **Couleur des lumières** (versions nuit). `--lumiere` et `--lumiere-bas` pour le dégradé des fenêtres, `--lueur` pour le halo.

## Optimisation

Les SVG sont allégés par `outil/opti.py` (traits fusionnés en chemins, nombres et couleurs raccourcis, dégradés inutiles retirés). Le rendu est identique et le poids baisse d'environ 60 % : les génériques passent de 5,8 Mo à 2,3 Mo, les repères de 2,4 Mo à 1,2 Mo. Un passant pèse environ 3 Ko.

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
python3 planche.py ..      # pages HTML des planches (dont planche-vie)
```

- `iso.py` : projection, lumière, couleurs jour/nuit, murs, toits, fenêtres, arbres.
- `generiques.py` : les bâtiments génériques et leurs teintes.
- `reperes.py` : les repères, un par fonction.
- `vie.py` : passants, mobilier, saisons et incongrus.
- `scenes.py` : assemble une rue à partir de valeurs (pour les démonstrations).
- `opti.py` : allège les SVG.

## Questions ouvertes

1. Le style vous va-t-il (niveau de détail, jour / nuit) ?
2. Faut-il un repère de plus (théâtre, Plateau des Poètes, stade, pont-canal de l'Orb, église de la Madeleine) ?
3. La nuit correspond-elle à une valeur (par exemple `valence` ou l'heure du message) ou à un réglage d'affichage ?
4. Les fenêtres allumées la nuit pourraient compter les messages d'un quartier.
5. Le tableau « quelle valeur change quoi » vous convient-il ?

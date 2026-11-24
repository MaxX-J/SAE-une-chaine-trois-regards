# Esquisses : balades dans Béziers

**BROUILLON du 24/11/2026. Ce ne sont que des esquisses**, faites pour choisir une direction. Ce n'est ni le style final, ni le code du projet, ni une décision. MaxX-J et withRen choisissent le 25/11.

Fond de carte : © les contributeurs OpenStreetMap, données sous licence ODbL.

## L'idée

Chaque message est une balade sur les vraies rues de Béziers. Chaque lieu visité colore les bâtiments autour de lui. Toutes les balades forment une seule carte.

## À choisir

| Version | Ce que c'est | Pour | Contre |
| --- | --- | --- | --- |
| **A. À plat** | Carte 2D vue du dessus | La plus simple et la plus lisible | Peu de relief |
| **B. Relief des lieux importants** | Carte plate, 31 bâtiments repères en 2,5D | On voit les tracés et les repères, travail limité | Le reste de la ville est plat |
| **C. Relief de toute la ville** | Les 11 725 bâtiments du secteur en 2,5D | La plus spectaculaire, surtout au zoom | Les bâtiments cachent une partie des tracés, plus lourde à afficher, plus longue à faire |

La 2,5D est un faux relief dessiné à plat : aucun modèle 3D, la caméra ne tourne pas.

Avis de Claude, à discuter : **B**, avec C en zoom si le temps le permet.

### A. À plat

| Vide | 10 messages | 10, un masqué |
| --- | --- | --- |
| ![Carte vide de Béziers](01-plat-vide.jpg) | ![Carte avec dix balades](02-plat-10.jpg) | ![La même carte, une balade retirée](03-plat-masque.jpg) |

| 60 messages | 300 messages | Zoom, 60 messages |
| --- | --- | --- |
| ![Carte avec soixante balades](04-plat-60.jpg) | ![Carte avec trois cents balades](05-plat-300.jpg) | ![Zoom sur le centre avec les symboles des lieux](06-plat-zoom.jpg) |

Une balade seule, avec son titre. La seconde est absurde : elle quitte les rues.

| ABSENCE | LOYER |
| --- | --- |
| ![Balade ABSENCE jusqu'au Cimetière Vieux](07-balade-absence.jpg) | ![Balade LOYER en lignes droites à travers les immeubles](08-balade-loyer.jpg) |

### B. Relief des lieux importants (60 messages)

![Béziers, seuls les lieux importants en relief](09-relief-reperes.jpg)

![Zoom sur les lieux importants en relief](10-relief-reperes-zoom.jpg)

### C. Relief de toute la ville (60 messages)

![Béziers, toute la ville en relief](11-relief-tout.jpg)

![Zoom sur la ville entière en relief](12-relief-tout-zoom.jpg)

## Ce qui est vrai, et ce qui ne l'est pas

- **Vrai :** rues, contours des bâtiments, cours d'eau, noms et places des lieux.
- **Inventé :** les messages et leurs valeurs. Dix sont écrits, les autres sont tirés au hasard. Aucune IA n'a été appelée.
- **Approximatif :** les hauteurs (quand OpenStreetMap ne donne pas les étages), les formes des repères (clocher, dôme, drapeau), le choix automatique des lieux.

## Défauts connus

- À 300 messages, la version à plat est chargée.
- Un seul cimetière dans la zone : beaucoup de messages tristes finiraient au même endroit.
- Les styles se limitent à des couleurs et des symboles simples. Les vrais styles par type de lieu restent à dessiner.
- `moment` et `ambiance` ne sont pas représentés.
- Les maisons sont des bâtiments pris au hasard : à remplacer par des quartiers, pour ne désigner aucun domicile.
- Palette de 10 familles × 7 émotions = 70 teintes, certaines trop proches.
- Les lieux ne sont pas triés à la main.

## Questions pour le choix

1. A, B ou C ?
2. Quels lieux importants garder (une trentaine) ?
3. Quel style pour chaque type de lieu ?
4. La carte commune et la balade individuelle conviennent-elles aux enseignants ?

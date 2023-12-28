# bramm-data-analysis

Rendu de projet de Géostatistiques effectué par Gaétan RIGAUT.

## Installation

⚠️ Le projet a été effectué avec python 3.11.6, je n'ai pas vérifié la compatibilité avec d'autres versions, mais j'imagine qu'*a minima* des versions ultérieures devraient fonctionner également ⚠️

#### Installation avec `pip`

Sauf erreur de ma part, les différentes librairies requises sont détaillées dans le fichier `requirements.txt`.

#### Installation avec `poetry`

Un fichier `poetry.lock` est défini à la racine du projet et devrait convenir pour une installation à l'aide de poetry.

## Données

Pour une utilisation comme tel, il est nécessaire de conserver dans le dossier `data` les trois sources de données suivantes :

- `Mines_2024.xlsx` : fichier contenant les données de mousse tel qu'il nous a été fourni, et disponible [ici](https://moodle.psl.eu/mod/resource/view.php?id=563618 "Lien Moodle du Jeu de données").
- `metropole.json` : fichier contenant le tracé de la frontière métropolitaine française, obtenu sur [github](https://github.com/gregoiredavid/france-geojson/blob/master/metropole.geojson "Lien vers le geojson avec la frontière de la France métropolitaine").
- `RMQS.csv` : fichier contenant les données RMQS modifié pour intégrer les données de longitude et latitude au format WGS84 (format standard), disponible [ici](https://cloud.minesparis.psl.eu/index.php/s/ttyZNBPSmR6JDxe "Lien de Téléchargement des Données RMQS") si nécessaire.

## Notebooks

Les différents notebooks à consulter se trouvent dans le dossier `notebooks` à la racine du projet.

L'ordre conseillé pour les parcourir est le suivant :

- [kriging.ipynb](notebooks/kriging.ipynb "Krigeage Uni-Variable")
- [rmqs_moss_kriging.ipynb](notebooks/rmqs_moss_kriging.ipynb "CoKrigeage sur les données de mousse et RMQS")
- ([spatial_division](notebooks/spatial_division.ipynb "Détail de la génération de grilles pour le krigeage"), éventuellement, mais pas fondamentalement utile)

## Code

Les divers fonctions et objets définis dans cet projet se situent dans le dossier `src/bramm_data_analysis`.

# Peuplement de l'ontologie des adresses
Peuplement de l'ontologie de modélisation des adresses via différentes source

## Dossier `sources`
Chaque dossier dans `sources` permet de peupler l'ontologie selon un type de source donnée :
* `ban_01343` contient des adresses issues de la [BAN (Base Nationale Adresse)](https://adresse.data.gouv.fr/base-adresse-nationale) d'une petite commune ; 
* `ban_paris` contient des adresses de Paris issues de la [BAN (Base Nationale Adresse)](https://adresse.data.gouv.fr/base-adresse-nationale) ;
* `paris_directories` contient des adresses de Paris issues des annuaires de commerces. Contrairement aux données de la BAN, les adresses ont chacune des structures différentes ;
* `praha_osm` contient des adresses du centre de Prague issues de [OSM (OpenStreetMap)](https://www.openstreetmap.org/) ;
* `taito_japan` contient des adresses du centre de Tokyo issues des données gouvernementales japonaises.

Pour peupler l'ontologie pour chaque dossier, il faut ouvrir le notebook `{nom_dossier}.ipynb` et lancer le script.

⚠️ Avant d'exécuter les scripts, il faut s'assurer que deux logiciels sont installés et ils devront tourner durant le processus :
* [Ontotext Refine](https://www.ontotext.com/products/ontotext-refine/) (ou OntoRefine) qui permet d'automatiser la conversion de données textuelles en un graphe de connaissances. Dans la section des variables globables (voir ci-dessous), deux variables sont liées au logiciel :
  * `ontorefine_cli` : chemin absolu de l'interface en ligne de commande (CLI) d'OntoRefine. Pour trouver ce chemin, il suffit de cliquer sur le bouton `Open CLI directory` présent sur l'interface de lancement du logiciel. Cela vous renvoie vers le dossier contenant la CLI dont le nom est `ontorefine-cli`.
  * `ontorefine_url` : l'URL de l'application web.  Pour trouver cette valeur, il suffit de cliquer sur le bouton `Open Refine web application` présent sur l'interface de lancement du logiciel. La valeur à associer à `ontorefine_url` est l'url à laquelle on enlève `/projects`.
* [GraphDB](https://graphdb.ontotext.com/) qui permet de stocker et de travailler sur des graphes de connaissance. Une variable est associée au logiciel : `graphdb_url` qui est l'URL de l'application web. Le procédé est similaire à celui de `ontorefine_url` pour trouver sa valeur.

![Interface d'OntoRefine avec les boutons \`Open Refine web application\` et \`Open CLI directory\`](./img/interface_ontorefine.png)

## Dossier `code`
Le dossier `code` comporte plusieurs fichiers python qui décrivent des fonctions permettant de faire le processus indiqué dans un notebook. 

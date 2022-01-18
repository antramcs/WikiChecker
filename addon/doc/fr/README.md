# WikiChecker

## Moteur de recherche rapide des articles dans Wikipedia.

### Introduction.

L'extension WikiChecker pour NVDA permet aux utilisateurs de consulter de forme rapide  et accessible n'importe quel article faisant référence à un terme en concret dans la page de [Wikipedia](https://wikipedia.org/).

Wikipedia   est un projet  de création d'une encyclopédie libre sur Internet, où chacun peut y collaborer  avec ses connaissances sur n'importe quel thème pour créer une base de données avec toute la sagesse humaine. Il est administré par la Wikimedia Foundation, une organisation à but non lucratif dont le financement est basé sur des dons. Ses  plus de 56 millions d'articles dans 321 langues ont été rédigés conjointement par des volontaires du monde entier, ce qui représente plus de 2000 millions d'éditions,  et permet à quiconque de rejoindre le projet pour les éditer, à moins que la page se trouve protégée contre le vandalisme pour éviter des problèmes ou des différends.


### Mode d'utilisation.

La manière d'utiliser WikiChecker est très simple. Il suffit de suivre les trois prochaines étapes:

1. Appuyer sur le raccourci clavier ou combinaisons de touches  assignées, que précédemment il a dû être configuré dans la boîte de dialogue Geste de Commandes, dans la catégorie WikiChecker.

2. Entrer le terme souhaité à rechercher dans la zone d'édition disposée à cet effet et exécuter la consultation dans Wikipedia en appuyant sur Entrée, ou en appuyant sur le bouton "Rechercher".

3. Sélectionner le résultat qui nous intéresse et appuyer sur Entrée sur celui-ci, ou en appuyant sur le bouton "Lire l'article".

Une fois ces trois étapes effectuées, l'article s'ouvrira dans la fenêtre du navigateur que nous avons par défaut assigné.

Avertissement: L'extension par défaut établit la langue prédéfinie dans NVDA en tant que langue de  consultation dans WikiChecker. Si vous souhaitez rechercher l'article dans une autre langue, il suffira de le sélectionner dans la liste des langues disponibles. Si la langue par défaut n'est pas trouvée dans NVDA parmi les langues disponibles, lors de l'exécution de l'extension nous serons positionnés sur la  liste pour choisir une. Si nous n'effectuons pas cette étape, les recherches ne seront pas effectuées.


### Raccourcis clavier.

Il n'y a pas des combinaisons de touches ou des raccourcis clavier pré-assignées, de sorte que chaque utilisateur puisse configurer celle qui convient le mieux pour chaque cas, afin de ne pas interférer avec d'autres extensions. Pour l'assigner, l'utilisateur doit aller dans le menu NVDA,  Préférences, Gestes de commandes, et une fois dedans, trouvez la catégorie WikiChecker, et assigner une combinaison qui l'intéresse.

Une fois dans l'interface de l'extension, il existe plusieurs combinaisons de touches pré-assignées, afin que nous puissions nous déplacer rapidement entre les différents éléments de celle-ci:

* Alt + R: Nous nous positionnons sur la zone d'édition pour écrire le terme à rechercher.
* alt + C: Nous nous positionnons sur le bouton "Rechercher" pour exécuter la consultation dans Wikipedia.
* Alt + L: Nous nous positionnons sur la  liste des langues disponibles, afin que nous puissions choisir une langue autre que celle de la valeur par défaut, ou, s'il n'y a pas la langue par défaut dans NVDA, de sorte que nous en choisissons une dans laquel effectuer la recherche.
* Alt + A: Nous nous positionnons sur la liste des articles disponibles, de sorte que nous choisissions l'un des résultats lancés par la consultation dans Wikipedia.
* Alt + I: Nous nous positionnons sur le bouton "Lire l'article" pour ouvrir l'article dans le navigateur.


## Journal des changements.

### Version 1.2.

* Ajout de deux boutons, "Rechercher" et "Lire l'article", pour les utilisateurs qui sont les plus habitués à utiliser ces éléments, de sorte qu'ils  ne se sentent pas désorientés lors de l'utilisation de l'interface.
* Ajouté les traductions en portugais et français. Merci à Ângelo Miguel Abrantes et Rémy Ruiz respectivement.
* Modifié la liste des langues pour être affiché en anglais, de sorte qu'elles puissent être utilisées par les utilisateurs qui ne comprennent pas la langue espagnole. Ce changement est expérimental et peut être modifié dans des versions ultérieures.


### Version 1.1.

* Ajout de la possibilité que WikiChecker fonctionne sur des ordinateurs travaillant sous des serveurs proxy.
* Ajout d'une vérification supplémentaire qui empêche lancer la consultation à Wikipedia si aucune des langue a été choisie parmi celles disponibles préalablement.
* Ajout d'une vérification supplémentaire dans le chargement des langues disponibles afin d'éviter un dysfonctionnement  de l'extension.
* Correction des erreurs et optimisation du code depuis la version précédente.


### Version 1.0.

* Version initiale.

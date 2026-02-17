# État de l'Art : Efficacité Énergétique Logicielle

Ce document présente l'étude théorique préalable à l'implémentation de notre projet. Il s'appuie sur les références académiques et techniques fournies par l'encadrant.

## 1. Introduction et Enjeux
L’émergence de l’urgence climatique impose aujourd’hui une transformation profonde des pratiques de l’ingénierie logicielle, faisant de l’éco-conception un impératif technique plutôt qu’une simple option de performance. Alors que le secteur numérique représente une part croissante de la consommation électrique mondiale, le développement moderne doit désormais intégrer les enjeux environnementaux dès la phase de conception pour limiter l'empreinte matérielle et énergétique des services numériques. L'enjeu principal est d'optimiser l'efficacité énergétique, c'est-à-dire de réduire la quantité d'énergie nécessaire (exprimée en Joules) pour accomplir une tâche précise, appelée Unité Fonctionnelle.

En adoptant le langage Rust, ce projet s'inscrit dans une démarche de maîtrise fine du matériel, où chaque cycle CPU économisé et chaque accès à la mémoire vive (RAM) optimisé contribuent directement à l'amélioration du bilan énergétique global.

L'objectif scientifique de ce projet est d'analyser les mécanismes qui régissent la consommation énergétique logicielle en s'appuyant sur des cas d'étude concrets, tels que le calcul d'un produit matriciel. Cette approche permet de démontrer qu'à résultat identique, des choix d'implémentation et de gestion des ressources différents modifient radicalement la quantité de Joules consommés. Il s'agit d'établir une méthodologie permettant d'identifier le compromis optimal entre le temps d'exécution et la puissance électrique appelée, plaçant ainsi le développeur comme un acteur central de la sobriété numérique.

## 2. Méthodologie d'évaluation de la consommation énergétique
Dans ce chapitre, nous allons étudier comment mesurer et évaluer la consommation énergétique d’un programme lors de son exécution. Cette étape est indispensable car on ne peut pas savoir si un programme est bien optimisé sans le mesurer concrètement et voir combien il a réellement consommé.

Nous allons structurer cette étude en trois points : tout d'abord, nous comparerons la pertinence d'une mesure logicielle via PowerAPI par rapport à une mesure physique. Ensuite, nous définirons un protocole d'isolation strict pour garantir que seule la consommation de notre application est comptabilisée. Enfin, nous détaillerons les métriques de calcul (Joules, Watts, Temps) qui nous permettront de quantifier l'efficacité énergétique de nos développements.

### 2.1 La Mesure : Physique vs Logicielle
Dans cette section, nous comparons deux approches pour quantifier la dépense énergétique d'un système informatique afin de justifier notre choix méthodologique.
* **La Mesure Physique (Wattmètre) :** Cette méthode consiste à placer un appareil de mesure entre la prise de courant et l'alimentation de l'ordinateur. Bien qu'elle donne la consommation réelle totale, elle manque de précision pour l'analyse logicielle car elle comptabilise l'ensemble des composants (écran, ventilateurs, périphériques USB, etc.), créant un "bruit" qui masque la consommation spécifique du programme étudié,rendant difficile l'isolation de l'impact réel du code.
* **La Mesure Logicielle (PowerAPI) :** À l'inverse, cette approche permet d'isoler la consommation des composants internes sollicités par le calcul, comme le processeur (CPU) et la mémoire vive (RAM). Nous avons choisi d'utiliser **PowerAPI**, un outil de référence qui agit comme un wattmètre logiciel pour estimer la consommation avec une granularité fine en ciblant spécifiquement le processus de notre application. Cette méthode offre l'avantage de suivre l'évolution de la consommation en temps réel et d'obtenir des données exploitables pour comparer différentes versions d'un algorithme sans les interférences liées au matériel périphérique.

### 2.2 Le Protocole d'Estimation (L'Isolation)
Pour obtenir des mesures fiables avec PowerAPI, il est impératif de mettre en place un protocole d'isolation strict. L'objectif est de garantir que l'énergie consommée et mesurée provient exclusivement de l'exécution de notre algorithme et non de tâches de fond du système d'exploitation.
* **Nettoyage de l’environnement :** Avant chaque session de mesure, toutes les applications non essentielles (navigateurs web, outils de communication, mises à jour automatiques) doivent être fermées. Cela permet de réduire la sollicitation inutile du processeur et de la mémoire vive, limitant ainsi le "bruit" numérique qui pourrait fausser les résultats.
* **Établissement de la ligne de base (Idle) :** Une phase de repos de quelques minutes est observée avant de lancer le programme. Nous mesurons la consommation du système "à vide" pour identifier la consommation résiduelle inhérente à l'ordinateur. Cette valeur sert de référence pour isoler le surcoût énergétique lié uniquement à notre code.
* **Stabilité thermique :** Le processeur consomme davantage d'énergie lorsqu'il chauffe (phénomène de fuite de courant). Nous veillons donc à ce que la machine soit à une température stable entre chaque test pour éviter que la chaleur accumulée ne biaise les comparaisons.
* **Répétabilité et moyenne statistique :** Une mesure unique n'est jamais représentative à cause des micro-activités du système. Chaque test est répété plusieurs fois (par exemple 20 itérations). Nous calculons ensuite une moyenne des résultats et l'écart-type pour assurer la validité statistique de nos données et éliminer les valeurs aberrantes.

### 2.2 Le Protocole d'Estimation (L'Isolation)
Pour obtenir des mesures fiables avec PowerAPI, il est impératif de mettre en place un protocole d'isolation strict. L'objectif est de garantir que l'énergie consommée et mesurée provient exclusivement de l'exécution de notre algorithme et non de tâches de fond du système d'exploitation.
* **Nettoyage de l’environnement :** Avant chaque session de mesure, toutes les applications non essentielles (navigateurs web, outils de communication, mises à jour automatiques) doivent être fermées. Cela permet de réduire la sollicitation inutile du processeur et de la mémoire vive, limitant ainsi le "bruit" numérique qui pourrait fausser les résultats.
* **Établissement de la ligne de base (Idle) :** Une phase de repos de quelques minutes est observée avant de lancer le programme. Nous mesurons la consommation du système "à vide" pour identifier la consommation résiduelle inhérente à l'ordinateur. Cette valeur sert de référence pour isoler le surcoût énergétique lié uniquement à notre code.
* **Stabilité thermique :** Le processeur consomme davantage d'énergie lorsqu'il chauffe (phénomène de fuite de courant). Nous veillons donc à ce que la machine soit à une température stable entre chaque test pour éviter que la chaleur accumulée ne biaise les comparaisons.


## 3. Étude Algorithmique de la Multiplication de Matrices
### 3.1 Définition mathématique
Soient deux matrices :
A de taille n × p
B de taille p × m
Le produit matriciel C = A × B est défini par :
C[i][j] = Σ A[i][k] × B[k][j]
Cette opération nécessite un grand nombre de calculs arithmétiques et d’accès mémoire, ce qui en fait un cas d’étude pertinent pour analyser la consommation énergétique.

### 3.2 Algorithme naïf
L’algorithme classique repose sur trois boucles imbriquées :
Première boucle : lignes de A
Deuxième boucle : colonnes de B
Troisième boucle : somme des produits
La complexité temporelle est :
O(n³)
Cette complexité implique un grand nombre d’opérations lorsque la taille des matrices augmente.

### 3.3 Impact de l’ordre des boucles sur la mémoire
L’ordre des boucles influence fortement :
la localité mémoire
l’utilisation du cache CPU
le nombre d’accès à la RAM
Un mauvais ordre peut provoquer davantage de cache misses, augmentant ainsi la consommation énergétique.
Cette observation montre que deux implémentations mathématiquement équivalentes peuvent avoir des comportements énergétiques très différents.

## 4. Complexité et Consommation Énergétique
La consommation énergétique d’un programme dépend de la relation suivante :
Énergie (Joules) = Puissance (Watts) × Temps (secondes)
Un algorithme plus rapide réduit généralement le temps d’exécution, mais peut augmenter la puissance instantanée du processeur.
L’objectif est donc de trouver un compromis optimal entre performance et consommation électrique.

## 5. Synthèse
Cette étude théorique met en évidence que la consommation énergétique d’un programme dépend :
des choix algorithmiques
de l’implémentation
de la gestion mémoire
de l’interaction avec l’architecture matérielle
Dans la suite du projet, différentes implémentations de la multiplication de matrices en Rust seront analysées et mesurées afin de comparer leur efficacité énergétique.
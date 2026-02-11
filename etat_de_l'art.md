# État de l'Art : Efficacité Énergétique Logicielle

Ce document présente l'étude théorique préalable à l'implémentation de notre projet. Il s'appuie sur les références académiques et techniques fournies par l'encadrant.

## 1. Introduction et Enjeux
L’émergence de l’urgence climatique impose aujourd’hui une transformation profonde des pratiques de l’ingénierie logicielle, faisant de l’éco-conception un impératif technique plutôt qu’une simple option de performance. Alors que le secteur numérique représente une part croissante de la consommation électrique mondiale, le développement moderne doit désormais intégrer les enjeux environnementaux dès la phase de conception pour limiter l'empreinte matérielle et énergétique des services numériques. L'enjeu principal est d'optimiser l'efficacité énergétique, c'est-à-dire de réduire la quantité d'énergie nécessaire (exprimée en Joules) pour accomplir une tâche précise, appelée Unité Fonctionnelle.

En adoptant le langage Rust, ce projet s'inscrit dans une démarche de maîtrise fine du matériel, où chaque cycle CPU économisé et chaque accès à la mémoire vive (RAM) optimisé contribuent directement à l'amélioration du bilan énergétique global.

L'objectif scientifique ici est d'analyser le comportement d'une "unité fonctionnelle" précise — le calcul d'un produit matriciel de taille $N$ — pour démontrer qu'à résultat mathématique identique, des choix d'implémentation différents modifient radicalement la quantité de Joules consommés. Il s'agit donc d'établir un compromis optimal entre le temps d'exécution et la puissance électrique appelée, replaçant ainsi le développeur comme un acteur central de la sobriété numérique.
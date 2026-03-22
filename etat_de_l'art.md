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

### 2.3 Les Métriques de Calcul
Une fois le protocole de mesure appliqué, nous collectons des données quantitatives que nous analysons selon trois indicateurs complémentaires :
* **L'Énergie (Joules) :** C'est notre métrique de référence. Elle représente la quantité totale de travail électrique consommé par le processeur et la mémoire durant l'exécution complète de l'algorithme. C'est l'indicateur principal de l'empreinte environnementale du code.
* **La Puissance (Watts) :** Elle exprime le débit d'énergie à un instant $T$. Son analyse nous permet d'identifier les phases de calcul les plus intenses et d'observer les "pics" de consommation liés à certaines instructions ou accès mémoire.
* **Le Temps d'exécution (Secondes) :** Bien que l'objectif soit de réduire l'énergie, le temps reste une variable indissociable. Nous l'utilisons pour calculer l'efficacité énergétique globale, car un programme qui consomme peu de puissance mais met trop de temps à s'exécuter peut finalement présenter un bilan énergétique (en Joules) plus lourd qu'un programme rapide et intense.

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

## 5. Deuxième Cas d’Étude : L’Algorithme de Fibonacci

Afin d’élargir l’analyse de l’efficacité énergétique à un second type de calcul, nous avons choisi d’étudier l’algorithme de Fibonacci. Ce choix permet de compléter le cas de la multiplication de matrices par un problème algorithmique plus simple, mais très pertinent pour observer l’impact des choix d’implémentation sur la performance et, à terme, sur la consommation énergétique.

### 5.1 Principe

La suite de Fibonacci est définie par la relation de récurrence suivante :

- F(0) = 0
- F(1) = 1
- F(n) = F(n - 1) + F(n - 2) pour n ≥ 2

Cet algorithme est intéressant car il peut être implémenté de plusieurs manières très différentes, avec des coûts de calcul très contrastés.

### 5.2 Versions étudiées

Dans notre projet, nous avons retenu trois implémentations de Fibonacci :

- **version naïve récursive** : simple à écrire, mais très coûteuse car elle répète de nombreux calculs identiques ;
- **version itérative** : plus efficace, car elle calcule la suite de manière séquentielle sans redondance ;
- **version avec mémoïsation** : optimise la version récursive en mémorisant les résultats déjà calculés.

### 5.3 Intérêt pour l’étude énergétique

L’algorithme de Fibonacci constitue un bon second cas d’étude car il met en évidence l’impact direct de la complexité algorithmique sur le temps d’exécution. Contrairement à la multiplication de matrices, qui mobilise fortement le cache et la mémoire, Fibonacci permet davantage d’illustrer les effets de la redondance des calculs et de l’optimisation algorithmique.

Cette comparaison est utile dans le cadre du projet, car elle permet d’étudier l’efficacité énergétique sur deux familles différentes de problèmes :

- un algorithme de calcul intensif avec forte sollicitation mémoire (multiplication de matrices) ;
- un algorithme récursif où l’optimisation réduit fortement le nombre d’opérations inutiles (Fibonacci).

### 5.4 Hypothèse de travail

Nous faisons l’hypothèse que la version naïve récursive de Fibonacci sera beaucoup moins efficace, aussi bien en temps qu’en consommation énergétique, que les versions itérative et mémoïsée. Cette étude permettra donc de confirmer, sur un second exemple, qu’un meilleur choix d’implémentation améliore significativement l’efficacité globale d’un programme.

## 5. Synthèse
Cette étude théorique met en évidence que la consommation énergétique d’un programme dépend :
des choix algorithmiques
de l’implémentation
de la gestion mémoire
de l’interaction avec l’architecture matérielle
Dans la suite du projet, différentes implémentations de la multiplication de matrices en Rust seront analysées et mesurées afin de comparer leur efficacité énergétique.

## 6. Résultats Expérimentaux et Analyse
Afin de valider les concepts théoriques, nous avons implémenté quatre variantes du produit matriciel $n \times n$ en Rust. Les tests ont été effectués sous WSL2 (Ubuntu 24.04).

### 3.1 Tableau Comparatif (Taille $n = 1024$)
| Variante Algorithmique | Temps d'exécution (s) | Gain / Naïve |
| :--------------- |:---------------:| :-----:|
| 1. Naïve (i, j, k)  |   7.34 s        |  Référence |
| 2. Vector (i, k, j)  |   0.59 s        |   92% |
| 3. Blocked (Tiling)  |   0.38 s        |   94% |
| 4. Parallel (Rayon)  |   0.29 s        |    96% |

## 7. Mesure de la Consommation Énergétique (Windows Native)

Les mesures de temps sous WSL2 ne permettant pas d'accéder aux capteurs matériels du CPU,
nous avons effectué les mesures énergétiques directement sous Windows en utilisant
l'API matérielle RAPL (Running Average Power Limit) d'Intel.

### 7.1 Infrastructure de Mesure

**Technologie RAPL (Running Average Power Limit)**

Le processeur Intel Core i5-1145G7 embarque des compteurs matériels intégrés appelés
RAPL qui mesurent la consommation électrique réelle du CPU en temps réel, directement
depuis les registres internes du processeur (MSR registers). Ces compteurs sont
inaccessibles depuis WSL2 car celui-ci ne dispose pas d'un accès direct au matériel.

**Outil : LibreHardwareMonitor**

Dans le cadre de ce projet, nous avons étudié l’outil **LibreHardwareMonitor** afin de mieux comprendre les possibilités offertes pour l’analyse du comportement matériel d’un programme.

LibreHardwareMonitor est un logiciel libre de monitoring matériel. D’après les informations consultées, il permet de surveiller plusieurs types d’indicateurs en temps réel, notamment :

- les **températures**
- les **vitesses des ventilateurs**
- les **tensions**
- la **charge** du système
- les **fréquences d’horloge**

L’outil peut lire des informations sur plusieurs composants matériels, par exemple :

- les **cartes mères**
- les **processeurs Intel et AMD**
- les **cartes graphiques NVIDIA, AMD et Intel**
- les **disques HDD, SSD et NVMe**
- les **cartes réseau**

Pour notre projet, LibreHardwareMonitor est particulièrement intéressant car il ne se limite pas à une simple lecture de puissance. Il peut aussi fournir d’autres informations utiles pour l’analyse expérimentale, comme :

- la **température du processeur**
- la **charge CPU**
- la **fréquence CPU**

Ces fonctionnalités ouvrent la possibilité d’aller au-delà d’une simple mesure de temps d’exécution ou d’énergie, en étudiant aussi le comportement thermique et la sollicitation matérielle des différentes implémentations.

Nous utilisons LibreHardwareMonitor sous Windows, avec son **serveur web local** qui expose les données sous forme JSON. Cela permet à notre script Python de récupérer automatiquement les mesures nécessaires pendant l’exécution des programmes Rust.

Enfin, LibreHardwareMonitor propose également une bibliothèque nommée **LibreHardwareMonitorLib**, qui permet d’intégrer directement ses fonctionnalités dans une application. Cela représente une piste intéressante pour des extensions futures du projet.

Les informations sur LibreHardwareMonitor ont été obtenues à partir du dépôt officiel GitHub :
https://github.com/LibreHardwareMonitor/LibreHardwareMonitor

Pour accéder aux données RAPL sous Windows, nous avons utilisé
[LibreHardwareMonitor](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor),
un logiciel open-source qui :
1. Accède aux registres matériels du CPU en mode administrateur
2. Lit les valeurs RAPL en temps réel
3. Les expose via un serveur web local sur `http://localhost:8085/data.json`

**Mise en place :**
```bash
# Étape 1 : Téléchargement de LibreHardwareMonitor
# https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases
# Extraire le zip et lancer LibreHardwareMonitor.exe en tant qu'administrateur

# Étape 2 : Activation du serveur Web
# Options → cocher "Web Server" → port 8085

# Étape 3 : Vérification de l'accès au flux de données
# http://localhost:8085/data.json

# Étape 4 : Identification du capteur CPU Package Power via PowerShell
$json = (Invoke-WebRequest -Uri "http://localhost:8085/data.json").Content | ConvertFrom-Json

function Find-Power($node) {
    if ($node.Text -match "Power" -or $node.Text -match "Package") {
        Write-Host "ID: $($node.id) | Nom: $($node.Text) | Valeur: $($node.Value)"
    }
    foreach ($child in $node.Children) { Find-Power $child }
}
Find-Power $json
```

Résultat obtenu :
```
ID: 11 | Nom: CPU Package | Valeur: 13,3 W   ← capteur utilisé
ID: 79 | Nom: GPU Power   | Valeur: 0,1 W
```

Le capteur **ID 11 — CPU Package** représente la puissance totale consommée par
le processeur. C'est ce capteur qui a été utilisé pour toutes les mesures.

### 7.2 Méthodologie de Mesure

**Principe : échantillonnage + intégration trapézoïdale**

La puissance CPU n'est pas constante pendant l'exécution d'un benchmark — elle varie
selon la charge. Il est donc impossible d'utiliser une valeur fixe. Notre script Python
adopte l'approche suivante :

1. **Lancer le binaire Rust en arrière-plan** via `subprocess.Popen()`
2. **Échantillonner la puissance** toutes les 50ms en interrogeant LibreHardwareMonitor
   pendant toute la durée d'exécution
3. **Calculer l'énergie** par intégration trapézoïdale :

$$E = \sum_{i=1}^{n} \frac{P_i + P_{i-1}}{2} \times \Delta t_i$$

où $P_i$ est la puissance en Watts à l'instant $t_i$ et $\Delta t_i$ est l'intervalle
entre deux échantillons consécutifs. Le résultat est exprimé en **Joules**.

Chaque version a été exécutée **2 fois** sur des matrices $1024 \times 1024$,
et la moyenne est retenue afin de réduire le bruit de mesure dû aux processus
système en arrière-plan (OS, antivirus, etc.).

### 7.3 Résultats Énergétiques (Taille $n = 1024$)

| Variante | Temps moyen (s) | Puissance moy. (W) | Énergie moy. (J) | Ratio / Naïve |
| :------- | :-------------: | :----------------: | :--------------: | :-----------: |
| Naïve (i,j,k)     | 8.24  | 18.07 | 147.15 | Référence |
| Vectorisée (i,k,j)| 0.59  | 10.60 | 5.12   | −96.5%    |
| Blocked (Tiling)  | 0.49  | 17.65 | 6.96   | −95.3%    |
| Parallel (Rayon)  | 0.38  | 14.40 | 3.86   | −97.4%    |

### 7.4 Analyse

**Le temps d'exécution est le facteur dominant de la consommation énergétique.**

La version naïve consomme **38x plus d'énergie** que la version parallèle, non pas
parce qu'elle consomme beaucoup plus de watts (18W vs 14W, soit seulement ×1.3),
mais parce qu'elle s'exécute **22x plus longtemps** (8.24s vs 0.38s).

Ce résultat illustre un principe fondamental de l'efficacité énergétique :

> *Réduire le temps d'exécution est plus efficace énergétiquement que réduire
> la puissance instantanée.*

**Comparaison vectorisée vs blocked :**
La version vectorisée (5.12 J) consomme moins que la version blocked (6.96 J) malgré
un temps légèrement supérieur, car sa puissance instantanée est plus basse (10.6W vs
17.6W). Le tiling améliore la localité cache mais introduit un overhead de gestion
des blocs qui augmente la charge CPU.

**Version parallèle :**
Bien qu'elle utilise plusieurs cœurs simultanément — ce qui augmente la puissance
instantanée — la réduction drastique du temps d'exécution (0.38s) en fait la version
la plus économe en énergie absolue (3.86 J).
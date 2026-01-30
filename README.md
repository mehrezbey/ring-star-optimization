# ring-star-optimization

## Description

Ce projet implémente et compare plusieurs approches d’optimisation combinatoire pour un problème combinant :

* la **sélection de stations (p-médian)**,
* la **construction d’une tournée (TSP)**,
* des **métaheuristiques (recuit simulé)**,
* et une **approche exacte** à des fins de comparaison.


---

## Auteurs

* **Bey Mehrez**
* **Aziz Azouni**

---

## Prérequis

Le projet est conçu pour être exécuté sous **Linux**, et au minimum sur les machines des salles TP de l’Institut Galilée.

Assurez-vous de disposer de :

* Python 3.8 ou plus
* `make`
* `pip`

---

## Récupération du projet

Deux méthodes sont possibles.

### Méthode 1 : Archive ZIP (recommandée si vous avez déjà le fichier)

* Extraire l’archive fournie
* Se placer dans le dossier du projet

```bash
cd ring-star-optimization/
```

### Méthode 2 : Clonage via Git

Si vous êtes familiarisé avec Git, vous pouvez cloner directement le dépôt :

```bash
git clone https://github.com/mehrezbey/ring-star-optimization.git
cd ring-star-optimization/
```

---

## Installation des dépendances

Depuis le répertoire racine du projet, exécuter :

```bash
make install
```

Cette commande :

* crée l’environnement nécessaire,
* installe automatiquement toutes les dépendances Python requises.

---

## Exécution du programme

Pour lancer le programme principal :

```bash
make run
```

Un **menu interactif** s’affiche alors dans le terminal.
Il vous permettra de :

* choisir une instance de test,
* sélectionner le type d’algorithme à exécuter (heuristique, métaheuristique, etc.),
* lancer les calculs et générer les résultats expérimentaux.

Les résultats (temps de calcul) sont sauvegardés dans un fichier `result.csv`.
Des visualisations peuvent également être générées sous forme d’images.

---

## Nettoyage du projet

Une fois l’exécution terminée, vous pouvez nettoyer l’environnement avec :

```bash
make clean
```

Cette commande :

* supprime les dépendances installées,
* supprime le fichier `result.csv`.

**Remarque** :
Les images générées ne sont **pas supprimées volontairement**, afin de permettre leur exploitation dans le rapport.

---

## Organisation du projet (résumé)

* `src/` : implémentations des algorithmes
* `data/` : jeux de données
* `results/` : résultats expérimentaux
* `Makefile` : installation, exécution et nettoyage
* `README.md` : instructions d’utilisation

---

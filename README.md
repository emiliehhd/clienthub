# ClientHub — CI/CD avec GitHub Actions, Docker et Azure

## Présentation

ClientHub est une application web composée d'une API Flask et d'une base de données MySQL.

L'objectif du projet est de mettre en place une chaîne **CI/CD automatisée** permettant de tester, construire et déployer l'application automatiquement.

## Architecture

L'application utilise :

* **Python / Flask** pour l'API
* **MySQL** pour la base de données
* **Docker** pour la conteneurisation
* **Docker Hub** pour stocker l'image de l'API
* **GitHub Actions** pour l'intégration et le déploiement continus
* **Azure VM** pour l'hébergement de l'application

L'API est accessible sur le port `8012`.

## Fonctionnement du pipeline CI/CD

Le pipeline est défini dans :

```text
.github/workflows/ci-cd.yml
```

À chaque `push` sur la branche `main`, GitHub Actions exécute automatiquement les étapes suivantes :

```text
Push sur main
      ↓
Tests unitaires
      ↓
Tests E2E
      ↓
Build de l'image Docker
      ↓
Push vers Docker Hub
      ↓
Connexion SSH à la VM Azure
      ↓
Déploiement de l'application
      ↓
Vérification de l'API
```

### 1. Tests unitaires

Les tests unitaires vérifient le fonctionnement de l'API Flask, notamment l'endpoint `/health`.

### 2. Tests E2E

Les tests E2E vérifient l'application complète avec les conteneurs Docker et la base MySQL.

Les endpoints `/health` et `/clients` sont testés.

### 3. Build et publication Docker

Après validation des tests, l'image Docker de l'API est construite puis publiée sur Docker Hub.

Deux tags sont générés :

* `latest`
* le SHA du commit Git

### 4. Déploiement Azure

Si les étapes précédentes réussissent, GitHub Actions se connecte automatiquement à la VM Azure via SSH.

L'image Docker est récupérée depuis Docker Hub puis l'application Flask et MySQL sont démarrés avec Docker Compose.

Le déploiement vérifie ensuite l'accessibilité de l'API avant de considérer le déploiement comme réussi.

## Déclenchement du déploiement

Le pipeline est déclenché automatiquement lorsqu'un commit est poussé sur la branche `main`.

Il n'est donc pas nécessaire de se connecter manuellement à la VM Azure pour déployer une nouvelle version.

## Choix techniques

### GitHub Actions

GitHub Actions permet de regrouper les tests, la construction de l'image et le déploiement dans un même pipeline automatisé.

### Docker

Docker permet d'assurer un environnement reproductible entre le développement, les tests et la VM Azure.

### Docker Compose

Docker Compose permet de gérer facilement les deux services principaux :

* l'API Flask
* la base de données MySQL

### Docker Hub

Docker Hub sert de registre pour stocker et distribuer l'image Docker de l'API entre GitHub Actions et la VM Azure.

### Azure VM

La VM Azure héberge l'application et permet de rendre l'API accessible depuis Internet.

### GitHub Secrets

Les informations sensibles telles que les identifiants Docker Hub, les informations de connexion SSH et les identifiants MySQL sont stockées dans **GitHub Secrets** et ne sont pas présentes dans le dépôt.

## Accès à l'application

API :

```text
http://40.66.52.118:8012
```

Endpoint de santé :

```text
http://40.66.52.118:8012/health
```

Endpoint clients :

```text
http://40.66.52.118:8012/clients
```

## Tests

Les tests peuvent être exécutés localement avec :

```bash
pytest
```

Le projet contient :

* `tests/test_app.py` pour les tests unitaires
* `tests/test_e2e.py` pour les tests end-to-end

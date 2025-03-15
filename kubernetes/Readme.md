# Déploiement Kubernetes - Application Todo

Ce document décrit le déploiement d'une application Todo avec une base de données MySQL sur un cluster Kubernetes. Les manifestes Kubernetes ont été créés pour orchestrer les conteneurs décrits dans le fichier docker-compose d'origine.

## Structure des fichiers

Le dossier `kubernetes/` contient tous les manifestes nécessaires au déploiement :

```
kubernetes/
├── namespace.yaml
├── mysql-secret.yaml
├── mysql-pvc.yaml
├── mysql-deployment.yaml
├── mysql-service.yaml
├── backend-configmap.yaml
├── backend-deployment.yaml
└── backend-service.yaml
```

## Description des manifestes

### 1. namespace.yaml
- Crée un espace de noms isolé `todo-app` pour regrouper toutes les ressources de l'application

### 2. mysql-secret.yaml
- Stocke les informations sensibles pour MySQL (utilisateurs, mots de passe, etc.)
- Utilise l'encodage base64 pour les valeurs comme requis par Kubernetes
- Remplace les variables d'environnement du fichier docker-compose

### 3. mysql-pvc.yaml
- Définit un PersistentVolumeClaim pour assurer la persistance des données MySQL
- Équivalent au volume nommé dans docker-compose

### 4. mysql-deployment.yaml
- Déploie le conteneur MySQL 8.0
- Configure les variables d'environnement à partir du Secret
- Monte le volume persistant pour les données
- Définit des sondes de vivacité (liveness) et préparation (readiness) pour assurer la stabilité

### 5. mysql-service.yaml
- Crée un service headless pour MySQL
- Permet la communication interne avec la base de données

### 6. backend-configmap.yaml
- Stocke les configurations non-sensibles pour le backend
- Configure l'hôte de base de données (pointant vers le service MySQL)

### 7. backend-deployment.yaml
- Configure le déploiement du backend avec 2 réplicas pour la haute disponibilité
- Définit les variables d'environnement nécessaires en référençant le ConfigMap et les Secrets
- Configure des sondes de santé qui vérifient l'endpoint `/health`

### 8. backend-service.yaml
- Expose le backend en tant que service ClusterIP
- Route les requêtes du port 80 vers le port 5000 de l'application

## Déploiement

Pour déployer l'application, exécutez les commandes suivantes dans l'ordre :

```bash
# Création du namespace
kubectl apply -f kubernetes/namespace.yaml

# Déploiement de MySQL
kubectl apply -f kubernetes/mysql-secret.yaml
kubectl apply -f kubernetes/mysql-pvc.yaml
kubectl apply -f kubernetes/mysql-deployment.yaml
kubectl apply -f kubernetes/mysql-service.yaml

# Déploiement du backend
kubectl apply -f kubernetes/backend-configmap.yaml
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-service.yaml
```

Alternativement, vous pouvez déployer tout d'un coup :

```bash
kubectl apply -f kubernetes/
```

## Vérification du déploiement

Utilisez ces commandes pour vérifier que le déploiement fonctionne correctement :

```bash
# Vérifier les pods
kubectl get pods -n todo-app

# Vérifier les services
kubectl get services -n todo-app

# Vérifier les déploiements
kubectl get deployments -n todo-app
```

## Personnalisation

Avant le déploiement, assurez-vous de :
1. Remplacer `${DOCKERHUB_ID}` dans `backend-deployment.yaml` par votre identifiant DockerHub
2. Encoder correctement vos informations d'identification en base64 dans `mysql-secret.yaml`

## Améliorations apportées

Ce déploiement Kubernetes comprend plusieurs améliorations par rapport à la configuration docker-compose :
- Haute disponibilité avec plusieurs réplicas pour le backend
- Sondes de santé pour garantir la stabilité des services
- Séparation des configurations et des secrets
- Isolation dans un namespace dédié
- Gestion de persistance des données via PVC

## Endpoint API Backend

L'API backend est accessible via le service `backend` dans le namespace `todo-app`. Les endpoints disponibles sont :
- `GET /api/todos` - Récupérer toutes les tâches
- `POST /api/todos` - Créer une nouvelle tâche
- `GET /api/todos/{id}` - Récupérer une tâche spécifique
- `GET /health` - Vérification de l'état de santé (pour Kubernetes)
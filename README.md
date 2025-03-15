# devops_project
Projet DevOps

# Backend Setup Guide

## Running Without Docker

### 1. Install Python and Dependencies
Ensure Python is installed on your system. If not, install it with:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

### 2. Verify Installation
Check Python and `pip` versions:

```bash
python3 --version
pip3 --version
```

### 3. Create and Activate a Virtual Environment
Create a virtual environment inside your project directory:

```bash
python3 -m venv devops_env
```

Activate the virtual environment:

```bash
source devops_env/bin/activate
```

### 4. Install Dependencies
Install the required dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the project directory and add the following content:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=todo_db
```

### 6. Create the Database
Ensure MySQL is running and create the database:

```sql
CREATE DATABASE todo_db;
```

### 7. Run the Backend
Start the Flask application:

```bash
python app.py
```

---

## Running with Docker

### 1. Pull the Backend Image from Docker Hub
Since the image is already available on Docker Hub, pull it using:

```bash
docker pull metsarr49/backend:v1.0.0
```

### 2. Run the Backend Container
If a local MySQL database is available, run the backend container with:

```bash
docker run --network=host -e DB_HOST=localhost -e DB_USER=root -e DB_PASSWORD=your_password -e DB_NAME=todo_db metsarr49/backend:v1.0.0
```

Alternatively, you can pass the `.env` file:

```bash
docker run --network=host --env-file .env metsarr49/backend:v1.0.0
```

Alternatively, you can use specific port (example 8080):

```bash
docker run -p 8080:5000  --env-file .env metsarr49/backend:v1.0.0
```

### 3. Run MySQL in Docker (Optional)
If you do not have a local MySQL instance, run a MySQL container:

```bash
docker run --name mysql-db -e MYSQL_ROOT_PASSWORD=your_password -e MYSQL_DATABASE=todo_db -p 3306:3306 -d mysql:latest
```

Ensure that the `DB_HOST` environment variable in the `.env` file is set to `host.docker.internal` (for Windows/macOS) or `mysql-db` (for Docker networks).

### 4. Test the API
Use `curl` or Postman to test the API:

#### Create a New Task (POST)
```bash
curl -X POST http://localhost:5000/api/todos -H "Content-Type: application/json" -d '{"title": "Send Email", "description": "Reply to client", "completed": false}'
```

#### Retrieve All Tasks (GET)
```bash
curl -X GET http://localhost:5000/api/todos
```

#### Retrieve a Specific Task (GET)
```bash
curl -X GET http://localhost:5000/api/todos/1
```

---

Now your backend is up and running locally or inside Docker. Modify the configuration as needed for your environment.

---

v2 of docker compose 
Run
``` bash
docker compose up -d 
```
Verify
``` bash
docker compose ps 
```
Stop
``` bash 
docker compose down 
```

# **Kubernetes Deployment - Todo Application**  

This document describes the deployment of a Todo application with a MySQL database on a Kubernetes cluster. Kubernetes manifests have been created to orchestrate the containers originally defined in the `docker-compose` file.  

## **File Structure**  

The `kubernetes/` directory contains all the necessary manifests for deployment:  

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

## **Manifest Descriptions**  

### **1. namespace.yaml**  
- Creates an isolated namespace `todo-app` to group all application resources.  

### **2. mysql-secret.yaml**  
- Stores sensitive MySQL information (usernames, passwords, etc.).  
- Uses base64 encoding as required by Kubernetes.  
- Replaces environment variables from the `docker-compose` file.  

### **3. mysql-pvc.yaml**  
- Defines a PersistentVolumeClaim (PVC) to ensure MySQL data persistence.  
- Equivalent to the named volume in `docker-compose`.  

### **4. mysql-deployment.yaml**  
- Deploys the MySQL 8.0 container.  
- Configures environment variables from the Secret.  
- Mounts the persistent volume for data storage.  
- Defines liveness and readiness probes to ensure service stability.  

### **5. mysql-service.yaml**  
- Creates a headless service for MySQL.  
- Enables internal database communication.  

### **6. backend-configmap.yaml**  
- Stores non-sensitive configurations for the backend.  
- Configures the database host (pointing to the MySQL service).  

### **7. backend-deployment.yaml**  
- Configures the backend deployment with 2 replicas for high availability.  
- Sets up required environment variables referencing ConfigMap and Secrets.  
- Configures health probes checking the `/health` endpoint.  

### **8. backend-service.yaml**  
- Exposes the backend as a ClusterIP service.  
- Routes requests from port 80 to port 5000 of the application.  

## **Deployment**  

To deploy the application, execute the following commands in order:  

```bash
# Create the namespace
kubectl apply -f kubernetes/namespace.yaml

# Deploy MySQL
kubectl apply -f kubernetes/mysql-secret.yaml
kubectl apply -f kubernetes/mysql-pvc.yaml
kubectl apply -f kubernetes/mysql-deployment.yaml
kubectl apply -f kubernetes/mysql-service.yaml

# Deploy the backend
kubectl apply -f kubernetes/backend-configmap.yaml
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-service.yaml
```

Alternatively, deploy everything at once:  

```bash
kubectl apply -f kubernetes/
```

## **Deployment Verification**  

Use these commands to verify that the deployment is running correctly:  

```bash
# Check running pods
kubectl get pods -n todo-app

# Check services
kubectl get services -n todo-app

# Check deployments
kubectl get deployments -n todo-app
```

## **Customization**  

Before deployment, make sure to:  
1. Replace `${DOCKERHUB_ID}` in `backend-deployment.yaml` with your actual DockerHub ID.  
2. Properly encode your credentials in base64 format in `mysql-secret.yaml`.  

## **Enhancements**  

This Kubernetes deployment includes several improvements over the `docker-compose` configuration:  
- High availability with multiple replicas for the backend.  
- Health probes to ensure service stability.  
- Separation of configurations and secrets.  
- Isolation within a dedicated namespace.  
- Persistent data management using PVC.  

## **Backend API Endpoints**  

The backend API is accessible via the `backend` service in the `todo-app` namespace. Available endpoints include:  

- `GET /api/todos` - Retrieve all tasks.  
- `POST /api/todos` - Create a new task.  
- `GET /api/todos/{id}` - Retrieve a specific task.  
- `GET /health` - Health check endpoint (for Kubernetes).  
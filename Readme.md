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


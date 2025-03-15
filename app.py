from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Configuration de la connexion à la base de données
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'todo_db')
        )
        return connection
    except Error as e:
        print(f"Erreur de connexion à MySQL: {e}")
        return None

# Créer la table si elle n'existe pas
def create_table():
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS todos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            connection.commit()
            cursor.close()
            connection.close()
            print("Table 'todos' créée avec succès ou déjà existante.")
    except Error as e:
        print(f"Erreur lors de la création de la table: {e}")

# Créer la table au démarrage
create_table()

# Endpoint pour créer une nouvelle tâche (WRITE)
@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Le titre est requis'}), 400
    
    title = data['title']
    description = data.get('description', '')
    completed = data.get('completed', False)
    
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            
            query = "INSERT INTO todos (title, description, completed) VALUES (%s, %s, %s)"
            values = (title, description, completed)
            
            cursor.execute(query, values)
            connection.commit()
            
            new_todo_id = cursor.lastrowid
            
            cursor.close()
            connection.close()
            
            return jsonify({
                'id': new_todo_id,
                'title': title,
                'description': description,
                'completed': completed,
                'message': 'Tâche créée avec succès'
            }), 201
    except Error as e:
        return jsonify({'error': f'Erreur lors de la création de la tâche: {str(e)}'}), 500

# Endpoint pour récupérer toutes les tâches (READ)
@app.route('/api/todos', methods=['GET'])
def get_todos():
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT id, title, description, completed, created_at FROM todos"
            cursor.execute(query)
            
            todos = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return jsonify(todos), 200
    except Error as e:
        return jsonify({'error': f'Erreur lors de la récupération des tâches: {str(e)}'}), 500

# Endpoint pour récupérer une tâche spécifique par ID (READ)
@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT id, title, description, completed, created_at FROM todos WHERE id = %s"
            cursor.execute(query, (todo_id,))
            
            todo = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if todo:
                return jsonify(todo), 200
            else:
                return jsonify({'error': 'Tâche non trouvée'}), 404
    except Error as e:
        return jsonify({'error': f'Erreur lors de la récupération de la tâche: {str(e)}'}), 500
    
# Endpoint pour les health checks Kubernetes
@app.route('/health', methods=['GET'])
def health_check():
    try:
        connection = create_connection()
        if connection:
            connection.close()
            return jsonify({"status": "healthy", "database": "connected"}), 200
        else:
            return jsonify({"status": "unhealthy", "database": "disconnected"}), 500
    except Error as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
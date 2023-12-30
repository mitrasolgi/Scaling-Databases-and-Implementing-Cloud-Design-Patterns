# app.py
from flask import Flask, request, jsonify
import sys
from config import AWSConfig, MySQLConfig
from mysql_cluster import MySQLCluster
from proxy_creator import create_proxy  # Import the create_proxy function
from gatekeeper import Gatekeeper
app = Flask(__name__)

# Create instances for master and slave
master_node = MySQLCluster(is_master=True)
slave_nodes = [MySQLCluster(is_master=False) for _ in range(len(AWSConfig.SLAVE_NODES_IPS))]

strategy = sys.argv[1] if len(sys.argv) > 1 else "direct"
proxy_server = create_proxy(strategy, master_node, slave_nodes)
gatekeeper = Gatekeeper(proxy_server)

@app.route('/process_request', methods=['POST'])
def process_request():
    data = request.get_json()
    query_type = data.get('query_type', '')

    if query_type not in ['read', 'write']:
        return jsonify({'error': 'Invalid query type'}), 400

    gatekeeper.process_request(query_type)

    return jsonify({'message': 'Request processed successfully'})

if __name__ == "__main__":
    with master_node.get_connection() as connection:
        cursor = connection.cursor()
        # Create a database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS test_database;")
        cursor.execute("USE test_database;")
        # Create a table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incoming_requests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age INT,
                email VARCHAR(255)
            );
        """)
        app.run(host='0.0.0.0', port=5000)

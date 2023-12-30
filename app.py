"""
app.py

This script defines a Flask web application that serves as an API for processing database queries.
It utilizes a MySQL database cluster with master and slave nodes, and a proxy server to handle read
and write queries. The gatekeeper ensures that requests are appropriately routed based on the query type.

Endpoints:
    - POST /process_request: Accepts JSON data containing a 'query_type' field ('read' or 'write') and
                             processes the request accordingly.

Usage:
    python app.py [proxy_strategy]

Parameters:
    - proxy_strategy (optional): The strategy used for proxying database requests. Accepted values are
                                 'direct' or any custom strategy implemented in proxy_creator.py.
                                 If not provided, the default is 'direct'.

Example:
    python app.py custom_strategy

Note:
    Before running the script, make sure to configure the database and table creation logic in the
    __main__ block, including the necessary imports and configurations.

"""
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
    """
       Endpoint for processing incoming database queries.

       Accepts a JSON request with a 'query_type' field specifying the type of query ('read' or 'write').
       The gatekeeper processes the request, routing it to the appropriate database node.

       Returns:
           - JSON response indicating the success or failure of the request.

       Example JSON input:
           {
               "query_type": "read",
               "data": {...}
           }

       Example JSON output:
           {
               "message": "Request processed successfully"
           }

       """
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

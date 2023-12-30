"""
mysql_cluster.py

This module defines the MySQLCluster class, which represents a cluster of MySQL database nodes.
Instances of this class can be either master or proxy nodes, based on the provided flag.

Usage:
    1. Import the MySQLCluster class from this module.
    2. Create instances of MySQLCluster, specifying whether each instance is a master or proxy node.
    3. Use the get_connection method to obtain a MySQL database connection.

Example:
    from mysql_cluster import MySQLCluster
    from config import MySQLConfig

    # Create a master node
    master_node = MySQLCluster(is_master=True)

    # Create a proxy node
    proxy_node = MySQLCluster(is_master=False)

    # Obtain a connection to the database using the master node
    with master_node.get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM your_table;")

    # Obtain a connection to the database using the proxy node
    with proxy_node.get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM your_table;")

Note:
    - Replace 'your_table' with the actual table name in your database.
"""
import mysql.connector
from config import AWSConfig, MySQLConfig
class MySQLCluster:
    def __init__(self, is_master):
        """
        Initializes the MySQLCluster instance.

        Parameters:
            is_master (bool): Specifies whether the instance represents a master node (True) or a proxy node (False).
        """
        self.is_master = is_master
        self.db_endpoint = MySQLConfig.MASTER_DB_HOST
        self.db_user = MySQLConfig.MASTER_DB_USER if is_master else MySQLConfig.PROXY_DB_USER
        self.db_password = MySQLConfig.MASTER_DB_PASSWORD if is_master else MySQLConfig.PROXY_DB_PASSWORD
        self.db_database = MySQLConfig.MASTER_DB_DATABASE if is_master else MySQLConfig.PROXY_DB_DATABASE

    def get_connection(self):
        """
        Obtain a connection to the MySQL database.

        Returns:
            mysql.connector.connection.MySQLConnection: A connection to the MySQL database.
        """
        return mysql.connector.connect(
            host=self.db_endpoint,
            user=self.db_user,
            password=self.db_password,
            database=self.db_database,
            autocommit=True
        )

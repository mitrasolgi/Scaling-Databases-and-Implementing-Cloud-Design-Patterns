"""
proxy.py

This module defines the Proxy class and three proxy strategy classes (DirectHitStrategy, RandomStrategy, CustomizedStrategy).
The Proxy class is responsible for routing database queries to the appropriate database node based on the selected strategy.

Usage:
    1. Import the Proxy class and the desired strategy class from this module.
    2. Create an instance of the Proxy class, specifying the database cluster, strategy, proxy IP, and instance type.
    3. Call the route_query method on the Proxy instance to route a database query.

Example:
    from proxy import Proxy, RandomStrategy
    from mysql_cluster import MySQLCluster

    # Create a MySQL database cluster
    my_cluster = MySQLCluster(is_master=True)

    # Create a Proxy instance with a random strategy
    random_proxy = Proxy(cluster=my_cluster, strategy=RandomStrategy(nodes=my_cluster.get_all_nodes()),
                         proxy_ip='192.168.1.1', instance_type='t2.large')

    # Route a database query using the proxy
    random_proxy.route_query("SELECT * FROM your_table;")

Note:
    - Replace 'your_table' with the actual table name in your database.
"""

import random

class Proxy:
    def __init__(self, cluster, strategy, proxy_ip, instance_type):
        """
               Initializes the Proxy instance.

               Parameters:
                   cluster (MySQLCluster): The MySQL database cluster.
                   strategy (object): An instance of a strategy class for routing queries.
                   proxy_ip (str): The IP address of the proxy.
                   instance_type (str): The type of the proxy instance (e.g., 't2.large').
               """
        self.cluster = cluster
        self.strategy = strategy
        self.proxy_ip = proxy_ip
        self.instance_type = instance_type

    def route_query(self, query):
        """
             Routes a database query to the appropriate database node based on the selected strategy.

             Parameters:
                 query (str): The SQL query to be routed to a database node.
             """
        node = self.strategy.select_node()
        print("Database and table created successfully.")
        with node.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)



class DirectHitStrategy:
    def __init__(self, cluster):
        """
              Initializes the DirectHitStrategy.

              Parameters:
                  cluster (MySQLCluster): The MySQL database cluster.
              """
        self.cluster = cluster

    def select_node(self):
        """
              Selects the database node directly associated with the cluster.

              Returns:
                  MySQLCluster: The master or proxy node associated with the cluster.
              """
        return self.cluster

class RandomStrategy:
    def __init__(self, nodes):
        """
               Initializes the RandomStrategy.

               Parameters:
                   nodes (list): A list of database nodes to choose from.
               """
        self.nodes = nodes

    def select_node(self):
        """
               Selects a database node randomly from the list.

               Returns:
                   MySQLCluster: A randomly selected master or proxy node.
               """
        return random.choice(self.nodes)

class CustomizedStrategy:
    def __init__(self, cluster, all_nodes):
        """
                Initializes the CustomizedStrategy.

                Parameters:
                    cluster (MySQLCluster): The MySQL database cluster.
                    all_nodes (list): A list of all available database nodes, including master and proxy nodes.
                """
        self.cluster = cluster
        self.all_nodes = all_nodes

    def select_node(self):
        """
              Selects a database node based on a customized strategy (e.g., ping time).

              Returns:
                  MySQLCluster: The selected master or proxy node.
              """
        ping_times = {node: self.measure_ping_time(node) for node in self.all_nodes}
        min_ping_node = min(ping_times, key=ping_times.get)
        return min_ping_node

    def measure_ping_time(self, node):
        """
               Measures the ping time to a database node (placeholder implementation).

               Parameters:
                   node (MySQLCluster): The database node to measure ping time for.

               Returns:
                   float: The simulated ping time.
               """
        return random.uniform(0.1, 1.0)

"""
proxy_creator.py

This module defines a function to create a Proxy instance with a specified routing strategy.
The create_proxy function takes a strategy, master node, and a list of nodes as input, and returns a Proxy instance.

Usage:
    1. Import the create_proxy function from this module.
    2. Create a master node and a list of nodes.
    3. Call the create_proxy function with the desired strategy, master node, and list of nodes to obtain a Proxy instance.

Example:
    from proxy_creator import create_proxy
    from mysql_cluster import MySQLCluster
    from config import AWSConfig

    # Create a master node
    master_node = MySQLCluster(is_master=True)

    # Create a list of nodes (including master and proxy nodes)
    nodes = [master_node, MySQLCluster(is_master=False), MySQLCluster(is_master=False)]

    # Create a Proxy instance with a random strategy
    random_proxy = create_proxy(strategy='random', master_node=master_node, nodes=nodes)

    # Route a database query using the proxy
    random_proxy.route_query("SELECT * FROM your_table;")

Note:
    - Replace 'your_table' with the actual table name in your database.
"""
from proxy import Proxy, DirectHitStrategy, RandomStrategy, CustomizedStrategy
from config import AWSConfig, MySQLConfig
def create_proxy(strategy, master_node, nodes):
    """
       Creates a Proxy instance with the specified routing strategy.

       Parameters:
           strategy (str): The routing strategy to be used ('direct', 'random', or 'customized').
           master_node (MySQLCluster): The master node of the database cluster.
           nodes (list): A list of database nodes, including master and proxy nodes.

       Returns:
           Proxy: An instance of the Proxy class with the specified routing strategy.
       """
    if strategy == "direct":
        return Proxy(master_node, DirectHitStrategy(master_node), AWSConfig.PROXY_SERVER_IP, AWSConfig.PROXY_SERVER_INSTANCE_TYPE)
    elif strategy == "random":
        return Proxy(master_node, RandomStrategy(nodes), AWSConfig.PROXY_SERVER_IP, AWSConfig.PROXY_SERVER_INSTANCE_TYPE)
    elif strategy == "customized":
        return Proxy(master_node, CustomizedStrategy(master_node, nodes), AWSConfig.PROXY_SERVER_IP, AWSConfig.PROXY_SERVER_INSTANCE_TYPE)
    else:
        raise ValueError("Invalid strategy")

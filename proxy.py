# proxy.py
import random

class Proxy:
    def __init__(self, cluster, strategy, proxy_ip, instance_type):
        self.cluster = cluster
        self.strategy = strategy
        self.proxy_ip = proxy_ip
        self.instance_type = instance_type

    def route_query(self, query):
        node = self.strategy.select_node()
        print("Database and table created successfully.")
        with node.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)



class DirectHitStrategy:
    def __init__(self, cluster):
        self.cluster = cluster

    def select_node(self):
        return self.cluster

class RandomStrategy:
    def __init__(self, nodes):
        self.nodes = nodes

    def select_node(self):
        return random.choice(self.nodes)

class CustomizedStrategy:
    def __init__(self, cluster, all_nodes):
        self.cluster = cluster
        self.all_nodes = all_nodes

    def select_node(self):
        ping_times = {node: self.measure_ping_time(node) for node in self.all_nodes}
        min_ping_node = min(ping_times, key=ping_times.get)
        return min_ping_node

    def measure_ping_time(self, node):
        return random.uniform(0.1, 1.0)

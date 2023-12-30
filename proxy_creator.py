# proxy_creator.py
from proxy import Proxy, DirectHitStrategy, RandomStrategy, CustomizedStrategy
from config import AWSConfig, MySQLConfig
def create_proxy(strategy, master_node, nodes):
    if strategy == "direct":
        return Proxy(master_node, DirectHitStrategy(master_node), AWSConfig.PROXY_SERVER_IP, AWSConfig.PROXY_SERVER_INSTANCE_TYPE)
    elif strategy == "random":
        return Proxy(master_node, RandomStrategy(nodes), AWSConfig.PROXY_SERVER_IP, AWSConfig.PROXY_SERVER_INSTANCE_TYPE)
    elif strategy == "customized":
        return Proxy(master_node, CustomizedStrategy(master_node, nodes), AWSConfig.PROXY_SERVER_IP, AWSConfig.PROXY_SERVER_INSTANCE_TYPE)
    else:
        raise ValueError("Invalid strategy")

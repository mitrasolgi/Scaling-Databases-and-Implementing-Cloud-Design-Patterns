# mysql_cluster.py
import mysql.connector
from config import AWSConfig, MySQLConfig
class MySQLCluster:
    def __init__(self, is_master):
        self.is_master = is_master
        self.db_endpoint = MySQLConfig.MASTER_DB_HOST
        self.db_user = MySQLConfig.MASTER_DB_USER if is_master else MySQLConfig.PROXY_DB_USER
        self.db_password = MySQLConfig.MASTER_DB_PASSWORD if is_master else MySQLConfig.PROXY_DB_PASSWORD
        self.db_database = MySQLConfig.MASTER_DB_DATABASE if is_master else MySQLConfig.PROXY_DB_DATABASE

    def get_connection(self):
        return mysql.connector.connect(
            host=self.db_endpoint,
            user=self.db_user,
            password=self.db_password,
            database=self.db_database,
            autocommit=True
        )

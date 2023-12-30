#!/bin/bash

# MySQL Stand-alone Server Setup
sudo apt-get update
sudo apt-get install -y mysql-server
sudo mysql_secure_installation

# MySQL Cluster Installation and Configuration
MYSQL_CLUSTER_VERSION="7.2.1"
MYSQL_CLUSTER_URL="http://dev.mysql.com/get/Downloads/MySQL-Cluster-${MYSQL_CLUSTER_VERSION}/mysql-cluster-gpl-${MYSQL_CLUSTER_VERSION}-linux2.6-x86_64.tar.gz"

# Download and extract MySQL Cluster
sudo wget ${MYSQL_CLUSTER_URL}
sudo tar xvf mysql-cluster-gpl-${MYSQL_CLUSTER_VERSION}-linux2.6-x86_64.tar.gz
sudo ln -s mysql-cluster-gpl-${MYSQL_CLUSTER_VERSION}-linux2.6-x86_64 mysqlc

# Create necessary directories
sudo mkdir -p /opt/mysqlcluster/deploy/{conf,mysqld_data,ndb_data}
sudo mkdir -p /opt/mysqlcluster/home

# Create MySQL Cluster configuration file
sudo tee /opt/mysqlcluster/home/my.cnf > /dev/null << EOF
[mysqld]
ndbcluster
datadir=/opt/mysqlcluster/deploy/mysqld_data
basedir=/home/ubuntu/mysql-cluster-gpl-${MYSQL_CLUSTER_VERSION}-linux2.6-x86_64/bin/mysqlc
socket=/var/run/mysqld/mysqld.sock
port=3306
EOF

# Create MySQL Cluster config.ini file
sudo tee /opt/mysqlcluster/deploy/conf/config.ini > /dev/null << EOF
[ndb_mgmd]
hostname=$(hostname -f)
datadir=/opt/mysqlcluster/deploy/ndb_data
nodeid=1

[ndbd default]
noofreplicas=1
datadir=/opt/mysqlcluster/deploy/ndb_data

[ndbd]
hostname=ip-172-31-24-120.ec2.internal
nodeid=2

[ndbd]
hostname=ip-172-31-29-199.ec2.internal
nodeid=3

[ndbd]
hostname=ip-172-31-21-246.ec2.internal
nodeid=4

[mysqld]
nodeid=50
EOF

# Initialize MySQL Cluster
sudo scripts/mysql_install_db --no-defaults datadir=/opt/mysqlcluster/deploy/mysqld_data

# Install required library
sudo apt-get update && sudo apt-get -y install libncurses5

# Start MySQL Cluster Management Server
sudo /home/ubuntu/mysql-cluster-gpl-${MYSQL_CLUSTER_VERSION}-linux2.6-x86_64/bin/ndb_mgmd -f /opt/mysqlcluster/deploy/conf/config.ini --initial --configdir=/opt/mysqlcluster/deploy/conf/ --ndb-nodeid=1

# Display cluster configuration and status
/home/ubuntu/mysql-cluster-gpl-${MYSQL_CLUSTER_VERSION}-linux2.6-x86_64/bin/ndb_mgm -e show

echo "MySQL Cluster setup complete."

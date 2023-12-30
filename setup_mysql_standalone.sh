#!/bin/bash

# Update package information and install MySQL Server
sudo apt-get update
sudo apt-get install -y mysql-server

# Run the MySQL secure installation script to enhance security
sudo mysql_secure_installation

echo "MySQL Stand-alone Server setup complete."

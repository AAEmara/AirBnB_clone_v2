#!/usr/bin/env bash
# Setting up our web servers for deployment.
# Installing Nginx.
sudo apt-get update && sudo apt-get -y install nginx 
#Starting Nginx.
sudo service nginx start
# Creating the necessary directories.
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared
# Creating a fake HTML file.
echo "Hello World!" > /data/web_static/releases/test/index.html
# Creating a symbolic link.
ln -sf /data/web_static/releases/test/ /data/web_static/current
# Giving ownership of the /data/ folder to `ubuntu` user, recursively.
sudo chown -R ubuntu:ubuntu /data/
# Configuring the Nginx's configuration file.
sudo sed -i '/^\t}/a\\tlocation \/hbnb_static\/ {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default
# Restarting Nginx after modifying configurations.
sudo service nginx restart

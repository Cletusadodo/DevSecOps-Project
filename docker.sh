#! bin/bash


sudo apt-get update
sudo apt-get install docker.io -y
sudo usermod -aG docker $USER  # Replace with your system's username, e.g., 'ubuntu'
newgrp docker
sudo chmod 777 /var/run/docker.sock


docker build -t netflix .
docker run -d --name netflix -p 8081:80 netflix:latest

#to delete
#docker stop <containerid>
#docker rmi -f netflix

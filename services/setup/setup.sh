#!/bin/bash

if command -v git >/dev/null 2>&1; then
  git clone https://github.com/agresdominik/seb_datascience/
else
  sudo apt install git
  git clone https://github.com/agresdominik/seb_datascience/
fi

if command -v python3 >/dev/null 2>&1; then
  git clone https://github.com/agresdominik/seb_datascience/
else
  sudo apt install python3 python3-pip
fi

cd ./seb_datasience

for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; 
    do sudo apt-get remove $pkg; 
done
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo   "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | 
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

pip install -r ./src/requirements.txt

docker compose -f ./services/grafana/docker-compose.yml up -d 
docker compose -f ./services/homeassistant/docker-compose.yml up -d 
docker compose -f ./services/prometheus/docker-compose.yml up -d 
#!/bin/sh

sudo yum install -y docker

sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker

docker build -t model_api:0.0
docker run -it --name model_api_0.0 -p 5000:5000 model_api:0.0



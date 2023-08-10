# Install Docker
sudo yum install docker -y
sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker
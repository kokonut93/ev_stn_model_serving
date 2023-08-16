# Install AWS CLI
sudo yum install python-setuptools python-pip -y
pip install awscli

# Install Docker
sudo yum install docker -y
sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker
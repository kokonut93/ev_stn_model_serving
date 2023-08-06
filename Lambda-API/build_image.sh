# clone git in AWS EC2
sudo yum update -y
sudo yum install git -y
mkdir api
git clone https://github.com/uoon97/model-api.git

# Install Docker
sudo yum install docker -y
sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker

# Build Docker Image in AWS EC2
cd model-api/lambda-api
docker build -t model_api:0.0 .

# Install AWS CLI
sudo yum install python-setuptools python-pip -y
pip install awscli
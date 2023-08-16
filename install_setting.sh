sudo yum update -y
sudo yum install git -y
git clone http://github.com/hwangpeng-sam/model-serving.git

cd model-serving

# Install Docker
sudo yum install docker -y
sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker
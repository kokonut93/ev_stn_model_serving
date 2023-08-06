# Build Docker Image in AWS EC2
cd model-api/lambda-api
docker build -t model_api:0.0 .

# Install AWS CLI
sudo yum install python-setuptools python-pip -y
pip install awscli
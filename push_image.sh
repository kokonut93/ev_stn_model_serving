# aws configure

# AWS Access Key ID [None]: 
# AWS Secreat Access Key [None]: 
# Default region name [None]: ap-northeast-2
# Default output format [None]: json

export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)
echo "export ACCOUNT_ID=${ACCOUNT_ID}" | tee -a ~/.bash_profile
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com

docker tag model_api:0.0 $ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com/ecr_seokyang:0.0
docker push $ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com/ecr_seokyang:0.0
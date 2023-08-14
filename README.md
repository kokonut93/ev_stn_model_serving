# EV Charger Station Occupancy Prediction Model API
The required input features are as follows.
- number of chargers(slow/fast) : 2 dims
- supply capacity : 1 dim
- location of station(lat/lon) : 2 dims
- average of taxi trip of road link within 500m radius : 1 dim
- proportion of road type within 500m radius(4 road type) : 4 dims
- proportion of district type within 500m radius(5 district type) : 5 dims

Original Repo: https://github.com/easttuna/ev-charger-occupancy-prediction

## How to

Clone git repo on EC2:

    sudo yum update -y
    sudo yum install git -y
    git clone https://github.com/hwangpeng-sam/model-serving.git

Run shell script files to build docker image:

    cd model-serving
    sh install_docker.sh
    sh build_image.sh

After setting aws configure, run the shell script file to push image: <br>
(Modify region, Elastic Container Registry!)

    sh push_image.sh

After create aws lambda function, connect your DB (by creating your private.db_info and inserting values into table) <br>
Lastly, create test event as belows. <br>
( lambda function configuration: Memory(2048 MB), Runtime(1m) ) 


    event = {}



# EV Charger Station Occupancy Prediction Model API

The required input features are as follows.

Station
- Station id : dims = (1,)
- number of chargers(slow/fast) : dims = (2,)
- supply capacity : dims = (1,)
- location of station(lat/lon) : dims = (2,)
- average of taxi trip of road link within 500m radius : dims = (1,)
- proportion of road type within 500m radius(4 road type) : dims = (4,)
- proportion of district type within 500m radius(5 district type) : dims = (5,)

Sequence
- Realtime Sequence : dims = (12, 1)
- Historical Sequence : dims = (4, 1)

Time
- (Time Index, day of week, weekday) : dims = (3,)

<br>

Outputs are as follows.

- Occupancy_20 ~ Occupancy_120 / class(good, normal, bad) : dims = (6, 3)

<br>

Original Repo: https://github.com/easttuna/ev-charger-occupancy-prediction

## How to

Clone git repo on EC2:

    sudo yum update -y
    sudo yum install git -y
    git clone https://github.com/hwangpeng-sam/model-serving.git

Run shell script files to build docker image:

    cd model-serving
    sh setting4build.sh
    sh image_build.sh

After setting aws configure, run the shell script file to push image: <br>
(Modify region, Elastic Container Registry!)

    sh image_push.sh

After create aws lambda function, connect your DB (by creating your private.db_info and inserting values into table) <br>
Lastly, create test event as belows. <br>
( lambda function configuration: Memory(2048 MB), Runtime(1m) ) 

    event = {}



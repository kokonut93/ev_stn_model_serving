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
    git clone https://github.com/uoon97/model-api.git

Run shell script files to build docker image:

    sh build_image.sh

After setting aws configure, run the shell script file to push image: <br>
(Modify region, Elastic Container Registry!)

    sh push_image.sh

After create aws lambda function, create test event below json file. <br>
(lambda function configuration: Memory(2048 MB), Runtime(1m)

    event = {
        "0": {
            "latitude": 39.7145,
            "longitude": 127.9425,
            "capacity": 50,
            "slow": 0,
            "fast": 2,
            "mean_trip": 19,
            "clip_length_city": 15000,
            "clip_length_highway": 4000,
            "clip_length_local": 2301,
            "clip_length_national": 1777,
            "full_length_city": 20000,
            "full_length_highway": 4600,
            "full_length_local": 2600,
            "full_length_national": 2500,
            "indust_ratio": 0,
            "etc_ratio": 0.1,
            "green_ratio": 0.4,
            "commerce_ratio": 0.2,
            "reside_ratio": 0.3
        },
    }

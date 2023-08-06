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

Build the Docker image:

    docker build -t model_api:0.0 .

Run the Container:

    docker run -it --name model_api_0.0 -p 5000:5000 model_api:0.0

From another CMD, send the input features in a request:

    curl -X POST -F file=@img_129.jpg http://localhost:5000/inference

Since the model was not completed yet, the image used in the simple image classification model was used as input.

## Example

![model api by docker with flask](https://github.com/uoon97/model-api/assets/64677725/bbbbdcf9-519f-45d6-8c6a-30d2cca7a861)

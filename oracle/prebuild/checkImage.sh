#!/bin/bash

# Input: name of image we want to run against
IMAGE=$1

# Set image ID to the results of searching docker for that image name
IMAGE_ID=$(docker images -q $IMAGE)

# If the string is non empty then an image id exists
if [ "${IMAGE_ID}" ]; then
    echo true
else
    echo false
fi


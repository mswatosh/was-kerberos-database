#!/bin/bash

# Inputs: URL to clone from, and folder to put it in
URL=$1
FOLDER=$2

# Make sure folder directory doesn't already exist, otherwise, this call would fail
if [ ! -d "$FOLDER" ] ; then
    git clone "$URL" "$FOLDER"
fi
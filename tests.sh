#! usr/bin/bash
DIR="/home/ec2-user/Project_test/"
if [ -d "$DIR" ]; then
    echo Directory "$DIR" exists.
    docker pull urielwo/final_project:latest
    docker images
    docker-compose up -d
    # run tests
else
    echo Directory "$DIR" not exists.
    exit 2 
fi

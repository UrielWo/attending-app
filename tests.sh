#! usr/bin/bash
DIR="/home/ec2-user/Project_test/"
if [ -d "$DIR" ]; then
    echo Directory "$DIR" exists.
    # pull image from docker hub / make it manually first on machine
    # docker compose up
    # run tests
else
    echo Directory "$DIR" not exists.
    exit 2 
fi

#! usr/bin/bash
DIR="/home/ec2-user/Project_test/"
if [ -d "$DIR" ]; then
    echo Directory "$DIR" exists.
    docker pull urielwo/final_project:latest
    docker images
    docker-compose up -d
    sleep 100
    # load .env password // if IP change need to updated on the jenkins manchine
    export $(cat .env | xargs)
    # test 1
    if curl -I "http://"${TESTVM_PUB_IP}":8081/Main" 2>&1 | grep -w "200\|301" ; then
        echo "page is up"
    else
        echo "page is down"
    fi
    # test 2
else
    echo Directory "$DIR" not exists.
    exit 2 
fi

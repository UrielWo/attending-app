#! usr/bin/bash

arg1="$1"
arg2="$2"
DIR="XXXXXXX"

if [[ -n "$1" ]] ; then
   if [ "$arg1" = "test" ]; then
        echo testing;
        # copy files to test server
        sudo scp docker-compose.yml .env tests ec2-user@test:/home/ec2-user/Project_test
        sudo ssh ec2-user@test
        
        # comment
        : '
        if [ -d "$DIR" ]; then
             echo Directory "$DIR" exists.
             # pull image from docker hub
             # docker compose up
             # run tests
        else
             echo Directory "$DIR" not exists.
        fi
       '
   elif [ "$arg1" = "prod" ]; then
       echo product
   else
       echo invalid argument
   fi 
else
    echo argument is empty
    exit 1
fi
if [[ -n "$2" ]] ; then
    echo warning: too much arguments - just one valid test/prod
fi



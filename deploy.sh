#! usr/bin/bash

arg1="$1"
arg2="$2"
DIR="/home/ec2-user/Project_test/"

if [[ -n "$1" ]] ; then
   if [ "$arg1" = "test" ]; then
        echo testing;
        # copy files to test server / need to add tests file
        sudo scp docker-compose.yml .env tests.sh ec2-user@test:/home/ec2-user/Project_test
        sudo ssh -tt ec2-user@test " cd "$DIR" && bash tests.sh && exit "
        echo finish tests successfully
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



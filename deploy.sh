#! usr/bin/bash

arg1="$1"
arg2="$2"

if [[ -n "$1" ]] ; then
   if [ "$arg1" = "test" ]; then
       echo testing
   elif [ "$arg1" = "prod" ]; then
       echo product
   else
       echo invalid argument
   fi 
else
    echo argument is empty
fi
if [[ -n "$2" ]] ; then
    echo warning: too much arguments - just one valid test/prod
fi



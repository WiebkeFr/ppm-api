#! /bin/bash

TRACES=${1:-5}
FILE=$2

BREAK="\n- - - - - - - - - - - - - - - -"

echo $FILE

for (( i=1; i<=$TRACES; i++ ))
do
    echo -e "Start of Trace $i"
    curl -X POST https://cpee.org/flow/start/xml/ -F behavior=fork_running -F xml=@$FILE
    echo -e "\n"
done
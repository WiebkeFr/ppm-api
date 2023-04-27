#! /bin/bash

TRACES=${1:-5}
BREAK="\n- - - - - - - - - - - - - - - -"

for (( i=1; i<=$TRACES; i++ ))
do
    echo -e "Start of Trace $i"
    curl -X POST https://cpee.org/flow/start/xml/ -F behavior=fork_running -F xml=@test-process.xml
    if test $i != $TRACES
    then
        echo -e $BREAK
    fi
done
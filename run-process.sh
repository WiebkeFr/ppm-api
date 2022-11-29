#! /bin/bash

echo "Start"
curl -X POST https://cpee.org/flow/start/xml/ -F behavior=fork freitag -F xml=@test-process.xml
echo "Finish"


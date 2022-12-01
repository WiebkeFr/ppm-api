# ppm-api

### How to start RestAPI?
```
source env/bin/activate
pip3 install -r requirements.txt
uvicorn main:app --host '::1' --port 9009
```

### Overview:
- #### run-process.sh
This is how the bash-script is run
```
>> bash run-process.sh X
```
with **X** being the number of iterations the process should be run. If no number is provided the process is run five times.
- #### test-process.xml

### Endpoints
Endpoints can be found at ```/docs```.
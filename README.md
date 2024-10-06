### Big Data Analysis & Business Intelligence
Big data assignment - 241 semester HCMUT


### Emitter
```
cd ./emitter/
docker-compose up -d # start MQTT broker server
npm install --global mqtt
node emitter.js
```

### Client
```
cd ./client
docker-compose up -d # start Spark service
pip3 install <dependencies>
python3 main.py
```
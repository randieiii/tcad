# TCAD

##Twitch Chat Analyzer DANKHACKERMANS
This application counts the most active user on a twich chat for the last 10 minutes.

Application that is presented can be deployed on AWS.

# Architecture

## Viewer
Service: `viewer` listens to a certain twich channel that is passed in env variable `CHANNEL` and writes all data in csv file in docker is "/home/app/vol" and in database. 
Note: currently this is depends on existing database. 
Requirments:
    - DBHOST: database host
    - DBUSER: postgres username 
    - DB: database in postgres
    - DBPASSWORD: postgres database password
    - NAME: twitch bot/user name
    - API_KEY: twtich api key
    - CHANNEL: twtich channel that you want to listen

## Database
Service: `database` store all logs data. Table look like this 
```
 id | username  | msg  |         timestamp          
----+-----------+------+----------------------------
```

## Analyzer
Service: `analyzer` uses tarnado as a web server. It handle data and create a chart with top 10 most active ppl
Note: currently this is depends on existing database. 
Requirments:
    - DBHOST: database host
    - DBUSER: postgres username 
    - DB: database in postgres
    - DBPASSWORD: postgres database password
    - CHANNEL: table name should be the same as name of channel 

Quick start:
```
aws cloudformation create-stack --template-body file://Deployment.yml --stack-name sodapoppin-viewer --parameters ParameterKey=ListnerUsername,ParameterValue=${NAME} ParameterKey=TwitchApiKey,ParameterValue=${API_KEY} ParameterKey=Channel,ParameterValue=sodapoppin ParameterKey=KeyName,ParameterValue=test-key
```
Local deployment:
```
#This should work if you define all env variables that required. (${DBPASS}, ${CHANNEL}, ${API_KEY}, ${NAME})
docker-compose up 
```
![](https://cdn.betterttv.net/emote/5e37903f61ff6b51e652837c/3x)

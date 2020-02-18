# TCAD

##Twitch Chat Analyzer DANKHACKERMANS

Quick start:
```
aws cloudformation create-stack --template-body file://Deployment.yml --stack-name sodapoppin-viewer --parameters ParameterKey=ListnerUsername,ParameterValue=${NAME} ParameterKey=TwitchApiKey,ParameterValue=${API_KEY} ParameterKey=Channel,ParameterValue=sodapoppin ParameterKey=KeyName,ParameterValue=test-key
```
Local deployment:
```
docker run  -v /tmp:/home/app/vol -e NAME=$NAME -e API_KEY=$API_KEY -e CHANNEL=sodapoppin --restart always 438ffcb0e55e
```
![](https://cdn.betterttv.net/emote/5e37903f61ff6b51e652837c/3x)

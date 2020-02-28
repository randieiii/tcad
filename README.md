# TCAD

## Twitch Chat Analyzer DANKHACKERMANS
![](https://cdn.betterttv.net/emote/5e37903f61ff6b51e652837c/3x)
<br />
This application creates templates for posts on reddit which represents some usless statistics(SUS) about a stream based on twitch chat log.

#####Help to pay bills for servers here:
<style>.bmc-button img{height: 34px !important;width: 35px !important;margin-bottom: 1px !important;box-shadow: none !important;border: none !important;vertical-align: middle !important;}.bmc-button{padding: 7px 10px 7px 10px !important;line-height: 35px !important;height:51px !important;min-width:217px !important;text-decoration: none !important;display:inline-flex !important;color:#ffffff !important;background-color:#79D6B5 !important;border-radius: 5px !important;border: 1px solid transparent !important;padding: 7px 10px 7px 10px !important;font-size: 28px !important;letter-spacing:0.6px !important;box-shadow: 0px 1px 2px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;margin: 0 auto !important;font-family:'Cookie', cursive !important;-webkit-box-sizing: border-box !important;box-sizing: border-box !important;-o-transition: 0.3s all linear !important;-webkit-transition: 0.3s all linear !important;-moz-transition: 0.3s all linear !important;-ms-transition: 0.3s all linear !important;transition: 0.3s all linear !important;}.bmc-button:hover, .bmc-button:active, .bmc-button:focus {-webkit-box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;text-decoration: none !important;box-shadow: 0px 1px 2px 2px rgba(190, 190, 190, 0.5) !important;opacity: 0.85 !important;color:#ffffff !important;}</style><link href="https://fonts.googleapis.com/css?family=Cookie" rel="stylesheet"><a class="bmc-button" target="_blank" href="https://www.buymeacoffee.com/QUlswbe"><img src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg" alt="Buy me a coffee"><span style="margin-left:15px;font-size:28px !important;">Buy me a coffee</span></a>

## Architecture

### Viewer
***Service***: `viewer` listens to multiple twich channels which via env variable `CHANNELS` and writes all data in postgres database in database.   <br />
**Note**: present code is garbanzo, do not look in src for viewer , I'm working on it.    <br />
**Requirments**: 
- `DBHOST`: database host
- `DBUSER`: postgres username 
- `DB`: database in postgres
- `DBPASSWORD`: postgres database password
- `NAME`: twitch bot/user name
- `API_KEY`: twtich chat api key(not the same as TW_API_KEY - make a google requests - "chatbots twitch" - https://en.lmgtfy.com/?q=chatbots+twitch&pp=1)
- `CHANNELS`: twtich channels which you want to listen (I'm listening to #pokelawls, #nmplol, #forsen, #sodapoppin, #greekgodx)
- `TW_API_KEY`: twitch api key

### Database
***Service***: `database` store all logs data. Table looks like this 
```
 id | username  | msg  |         timestamp          
----+-----------+------+----------------------------
```

### Analyzer
***Service***: `analyzer` makes some useless analitics for parsed data(like top 10 ppl who spammed the most or 10 the most spammed words or searching for word fat and ugly and stupid and dumb(all words in a file:`searchablew` )) in database and returns a zip file. <br />
**Note**: currently code is also a shitshow,I'm also working on it.<br />
**Requirments**:<br />
- `DBHOST`: database host
- `DBUSER`: postgres username 
- `DB`: database in postgres
- `DBPASSWORD`: postgres database password

## Quick start:
### Cloud/AWS deployment 
App can be deployed on 2 AWS t2.micro instances like that:
```
aws cloudformation create-stack --template-body file://Deployment.yml --stack-name viewer --parameters \
    ParameterKey=ListnerUsername,ParameterValue=${NAME} \
    ParameterKey=TwitchApiKey,ParameterValue=${API_KEY} \
    ParameterKey=Channels,ParameterValue='sodapoppin:pokelawls:greekgodx:nmplol:forsen' \
    ParameterKey=Channel,ParameterValue=sodapoppin \
    ParameterKey=KeyName,ParameterValue=test-key \
    ParameterKey=TwApi,ParameterValue=${TWAPI} \
    ParameterKey=DBPASS,ParameterValue=${DBPASS}
```
### Local deployment:
Or it can be tested locally. <br />
This should work if you define all env variables that required. (`${DBPASS}`,`${TWAPI}`, `${CHANNEL}`, `${API_KEY}`, `${NAME}`) <br />
You can see it in field environment in file - docker-compose.yml  <br />
```
docker-compose up 
```


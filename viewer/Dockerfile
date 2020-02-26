FROM node:10
RUN apt-get update 
COPY . /home/app
WORKDIR /home/app/
RUN npm install 

CMD [ "node", "./chat_crawler.js" ]
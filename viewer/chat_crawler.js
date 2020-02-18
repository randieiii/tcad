const tmi = require('tmi.js');
const fs = require('fs');
const cowsay = require('cowsay');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const CHANNEL = process.env.CHANNEL
const NAME = process.env.NAME
const API_KEY = process.env.API_KEY

// Define configuration options
const opts = {
  identity: {
    username: NAME,
    password: API_KEY
  },
  channels: [
    CHANNEL
  ]
};
// Create a client with our options
const client = new tmi.client(opts);
const exclude = [""]
// let writeStream = fs.createWriteStream(`./vol/chat${Date.now()}.txt`);
const csvWriter = createCsvWriter({
  path: `./vol/chat${Date.now()}.txt`,
  header: [
    {id: 'username', title: 'USERNAME'},
    {id: 'msg', title: 'MSG'}
  ]
})
// Register our event handlers (defined below)
client.on('message', onMessageHandler);
client.on('connected', onConnectedHandler);

// Connect to Twitch:
client.connect();

// Called every time a message comes in
function onMessageHandler (target, context, msg, self) {
  if (self) { return; } // Ignore messages from the bot

  if (!context.username.match(/bot|streamelements/g)) {
    console.log(cowsay.think({
      text : msg,
      cow : 'C3PO',
      mode: 'g'
    }) )  
    // console.log(context)
    csvWriter.writeRecords([
      {username: context.username,  msg: msg}
    ])
    // writeStream.write(`${msg}\n`);
  }
}


// Called every time the bot connects to Twitch chat
function onConnectedHandler (addr, port) {
  console.log(`* Connected to ${addr}:${port}`);
}
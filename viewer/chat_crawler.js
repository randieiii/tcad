const tmi = require('tmi.js');
const cowsay = require('cowsay');
const { Pool, Client } = require('pg')
const request = require('request');

const CHANNELS = process.env.CHANNELS.split(" ");
const NAME = process.env.NAME
const API_KEY = process.env.API_KEY
const TW_API_KEY = process.env.TWAPI
const DB = {
  user: process.env.DBUSER,
  host: process.env.DBHOST,
  database: process.env.DB,
  password: process.env.DBPASSWORD,
  port: 5432,
}


var activeChannel = new Set();

function getActive(channel) {
  const options = {
    url: `https://api.twitch.tv/helix/streams?user_login=${channel.replace("#","")}`,
    headers: {
      'Client-ID': TW_API_KEY
    }
  };

  request(options, function (error, response, body) {
    if (!error && response.statusCode == 200) {
      const info = JSON.parse(body);
      console.log(`Response = ${info.data}`)
      info.data != 0 ? activeChannel.add(channel) : activeChannel.delete(channel);
    }
  });
}

var getOnlyActiveChannel = function() {
  CHANNELS.forEach(getActive)
  console.log(activeChannel)
}

setInterval(getOnlyActiveChannel, 10000)
const dbclient = new Client(DB)
dbclient.connect()

var itemsProcessed = 0;

function createTable(channel) {
  dbclient.query(`CREATE TABLE IF NOT EXISTS ${channel} (id serial PRIMARY KEY, username VARCHAR (64) NOT NULL, msg TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);`, (err, res) => {
    console.log(err, res)
    itemsProcessed++;
    if(itemsProcessed === CHANNELS.length) {
      dbclient.end()
    }
  })
}

CHANNELS.forEach(createTable)
const pool = new Pool(DB)

const opts = {
  identity: {
    username: NAME,
    password: API_KEY
  },
  channels: CHANNELS
};

const client = new tmi.client(opts);

client.on('message', onMessageHandler);
client.on('connected', onConnectedHandler);
client.connect();

// Called every time a message comes in
function onMessageHandler (target, context, msg, self) {
  table = target.replace("#","")
  if (self) { return; } // Ignore messages from the bot

  if (!context.username.match(/bot|streamelements/g) && activeChannel.has(target)) {
    console.log(cowsay.think({
      text : msg,
      cow : 'C3PO',
      mode: 'g'
    }) )  

    pool.query(`INSERT into ${table} (username, msg) VALUES($1, $2);`, [context.username, msg], (err, res) => {
      console.log(err, res)
    })
  }
}

function onConnectedHandler (addr, port) {
  console.log(`* Connected to ${addr}:${port}`);
}
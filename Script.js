var WebHDFS = require('webhdfs');
var hdfs = WebHDFS.createClient({
    user: 'andrei',
    host: 'localhost',
    port: 9870,
    path: '/webhdfs/v1'
  });
var fs = require('fs');

var localFileStream = fs.createReadStream('/home/andrei/hadoop-kekw/hadoop-kekw/vol/chat1581689476859.txt');
var remoteFileStream = hdfs.createWriteStream('/user/andrei/ollo.txt');

localFileStream.pipe(remoteFileStream);

remoteFileStream.on('error', function onError (err) {
  console.log(err)
});

// remoteFileStream.on('finish', function onFinish () {
//   console.log("Done")
// });

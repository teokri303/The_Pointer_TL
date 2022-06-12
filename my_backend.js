var createError = require('http-errors');
var express = require('express');
var path = require('path');
var bodyParser = require('body-parser');
var cors = require('cors')
const geolib = require('geolib')

var http = require('http');
var util = require('util');
var mysql = require('mysql');
const url = require('url');
var formidable = require('formidable');

var haversine = require("haversine-distance");

var app = express();

// view engine setup
app.set('views', path.join(__dirname, '/'));
app.set('view engine', 'ejs');


//gia updated event info
app.all('/updated_event_info',function (req, res) {
  console.log('Request received: ');
  util.inspect(req) // this line helps you inspect the request so you can see whether the data is in the url (GET) or the req body (POST)
  util.log('Request recieved: \nmethod: ' + req.method + '\nurl: ' + req.url) // this line logs just the method and url
  if(req.method==='OPTIONS'){
          res.writeHead(200);
          res.end();
    }else if(req.method==='POST'){
      var body = [];
      //h katallhlh kefalida
      res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
      });
      //diavase data
      req.on("data", (chunk) => {
        console.log(chunk);
        body.push(chunk);
      });
      //otan exeis diavasei olo to data
      req.on("end", () => {
        var mdata = Buffer.concat(body).toString();
        mdata = JSON.parse(mdata);//parsing json
        var con = mysql.createConnection({
          host: "localhost",
          user: "root",
          password: "Den8aKsexasw",
          database: "mapp",
          multipleStatements: true
        });
        con.connect(async function(err) {
          var j = false;
          console.log("Connected");
          const query = util.promisify(con.query).bind(con);//gia na exw promises
          //check if user has joined before
          var mquery = "select * from to_event where uid="+mdata.user.id+" and eid="+mdata.event.id+";";
          result = await query(mquery);
          if (result.length > 0 ){
            //user has joined...
            j = true;
          }
          //only event info
          var mquery = "select * from event where name like \'"+mdata.event.name+"\' and id="+mdata.event.id+";";
          result = await query(mquery);
          message = {info : result, joined : j};
          res.write(JSON.stringify(message));
          res.end();
        });//telos connect

      res.on('error', (err) => {
        console.error(err);
      });
    });//req on end
  }//end if
});
//gia updated event info
//plh8os friends
app.all('/get_friends',function (req, res) {
  console.log('Request received: ');
  util.inspect(req) // this line helps you inspect the request so you can see whether the data is in the url (GET) or the req body (POST)
  util.log('Request recieved: \nmethod: ' + req.method + '\nurl: ' + req.url) // this line logs just the method and url
  if(req.method==='OPTIONS'){
          res.writeHead(200);
          res.end();
    }else if(req.method==='POST'){
      var body = [];
      //h katallhlh kefalida
      res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
      });
      //diavase data
      req.on("data", (chunk) => {
        console.log(chunk);
        body.push(chunk);
      });
      //otan exeis diavasei olo to data
      req.on("end", () => {
        var mdata = Buffer.concat(body).toString();
        mdata = JSON.parse(mdata);//parsing json
        console.log(mdata);
        var con = mysql.createConnection({//sundesh se vash
          host: "localhost",
          user: "root",
          password: "Den8aKsexasw",
          database: "softeng22",
          multipleStatements: true
        });
        con.connect(async function(err) {
          console.log("Connected");
          const query = util.promisify(con.query).bind(con);//gia na exw promises
          //den kserw an 8a xreiastei security...
          // ? var mquery = "SELECT * FROM location WHERE name like \'%"+mdata.name+"%\' AND lat = "+mdata.coords.lat+" AND lon = "+mdata.coords.lon+";"
          var mquery = "SELECT t2.* FROM (Select * from friend_request WHERE username_1 like \'"+mdata.username+"\'AND state_1=\'accepted\' AND state_2=\'accepted\') as t1 INNER JOIN (select * from user) as t2 ON t2.username=t1.username_2 ;";
          var info_result = await query(mquery);
          var c_array = [];
          for( k in info_result){
            var mquery = "SELECT count(*) FROM friend_request WHERE username_1 like \'"+info_result[k].username+"\'AND state_1=\'accepted\' AND state_2=\'accepted\';";
            c_array.push( await query(mquery) );
          }
          res.write(JSON.stringify({info : info_result,count : c_array}));
          res.end();
        });//telos connect

      res.on('error', (err) => {
        console.error(err);
      });
    });//req on end
  }//end if
});
//plh8os filwn

//gia friend request
app.all('/send_friend_request',function (req, res) {
  console.log('Request received: ');
  util.inspect(req) // this line helps you inspect the request so you can see whether the data is in the url (GET) or the req body (POST)
  util.log('Request recieved: \nmethod: ' + req.method + '\nurl: ' + req.url) // this line logs just the method and url
  if(req.method==='OPTIONS'){
          res.writeHead(200);
          res.end();
    }else if(req.method==='POST'){
      var body = [];
      //h katallhlh kefalida
      res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
      });
      //diavase data
      req.on("data", (chunk) => {
        console.log(chunk);
        body.push(chunk);
      });
      //otan exeis diavasei olo to data
      req.on("end", () => {
        var mdata = Buffer.concat(body).toString();
        mdata = JSON.parse(mdata);//parsing json
        mdata = mdata.msg;                                  //prosexe to ligo ayto...
        var con = mysql.createConnection({//sundesh se vash
          host: "localhost",
          user: "root",
          password: "Den8aKsexasw",
          database: "softeng22",
          multipleStatements: true
        });
        con.connect(function(err) {
          console.log("Connected");
          const query = util.promisify(con.query).bind(con);//gia na exw promises
          //den kserw an 8a xreiastei security...
          // ? var mquery = "SELECT * FROM location WHERE name like \'%"+mdata.name+"%\' AND lat = "+mdata.coords.lat+" AND lon = "+mdata.coords.lon+";"
          var mquery = "INSERT INTO friend_request(id_1,id_2,username_1,username_2,state_1,state_2) VALUES ("+mdata.id1+","+mdata.id2+",\'"+mdata.username1+"\' ,\'"+mdata.username2+"\',\'accepted\',\'pending\'),("+mdata.id2+","+mdata.id1+",\'"+mdata.username2+"\' ,\'"+mdata.username1+"\',\'pending\',\'accepted\');";
          con.query(mquery, function (err, result, fields) {
            if (err){
              throw err;
            }
            res.write(JSON.stringify({info : '1'}));
            res.end();
          });//telos query gia info
        });//telos connect

      res.on('error', (err) => {
        console.error(err);
      });
    });//req on end
  }//end if
});
//send friend request
//accept FriendRequest
app.all('/accept_friend_request',function (req, res) {
  console.log('Request received: ');
  util.inspect(req) // this line helps you inspect the request so you can see whether the data is in the url (GET) or the req body (POST)
  util.log('Request recieved: \nmethod: ' + req.method + '\nurl: ' + req.url) // this line logs just the method and url
  if(req.method==='OPTIONS'){
          res.writeHead(200);
          res.end();
    }else if(req.method==='POST'){
      var body = [];
      //h katallhlh kefalida
      res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
      });
      //diavase data
      req.on("data", (chunk) => {
        console.log(chunk);
        body.push(chunk);
      });
      //otan exeis diavasei olo to data
      req.on("end", () => {
        var mdata = Buffer.concat(body).toString();
        mdata = JSON.parse(mdata);//parsing json
        console.log(mdata);
        var con = mysql.createConnection({//sundesh se vash
          host: "localhost",
          user: "root",
          password: "Den8aKsexasw",
          database: "softeng22",
          multipleStatements: true
        });
        con.connect(function(err) {
          console.log("Connected");
          const query = util.promisify(con.query).bind(con);//gia na exw promises
          var mquery = "UPDATE friend_request SET state_1= \'" + mdata.state_1 + "\',state_2=\'" + mdata.state_2 + "\' WHERE (username_1 like \'"+mdata.sender+"\'AND username_2 like \'"+mdata.receiver+"\') OR"+"(username_1 like \'"+mdata.receiver+"\'AND username_2 like \'"+mdata.sender+"\')"+";";
          con.query(mquery, function (err, result, fields) {
            if (err){
              throw err;
            }
            res.write(JSON.stringify({info : result}));
            res.end();
          });//telos query gia info
        });//telos connect

      res.on('error', (err) => {
        console.error(err);
      });
    });//req on end
  }//end if
});
//accept FriendRequest
//reject FriendRequest
app.all('/reject_friend_request',function (req, res) {
  console.log('Request received: ');
  util.inspect(req) // this line helps you inspect the request so you can see whether the data is in the url (GET) or the req body (POST)
  util.log('Request recieved: \nmethod: ' + req.method + '\nurl: ' + req.url) // this line logs just the method and url
  if(req.method==='OPTIONS'){
          res.writeHead(200);
          res.end();
    }else if(req.method==='POST'){
      var body = [];
      //h katallhlh kefalida
      res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
      });
      //diavase data
      req.on("data", (chunk) => {
        console.log(chunk);
        body.push(chunk);
      });
      //otan exeis diavasei olo to data
      req.on("end", () => {
        var mdata = Buffer.concat(body).toString();
        mdata = JSON.parse(mdata);//parsing json
        console.log(mdata);
        var con = mysql.createConnection({//sundesh se vash
          host: "localhost",
          user: "root",
          password: "Den8aKsexasw",
          database: "softeng22",
          multipleStatements: true
        });
        con.connect(function(err) {
          console.log("Connected");
          const query = util.promisify(con.query).bind(con);//gia na exw promises
          var mquery = "DELETE FROM friend_request WHERE (username_1 like \'"+mdata.self+"\'AND username_2 like \'"+mdata.you+"\') OR"+"(username_1 like \'"+mdata.you+"\'AND username_2 like \'"+mdata.self+"\')"+";";
          con.query(mquery, function (err, result, fields) {
            if (err){
              throw err;
            }
            res.write(JSON.stringify({info : result}));
            res.end();
          });//telos query gia info
        });//telos connect

      res.on('error', (err) => {
        console.error(err);
      });
    });//req on end
  }//end if
});
//reject FriendRequest
//retrieve friend requests
app.all('/get_friend_request',function (req, res) {
  console.log('Request received: ');
  util.inspect(req) // this line helps you inspect the request so you can see whether the data is in the url (GET) or the req body (POST)
  util.log('Request recieved: \nmethod: ' + req.method + '\nurl: ' + req.url) // this line logs just the method and url
  if(req.method==='OPTIONS'){
          res.writeHead(200);
          res.end();
    }else if(req.method==='POST'){
      var body = [];
      //h katallhlh kefalida
      res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
      });
      //diavase data
      req.on("data", (chunk) => {
        console.log(chunk);
        body.push(chunk);
      });
      //otan exeis diavasei olo to data
      req.on("end", () => {
        var mdata = Buffer.concat(body).toString();
        mdata = JSON.parse(mdata);//parsing json
        var con = mysql.createConnection({//sundesh se vash
          host: "localhost",
          user: "root",
          password: "Den8aKsexasw",
          database: "softeng22",
          multipleStatements: true
        });
        con.connect(function(err) {
          console.log("Connected");
          const query = util.promisify(con.query).bind(con);//gia na exw promises
          //den kserw an 8a xreiastei security...
          // ? var mquery = "SELECT * FROM location WHERE name like \'%"+mdata.name+"%\' AND lat = "+mdata.coords.lat+" AND lon = "+mdata.coords.lon+";"
          var mquery = "SELECT * FROM friend_request WHERE username_1 like \'"+mdata.username+"\'AND state_1=\'pending\';";
          con.query(mquery, function (err, result, fields) {
            if (err){
              throw err;
            }
            res.write(JSON.stringify({info : result}));
            res.end();
          });//telos query gia info
        });//telos connect

      res.on('error', (err) => {
        console.error(err);
      });
    });//req on end
  }//end if
});
//retrieve friend requests
//Check if Friend or Friend_Request
app.all('/check_if_friend',function (req, res) {
  console.log('Request received: ');
  util.inspect(req) // this line helps you inspect the request so you can see whether the data is in the url (GET) or the req body (POST)
  util.log('Request recieved: \nmethod: ' + req.method + '\nurl: ' + req.url) // this line logs just the method and url
  if(req.method==='OPTIONS'){
          res.writeHead(200);
          res.end();
    }else if(req.method==='POST'){
      var body = [];
      //h katallhlh kefalida
      res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
      });
      //diavase data
      req.on("data", (chunk) => {
        console.log(chunk);
        body.push(chunk);
      });
      //otan exeis diavasei olo to data
      req.on("end", () => {
        var mdata = Buffer.concat(body).toString();
        mdata = JSON.parse(mdata);//parsing json
        console.log(mdata);
        var con = mysql.createConnection({//sundesh se vash
          host: "localhost",
          user: "root",
          password: "Den8aKsexasw",
          database: "softeng22",
          multipleStatements: true
        });
        con.connect(async function(err) {
          console.log("Connected");
          var to_send = {info : '1', at_event : '1'}
          const query = util.promisify(con.query).bind(con);//gia na exw promises
          var mquery = "SELECT * FROM friend_request WHERE username_1 like \'"+mdata.self.username+"\' AND username_2 like \'"+mdata.user.username+"\';";
          var result = await query(mquery);
          if(result.length > 0){
            to_send.info = '1';
          }else{
            to_send.info = '0';
          }
          var mquery = "SELECT * FROM at_event WHERE uid like \'"+mdata.user.id+"\';";
          result = await query(mquery);
          if(result.length > 0){
            to_send.at_event = '1';
          }else{
            to_send.at_event = '0';
          }
          res.write(JSON.stringify(to_send));
          res.end();
        });//telos connect

      res.on('error', (err) => {
        console.error(err);
      });
    });//req on end
  }//end if
});
//Check if Friend or Friend Request

//get users with name
app.all('/simple_search',async function (req, res) {
  console.log('Request received: ');
  util.inspect(req) // this line helps you inspect the request so you can see whether the data is in the url (GET) or the req body (POST)
  util.log('Request recieved: \nmethod: ' + req.method + '\nurl: ' + req.url) // this line logs just the method and url
  if(req.method==='OPTIONS'){
          res.writeHead(200);
          res.end();
    }else if(req.method==='POST'){
      var body = [];
      //h katallhlh kefalida
      res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
      });
      //diavase data
      req.on("data", (chunk) => {
        console.log(chunk);
        body.push(chunk);
      });
      //otan exeis diavasei olo to data
      req.on("end",async () => {
        var mdata = Buffer.concat(body).toString();
        mdata = JSON.parse(mdata);//parsing json
        var con = mysql.createConnection({
          host: "localhost",
          user: "root",
          password: "Den8aKsexasw",
          database: "softeng22",
          multipleStatements: true
        });
        con.connect(async function(err) {
          console.log("Connected");
          //const query = util.promisify(con.query).bind(con);//g9ia na exw promises
          var mquery = "SELECT * FROM user WHERE username like \'"+mdata.name+"%\';"
          con.query(mquery,async function (err, result, fields) {
            if (err){
              throw err;
            }
            message = {info : result};
            res.write(JSON.stringify(message));
            res.end();
          });//telos query gia info
        });//telos connect

      res.on('error', (err) => {
        console.error(err);
      });
    });//req on end
  }//end if
});
//get users with name
//gia join event
app.all('/join_event',function (req, res) {
  console.log('Request received: ');
  util.inspect(req) // this line helps you inspect the request so you can see whether the data is in the url (GET) or the req body (POST)
  util.log('Request recieved: \nmethod: ' + req.method + '\nurl: ' + req.url) // this line logs just the method and url
  if(req.method==='OPTIONS'){
          res.writeHead(200);
          res.end();
    }else if(req.method==='POST'){
      var body = [];
      //h katallhlh kefalida
      res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
      });
      //diavase data
      req.on("data", (chunk) => {
        console.log(chunk);
        body.push(chunk);
      });
      //otan exeis diavasei olo to data
      req.on("end", () => {
        var mdata = Buffer.concat(body).toString();
        mdata = JSON.parse(mdata);//parsing json
        var con = mysql.createConnection({
          host: "localhost",
          user: "root",
          password: "Den8aKsexasw",
          database: "softeng22",
          multipleStatements: true
        });
        con.connect(async function(err) {
          console.log("Connected");
          const query = util.promisify(con.query).bind(con);//gia na exw promises
          var mquery = "select * from to_event where uid="+mdata.user.id+" and eid="+mdata.event.id+";";//an exei mpei pali
          result = await query(mquery);
          if (result.length == 0 ){
            var mquery = "insert into to_event values ("+mdata.user.id+","+mdata.event.id+");";
            con.query(mquery, async function (err, result, fields) {
              if (err){
                throw err;
              }
              message = {info : true, msg : "Joined Succesfully !"};
              res.write(JSON.stringify(message));
              res.end();
            });//telos query gia info
            var mquery = "update user set points = "+ mdata.user.points+" where username like \'"+mdata.user.username+"\';";
            con.query(mquery, async function (err, result, fields) {
              if (err){
                throw err;
              }
            });
            //vazw +1 sto counter
            mquery = "update event set counter = counter + 1 where id like \'"+mdata.event.id+"\';";
            con.query(mquery, async function (err, result, fields) {
              if (err){
                throw err;
              }
            });//telos query gia info
          }else{
            message = {info : false,msg : "You have joined this event before."};
            res.write(JSON.stringify(message));
            res.end();
          }
        });//telos connect

      res.on('error', (err) => {
        console.error(err);
      });
    });//req on end
  }//end if
});
//gia join event
//gia event creation
app.all('/event_creation',async function (req, res) {
  console.log('Request received: ');
  util.inspect(req) // this line helps you inspect the request so you can see whether the data is in the url (GET) or the req body (POST)
  util.log('Request recieved: \nmethod: ' + req.method + '\nurl: ' + req.url) // this line logs just the method and url
  if(req.method==='OPTIONS'){
          res.writeHead(200);
          res.end();
    }else if(req.method==='POST'){
      var body = [];
      //h katallhlh kefalida
      res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
      });
      //diavase data
      req.on("data", (chunk) => {
        console.log(chunk);
        body.push(chunk);
      });
      //otan exeis diavasei olo to data
      req.on("end",async () => {
        var mdata = Buffer.concat(body).toString();
        mdata = JSON.parse(mdata);//parsing json
        var con = mysql.createConnection({
          host: "localhost",
          user: "root",
          password: "Den8aKsexasw",
          database: "softeng22",
          multipleStatements: true
        });
        con.connect(async function(err) {
          console.log("Connected");
          console.log(mdata);
          const query = util.promisify(con.query).bind(con);//g9ia na exw promises
          var mquery = "SELECT * FROM event WHERE name like \'%"+mdata.name+"%\' AND creator_id = "+mdata.creator_id+" ;"
          con.query(mquery,async function (err, result, fields) {
            if (err){
              throw err;
            }
            if(result.length > 0){
              message = {info : "Event Exists"};
              res.write(JSON.stringify(message));
              res.end();
            }else{
              var mquery = "INSERT INTO event(name,lon,lat,cap,starts,ends,points_r,private,creator_name,creator_email,creator_id) VALUES (\'"+mdata.name+"\' ,"+mdata.lon+","+ mdata.lat+","+mdata.cap+",\'"+mdata.starts+"\',\'"+ mdata.ends+"\',"+mdata.points_r+","+mdata.private+",\'"+mdata.creator_name+"\',\'"+mdata.creator_email+"\',\'"+mdata.creator_id+"\');";
              result = await query(mquery);
              var mquery = "select id from event where (name like \'"+mdata.name+"\') and (lon = \'"+mdata.lon+"\') and (lat = \'"+mdata.lat+"\') and (creator_id = "+mdata.creator_id+");";
              result = await query(mquery);//edw 8elw na vazw ws summetoxh ton xrhsth
              res.write(JSON.stringify({info : '1',eid : result[0]}));
              res.end();
            }
          });//telos query gia info
        });//telos connect
        res.on('error', (err) => {
          console.error(err);
        });
      });//req on end
    }//end if
  });
//event creation
//gia get_available_events
app.all('/get_available_events',function (req, res) {
  console.log('Request received: ');
  util.inspect(req) // this line helps you inspect the request so you can see whether the data is in the url (GET) or the req body (POST)
  util.log('Request recieved: \nmethod: ' + req.method + '\nurl: ' + req.url) // this line logs just the method and url
  if(req.method==='OPTIONS'){
          res.writeHead(200);
          res.end();
    }else if(req.method==='POST'){
      var body = [];
      //h katallhlh kefalida
      res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
      });
      //diavase data
      req.on("data", (chunk) => {
        console.log(chunk);
        body.push(chunk);
      });
      //otan exeis diavasei olo to data
      req.on("end", () => {
        var mdata = Buffer.concat(body).toString();
        mdata = JSON.parse(mdata);//parsing json
        console.log(mdata);
        var con = mysql.createConnection({
          host: "localhost",
          user: "root",
          password: "Den8aKsexasw",
          database: "softeng22",
          multipleStatements: true
        });
        con.connect(function(err) {
          console.log("Connected");
          //dhmiourgia tetragwnou
          //gia arxh 8a ta pernaw egw ta km
          var the_rect = calcRectangle(mdata.coords,10);
          console.log(the_rect);
          const query = util.promisify(con.query).bind(con);//gia na exw promises
          var mquery = "select * from event where (lat <= "+the_rect[0].latitude+" and lat >="+the_rect[2].latitude+" and lon <= "+the_rect[1].longitude+" and lon >= "+the_rect[3].longitude+");";
          con.query(mquery, async function (err, result, fields) {
            if (err){
              throw err;
            }
            console.log(result);
            message = {info : result};
            res.write(JSON.stringify(message));
            res.end();
          });//telos query gia info
        });//telos connect

      res.on('error', (err) => {
        console.error(err);
      });
    });//req on end
  }//end if
});
//gia events_available
//gia get_expired_events
app.all('/get_expired_events',function (req, res) {
  console.log('Request received: ');
  util.inspect(req) // this line helps you inspect the request so you can see whether the data is in the url (GET) or the req body (POST)
  util.log('Request recieved: \nmethod: ' + req.method + '\nurl: ' + req.url) // this line logs just the method and url
  if(req.method==='OPTIONS'){
          res.writeHead(200);
          res.end();
    }else if(req.method==='POST'){
      var body = [];
      //h katallhlh kefalida
      res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
      });
      //diavase data
      req.on("data", (chunk) => {
        console.log(chunk);
        body.push(chunk);
      });
      //otan exeis diavasei olo to data
      req.on("end", () => {
        var mdata = Buffer.concat(body).toString();
        mdata = JSON.parse(mdata);//parsing json
        console.log(mdata);
        var con = mysql.createConnection({
          host: "localhost",
          user: "root",
          password: "Den8aKsexasw",
          database: "softeng22",
          multipleStatements: true
        });
        con.connect(function(err) {
          console.log("Connected");
          const query = util.promisify(con.query).bind(con);//gia na exw promises
          var mquery = "select t1.* from (select * from event )as t1 INNER JOIN (select * from to_event where uid = "+mdata.id+") as t2 on t1.id=t2.eid;";
          con.query(mquery, async function (err, result, fields) {
            if (err){
              throw err;
            }
            console.log(result);
            message = {info : result};
            res.write(JSON.stringify(message));
            res.end();
          });//telos query gia info
        });//telos connect

      res.on('error', (err) => {
        console.error(err);
      });
    });//req on end
  }//end if
});
//gia events_available
//vazw pou eimai
app.all('/login',function (req, res) {
  console.log('Request received: ');
  util.inspect(req) // this line helps you inspect the request so you can see whether the data is in the url (GET) or the req body (POST)
  util.log('Request recieved: \nmethod: ' + req.method + '\nurl: ' + req.url) // this line logs just the method and url
  if(req.method==='OPTIONS'){
          res.writeHead(200);
          res.end();
    }else if(req.method==='POST'){
      var body = [];
      //h katallhlh kefalida
      res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
      });
      //diavase data
      req.on("data", (chunk) => {
        console.log(chunk);
        body.push(chunk);
      });
      //otan exeis diavasei olo to data
      req.on("end", () => {
        var mdata = Buffer.concat(body).toString();
        mdata = JSON.parse(mdata);//parsing json
        mdata = mdata.msg;
        var con = mysql.createConnection({
          host: "localhost",
          user: "root",
          password: "Den8aKsexasw",
          database: "softeng22",
          multipleStatements: true
        });
        con.connect(function(err) {
          console.log("Connected");
          const query = util.promisify(con.query).bind(con);//g9ia na exw promises
          var mquery = "SELECT * FROM user WHERE username like \'"+mdata.username+"\' AND email like \'"+mdata.email+"\';";
          con.query(mquery, async function (err, result, fields) {
            if (err){
              throw err;
            }
            if(result.length == 0){
              message = {info : 0,msg :"Invalid Username or E-Mail"};
              res.write(JSON.stringify(message));
              res.end();
            }else{
              var mquery = "UPDATE user SET lat="+mdata.coords.lat+",lon="+mdata.coords.lon+",online=1 WHERE username like \'%"+mdata.username+"%\' AND email like \'%"+mdata.email+"%\';";
              query(mquery);
              var mquery = "SELECT count(*) FROM friend_request WHERE username_1 like \'"+mdata.username+"\'AND state_1=\'accepted\' AND state_2=\'accepted\';";
              num_of_friends = await query(mquery);
              message = {info : '1',msg : result[0],count : num_of_friends};
              res.write(JSON.stringify(message));
              res.end();
            }
          });//telos query gia info
        });//telos connect

      res.on('error', (err) => {
        console.error(err);
      });
    });//req on end
  }//end if
});
//gia login
//gia register
app.all('/register',function (req, res) {
  console.log('Request received: ');
  util.inspect(req) // this line helps you inspect the request so you can see whether the data is in the url (GET) or the req body (POST)
  util.log('Request recieved: \nmethod: ' + req.method + '\nurl: ' + req.url) // this line logs just the method and url
  if(req.method==='OPTIONS'){
          res.writeHead(200);
          res.end();
    }else if(req.method==='POST'){
      var body = [];
      //h katallhlh kefalida
      res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE'
      });
      //diavase data
      req.on("data", (chunk) => {
        console.log(chunk);
        body.push(chunk);
      });
      //otan exeis diavasei olo to data
      req.on("end", () => {
        var mdata = Buffer.concat(body).toString();
        mdata = JSON.parse(mdata);//parsing json
        mdata = mdata.msg;
        var con = mysql.createConnection({
          host: "localhost",
          user: "root",
          password: "Den8aKsexasw",
          database: "softeng22",
          multipleStatements: true
        });
        con.connect(function(err) {
          console.log("Connected");
          const query = util.promisify(con.query).bind(con);//g9ia na exw promises
          var mquery = "SELECT * FROM user WHERE username like \'%"+mdata.username+"%\' AND email like \'%"+mdata.email+"%\';";
          con.query(mquery, function (err, result, fields) {
            if (err){
              throw err;
            }
            if(result.length > 0){
              message = {info : "User Exists"};
              res.write(JSON.stringify(message));
              res.end();
            }else{
              res.write(JSON.stringify({info : '1'}));
              res.end();
              var mquery = "INSERT INTO user(username,email,password,points) VALUES (\'"+mdata.username+"\' ,\'"+mdata.email+"\',\'"+ mdata.password+"\',30000);";
              query(mquery);
            }
          });//telos query gia info
        });//telos connect

      res.on('error', (err) => {
        console.error(err);
      });
    });//req on end
  }//end if
});
//gia register

function calcRectangle(coords,km)
{
  var i = 0;
  var the_rect = []
  while(i < 360){
    the_rect.push( geolib.computeDestinationPoint({latitude : coords.lat,longitude : coords.lon}, km * 1000,i) );
    i+=90;
  }
  return the_rect;
}

app.listen(8080, function() {
console.log('Node app is running on port 8080');
});
module.exports = app;

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
          database: "mapp",
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
          database: "mapp",
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
              var mquery = "INSERT INTO user(username,email,pssw,points) VALUES (\'"+mdata.username+"\' ,\'"+mdata.email+"\',\'"+ mdata.password+"\',30000);";
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



app.listen(8080, function() {
console.log('Node app is running on port 8080');
});
module.exports = app;

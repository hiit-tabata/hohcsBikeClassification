const request = require('superagent');
const parse = require('csv-parse');
const fs = require('fs');

const SERVER_URL = "http://hohcs.holmantai.net"

const LABELS_CSV = "../labels.csv";
const JSON_FOLDER = "../json/"

//the first param should the server password
const admin_pw = process.argv[2];

//global var
let serverToken = "";
let arr = []

console.log("the password " +admin_pw)

// login as admin

function login(){
  return new Promise((resolve, reject)=>{
    request
      .post(`${SERVER_URL}/api/Users/login`)
      .set('Content-Type', 'application/json')
      .send(JSON.stringify({ email: 'admin@admin.admin', password: admin_pw }) )
      .end((err, res)=>{
        if(err){
          console.error(err);
          reject(err);
        }else{
          console.log(`login at: ${res.body.created}`)
          serverToken = res.body.id;
          resolve(res.body.id)
        }
      });
  });
}

// assume i got a csv with this format
/*
   recordId, date,.........
*/

let requestData = (id)=>{
  return new Promise((resolve, reject)=>{
    request
      .get(`${SERVER_URL}/api/record?filter=%7B%22where%22%3A%7B%22id%22%3A%22${id}%22%7D%7D&access_token=${serverToken}`)
      .set('Content-Type', 'application/json')
      .end((err, res)=>{
        if(err){
          reject(err);
        }else{
          resolve(res.body);
        }
      });
  });
}

//read the csv file, reutrn a promise
let readCsv = (path)=>{
  return new Promise((resolve, reject)=>{
    fs.readFile(path, 'utf8', (err,data)=>{
      if (err) {
        reject(err);
      }
      let csvArr = parse(data, {from: 3}, (err, output)=>{
        if (err) {
          reject(err);
        }
        resolve(output);
      });
    });
  });
}

// download datas into json
let downloadJson = ()=>{
  let temp_arr = arr;

  console.log("start download json");
  // console.log(`user ${row[0]} recordId ${row[1]}`)

  let local_request = (client, recordId)=>{
    console.log(`user ${client} recordId ${recordId}`)

    requestData(recordId)
    .then(res=>{
      let json = JSON.stringify(res[0]);
      //write raw json
      fs.writeFile(
        JSON_FOLDER+`${recordId}.json`,
        json,(err)=>{
          if(err){
            throw err;
          }else{
            console.log("i got res of " + recordId);
            if(temp_arr.length > 0){
              let next = temp_arr.pop();
              local_request(next[0], next[1]);
            }
          }
      });
    })
    .catch(err=>{
      console.error(err);
    })

  }

  let next = temp_arr.pop();
  local_request(next[0], next[1])
}

//main code
readCsv(LABELS_CSV)
.then(arr_=>{
  arr = arr_;
  return login();
})
.then(downloadJson)
.catch(err=>{
  console.error(err);
})

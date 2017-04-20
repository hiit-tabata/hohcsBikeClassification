const request = require('superagent');

const SERVER_URL = "http://hohcs.holmantai.net"

//the first param should the server password
const admin_pw = process.argv[2];
let serverToken = "";

console.log("the password " +admin_pw)

// login as admin
request
  .post(`${SERVER_URL}/api/Users/login`)
  .set('Content-Type', 'application/json')
  .send(JSON.stringify({ email: 'admin@admin.admin', password: admin_pw }) )
  .end((err, res)=>{
    if(err){
      console.error(err);
    }else{
      console.log(`login at: ${res.body.created}`)
      serverToken = res.body.id;
    }
  });

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

requestData("58142861ffba070fe0d65c5d")
.then(res=>{
  console.log(res);
})
.catch(err=>{
  console.error(err);
})

const { Neurosity } = require("@neurosity/sdk");
const dgram = require("dgram");
const TELLO_PORT = 8889;
const TELLO_IP = "192.168.10.1";
const drone = dgram.createSocket("udp4");
drone.bind(TELLO_PORT);

/*
const deviceId = document.getElementById("deviceId");
const email = document.getElementById("username");
const password = document.getElementById("password");
*/
function processLogin(username, password, deviceId) {
  // Validate if the required environment variables are provided
  if (username == ""|| password == "" || deviceId == "") {
    console.error(
      "Please verify deviceId, email, and password are provided, quitting..."
    );
    return false
  }
  else{
    return true;
  }
    
  }
async function main(email, password, neurosity) {
try{
  await neurosity
    .login({
      email: email,
      password: password
    });
    console.log('Logged in successfully');
    return true;
  }
  catch(error){
      console.log(error);
      return false;
  }
};

function sleep() {
    ms = 3000
    return new Promise(resolve => setTimeout(resolve, ms));
}

function sendCommand(command) {
  drone.send(command, TELLO_PORT, TELLO_IP, (err) => {
    if (err) console.error("Error sending command:", err);
    else console.log("Command sent:", command);
  });
}
// rc a b c d
// a: left/right
// b: forward/backward
// c: up/down
// d: yaw
// space: emergency stop



module.exports = {processLogin, main, sleep, sendCommand};

const { Neurosity } = require("@neurosity/sdk");

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
      email,
      password
    });
    console.log('Logged in successfully');
    return true;
  }
  catch(error){
      console.log(error);
      return false;
  }
};

module.exports = {processLogin, main};

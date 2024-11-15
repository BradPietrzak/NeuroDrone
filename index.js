const { Neurosity } = require("@neurosity/sdk");

/*
const deviceId = document.getElementById("deviceId");
const email = document.getElementById("username");
const password = document.getElementById("password");
*/
const verifyEnvs = (email, password, deviceId) => {
  const invalidEnv = (env) => {
    return env === "" || env === 0;
  };

  // Validate if the required environment variables are provided
  if (invalidEnv(email) || invalidEnv(password) || invalidEnv(deviceId)) {
    console.error(
      "Please verify deviceId, email, and password are provided, quitting..."
    );
    document.getElementById("error").innerHTML = "Invalid Login";
    
  }
};

const neurosity = new Neurosity({
    deviceId
});

const main = async () => {
  await neurosity
    .login({
      email,
      password
    })
    .catch((error) => {
      console.log(error);
      throw new Error(error);
    });
  console.log("Logged in");

 
};



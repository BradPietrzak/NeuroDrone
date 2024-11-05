const { Neurosity } = require("@neurosity/sdk");
require("dotenv").config();
const readline = require("readline");

// Environment variables
const deviceId = process.env.DEVICE_ID || "";
const email = process.env.EMAIL || "";
const password = process.env.PASSWORD || "";

// Verify environment variables
const verifyEnvs = (email, password, deviceId) => {
  const invalidEnv = (env) => {
    return env === "" || env === 0;
  };
  if (invalidEnv(email) || invalidEnv(password) || invalidEnv(deviceId)) {
    console.error(
      "Please verify deviceId, email, and password are in .env file, quitting..."
    );
    process.exit(0);
  }
};
verifyEnvs(email, password, deviceId);

console.log(`${email} attempting to authenticate to ${deviceId}`);

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

  displayCurrentThought();
  trainThought();

  // Checks for user input to toggle thoughts
  rl.on("line", (input) => {
    if (input.toLowerCase() === "next") {
      toggleThought();
      trainThought(); // Start training the new thought
    } else if (input.toLowerCase() === "exit") {
      console.log("Exiting...");
      rl.close();
      process.exit(0);
    } else {
      console.log('Type "next" to toggle thoughts or "exit" to quit.');
    }
  });
};


main();

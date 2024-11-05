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

// List of thoughts to train
const thoughts = ["leftHandPinch", "rightHandPinch", "leftArm", "rightArm"];
let currentThoughtIndex = 0;

// Helper function to display current thought
const displayCurrentThought = () => {
  console.log(`Currently training thought: ${thoughts[currentThoughtIndex]}`);
};

// Set up a readline interface for user input
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Function to toggle through thoughts
const toggleThought = () => {
  currentThoughtIndex = (currentThoughtIndex + 1) % thoughts.length;
  displayCurrentThought();
};

// Function to start training the selected thought
const trainThought = () => {
  const thoughtToTrain = thoughts[currentThoughtIndex];
  neurosity.kinesis(thoughtToTrain).subscribe((intent) => {
    if (intent.confidence > 0.8) { 
      console.log(`Detected ${thoughtToTrain}`);
    }
  });
  console.log(`Training on thought: ${thoughtToTrain}`);
};

// Main function to log in and start thought training
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

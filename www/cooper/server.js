const express = require("express");
const http = require("http");
const path = require("path");
const socketIo = require("socket.io");
const opn = require("opn");
const { spawn } = require("child_process");

const app = express();

app.use(express.static(path.join(__dirname + "/public")));

const server = http.createServer(app);

const io = socketIo(server);
io.on("connection", (socket) => {
  console.log("Client connected");

  // Handle drone commands
  socket.on("command", (command) => {
    sendCommand(command);
  });

  socket.on("start-video", () => {
    console.log("Starting video stream...");
    sendCommand("streamon");

    const ffplay = spawn("ffplay", ["-i", "udp://0.0.0.0:11111"], {
      stdio: "inherit",
    });

    ffplay.on("error", (error) => {
      console.error(`Error starting video stream: ${error.message}`);
    });

    ffplay.on("exit", (code, signal) => {
      if (code !== null) {
        console.log(`ffplay exited with code ${code}`);
      } else {
        console.log(`ffplay was killed with signal ${signal}`);
      }
    });
  });

  socket.on("disconnect", () => {
    console.log("Client disconnected");
  });
});

const PORT = 80;
const ADDR = "localhost";

server.listen(PORT, ADDR, () => {
  opn(`http://${ADDR}:${PORT}`);
});

const dgram = require("dgram");
const { send } = require("process");
const COMMAND_PORT = 8889;
const TELLO_IP = "192.168.10.1";
const drone = dgram.createSocket("udp4");
drone.bind(COMMAND_PORT);

function sendCommand(command) {
  drone.send(command, COMMAND_PORT, TELLO_IP, (err) => {
    if (err) console.error("Error sending command:", err);
    else console.log("Command sent:", command);
  });
}

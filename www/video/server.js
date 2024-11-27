const express = require("express");
const dgram = require("dgram");
const { spawn } = require("child_process");
const WebSocket = require("ws");

const app = express();
const TELLO_IP = "192.168.10.1";
const COMMAND_PORT = 8889;
const VIDEO_PORT = 11111;

const commandSocket = dgram.createSocket("udp4");
const videoSocket = dgram.createSocket("udp4");

app.use(express.static("public"));

app.get("/control", async (req, res) => {
  const { command } = req.query;
  try {
    commandSocket.send(command, COMMAND_PORT, TELLO_IP, (err) => {
      if (err) {
        res.status(500).send("Error sending command");
      } else {
        console.log(`Command sent: ${command}`);
        res.send("Command sent successfully");
      }
    });
  } catch (error) {
    res.status(500).send("Error");
  }
});

const server = app.listen(3000, () => {
  console.log("Server is running on http://localhost:3000");
});

async function initializeDrone() {
  commandSocket.send("command", COMMAND_PORT, TELLO_IP, () => {
    console.log("Initialized Tello in SDK mode.");
  });

  commandSocket.send("streamon", COMMAND_PORT, TELLO_IP, (err) => {
    if (err) {
      console.error("Failed to start video stream");
    } else {
      console.log("Video stream started");
    }
  });

  videoSocket.bind(VIDEO_PORT);
}

initializeDrone();

// Create a WebSocket server for video streaming
const wss = new WebSocket.Server({ noServer: true });

wss.on("connection", (ws) => {
  console.log("Client connected to video stream");

  ffmpegProcess.stdout.on("data", (chunk) => {
    ws.send(chunk); // Send FFmpeg video stream to WebSocket client
  });
});

// Handle HTTP upgrade for WebSocket
server.on("upgrade", (request, socket, head) => {
    if (request.url === "/video-stream") {
      wss.handleUpgrade(request, socket, head, (ws) => {
        wss.emit("connection", ws, request);
      });
    }
  });

const ffmpegProcess = spawn("ffmpeg", [
  "-i",
  "udp://0.0.0.0:11111", // Update with local IP if needed
  "-f",
  "mpegts",
  "-codec:v",
  "mpeg1video",
  "-s",
  "640x480", // Resolution
  "-b:v",
  "800k", // Bitrate
  "-r",
  "30", // Frame rate
  "pipe:1", // Output to WebSocket
]);

// Log FFmpeg stderr for better error tracking
ffmpegProcess.stderr.on("data", (data) => {
  console.error(`FFmpeg Error: ${data.toString()}`);
});



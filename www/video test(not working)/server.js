const express = require("express");
const { spawn } = require("child_process");
const FfmpegCommand = require("fluent-ffmpeg");
const StreamCache = require("stream-cache");
const app = express();
const http = require("http");
const path = require("path");

app.use(express.static(path.join(__dirname + "/public")));

const server = http.createServer(app);
const port = 3000;

app.get("/video-stream", (req, res) => {
  res.setHeader("Content-Type", "video/mp4");

  const cacheStream = new StreamCache();
  const ffmpegProcess = new FfmpegCommand()
    .input("udp://192.168.10.1:11111")
    .inputFormat("h264")
    .format("mp4")
    .videoCodec("libx264")
    .outputOptions([
      "-movflags frag_keyframe+empty_moov",
      "-buffer_size 999k",
      "-crf 23"
    ])
    .on("end", () => {
      console.log("Stream ended");
    })
    .on("error", (err, stdout, stderr) => {
      console.error("FFmpeg error:", err);
      console.error("FFmpeg stdout:", stdout);
      console.error("FFmpeg stderr:", stderr);
    })
    .pipe(cacheStream);

  cacheStream.pipe(res);
});

server.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

// Command to initialize the drone
const TELLO_IP = "192.168.10.1";
const COMMAND_PORT = 8889;
const dgram = require("dgram");
const commandSocket = dgram.createSocket("udp4");

function initializeDrone() {
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
}

initializeDrone();

const FfmpegCommand = require("fluent-ffmpeg");

const ffmpegProcess = new FfmpegCommand()
  .input("udp://192.168.10.1:11111")
  .inputFormat("h264")
  .format("mp4")
  .videoCodec("libx264")
  .outputOptions([
    "-movflags frag_keyframe+empty_moov",
    "-fflags nobuffer",
    "-flags low_delay",
    "-max_delay 0",
    "-tune zerolatency",
    "-buffer_size 2M",
    "-analyzeduration 100M",
    "-crf 23", "-preset ultrafast"
  ])
  .on("end", () => {
    console.log("Stream ended");
  })
  .on("error", (err, stdout, stderr) => {
    console.error("FFmpeg error:", err);
    console.error("FFmpeg stdout:", stdout);
    console.error("FFmpeg stderr:", stderr);
  })
  .save("output.mp4");

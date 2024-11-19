const express = require("express");
const http = require("http");
const path = require("path");
const app = express();
const server = http.createServer(app);
const port = 3000;


app.use(express.static(path.join(__dirname + '/headset')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '/headset/login.html')); // Serve login.html
});

const loginRouter = require('./routes/login')


app.use('/login', loginRouter);



server.listen(port, () => {
    console.log(`Listening on port ${port}`);
});

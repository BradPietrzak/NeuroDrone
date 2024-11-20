//establish server connection
const express = require("express");
const http = require("http");
const path = require("path");
const app = express();
const server = http.createServer(app);
const port = 3000;

//specify path dependencies
app.use(express.urlencoded({ extended: true })); 
app.use(express.json());
app.use(express.static(path.join(__dirname + '/headset')));


// Serve login.html at root level
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '/headset/login.html')); 
});

//establish routes specify login route
const loginRouter = require('./routes/login')


app.use('/login', loginRouter);



server.listen(port, () => {
    console.log(`Listening on port ${port}`);
});

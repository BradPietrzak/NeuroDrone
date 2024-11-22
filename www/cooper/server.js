const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();

app.use(express.static('./'));

const server = http.createServer(app);

const io = socketIo(server);
io.on('connection', (socket) => {
    console.log('Client connected');

    socket.on('command', (command) => {
        sendCommand(command);
    });

    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

// 25-28 checks if it is running in a dockerfile or not
const isDocker = process.env.DOCKER === 'true';

const PORT = 80;
const ADDR = isDocker ? '0.0.0.0' : 'localhost'; 

server.listen(PORT, ADDR, () => {
    console.log(`Server listening on http://${ADDR}:${PORT}`);
});

const dgram = require('dgram');
const TELLO_PORT = 8889;
const TELLO_IP = '192.168.10.1';
const drone = dgram.createSocket('udp4');
drone.bind(TELLO_PORT);

function sendCommand(command) {
    drone.send(command, TELLO_PORT, TELLO_IP, (err) => {
        if (err) console.error('Error sending command:', err);
        else console.log('Command sent:', command);
    });
}

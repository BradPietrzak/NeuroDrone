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

const PORT = 80;
const ADDR = 'localhost';

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
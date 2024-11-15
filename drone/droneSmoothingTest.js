const dgram = require('dgram');
const client = dgram.createSocket('udp4');

// Tello's default IP and command port
const TELLO_IP = '192.168.10.1';
const TELLO_PORT = 8889;

// Send a command to the Tello drone
function sendCommand(command) {
    const message = Buffer.from(command);
    client.send(message, 0, message.length, TELLO_PORT, TELLO_IP, (err) => {
        if (err) console.error(err);
        else console.log(`Command sent: ${command}`);
    });
}

// Listen for responses from the Tello drone
client.on('message', (msg, rinfo) => {
    console.log(`Drone Response: ${msg.toString()}`);
});

// Handle connection errors
client.on('error', (err) => {
    console.error(`Error: ${err}`);
    client.close();
});

sendCommand('command');
setTimeout(() => {
  sendCommand('takeoff');
}, 1000);
setTimeout(() => {
  sendCommand('rc 0 100 0 0')
}, 1000);
sendCommand('speed?')
sendCommand('sdk?')
setTimeout(() => {
  sendCommand('stop')
}, 1000);
setTimeout(() => {
  sendCommand('land')
}, 3000);

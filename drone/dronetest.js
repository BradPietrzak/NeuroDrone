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

// Start by sending the "command" to enter SDK mode
sendCommand('command');

// For example, to take off the drone, send "takeoff" command after entering SDK mode
setTimeout(() => {
    sendCommand('takeoff');
}, 3000);

// After another delay, you can land the drone
setTimeout(() => {
    sendCommand('land');
}, 15000);
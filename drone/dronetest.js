const dgram = require('dgram');
const client = dgram.createSocket('udp4');

const TELLO_IP = '192.168.10.1';
const TELLO_PORT = 8889;

function sendCommand(command) {
    const message = Buffer.from(command);
    client.send(message, 0, message.length, TELLO_PORT, TELLO_IP, (err) => {
        if (err) console.error(err);
        else console.log(`Command sent: ${command}`);
    });
}

client.on('message', (msg, rinfo) => {
    console.log(`Drone Response: ${msg.toString()}`);
});

client.on('error', (err) => {
    console.error(`Error: ${err}`);
    client.close();
});

sendCommand('command');
sendCommand('battery?');
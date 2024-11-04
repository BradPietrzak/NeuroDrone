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

// wait 3 seconds then say "accepting inputs from keyboard"
setTimeout(() => {
    console.log('accepting inputs from keyboard');
}, 3000);

// now we can accept inputs from the keyboard
// wasd for cardinal directions, q and e for up and down and space for takeoff and land
const readline = require('readline');
readline.emitKeypressEvents(process.stdin);
process.stdin.setRawMode(true);

process.stdin.on('keypress', (str, key) => {
    if (key.ctrl && key.name === 'c') {
        process.exit();
    } else {
        switch (key.name) {
            case 'w':
                sendCommand('forward 20');
                break;
            case 's':
                sendCommand('back 20');
                break;
            case 'a':
                sendCommand('left 20');
                break;
            case 'd':
                sendCommand('right 20');
                break;
            case 'q':
                sendCommand('up 20');
                break;
            case 'e':
                sendCommand('down 20');
                break;
            case 'space':
                sendCommand('takeoff');
                break;
            case 'l':
                sendCommand('land');
                break;
            default:
                console.log('Invalid command');
        }
    }
});
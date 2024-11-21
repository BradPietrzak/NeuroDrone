const socket = io();

function sendCommand(command) {
    socket.emit('command', command);
    console.log(`Sent command: ${command}`);
}

function connect() {
    sendCommand('command')
}

// rc a b c d
// a: left/right
// b: forward/backward
// c: up/down
// d: yaw
// space: emergeny stop
// p: stats
document.addEventListener('keydown', (event) => {
    switch (event.key) {
        case 'w':
            sendCommand('rc 0 50 0 0');
            break;
        case 's':
            sendCommand('rc 0 -50 0 0');
            break;
        case 'a':
            sendCommand('rc -50 0 0 0');
            break;
        case 'd':
            sendCommand('rc 50 0 0 0');
            break;
        case 'ArrowUp':
            sendCommand('rc 0 0 50 0');
            break;
        case 'ArrowDown':
            sendCommand('rc 0 0 -50 0');
            break;
        case 'q':
            sendCommand('rc 0 0 0 -50');
            break;
        case 'e':
            sendCommand('rc 0 0 0 50');
            break;
        case 't':
            sendCommand('takeoff');
            break;
        case 'l':
            sendCommand('land');
            break;
        case ' ':
            sendCommand('emergency');
            break;
    }
});

document.addEventListener('keyup', (event) => {
    switch (event.key) {
        case 'w':
            sendCommand('stop');
            break;
        case 's':
            sendCommand('stop');
            break;
        case 'a':
            sendCommand('stop');
            break;
        case 'd':
            sendCommand('stop');
            break;
        case 'ArrowUp':
            sendCommand('stop');
            break;
        case 'ArrowDown':
            sendCommand('stop');
            break;
        case 'q':
            sendCommand('stop');
            break;
        case 'e':
            sendCommand('stop');
            break;
    }
});

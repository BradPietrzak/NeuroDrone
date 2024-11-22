const socket = io();

function sendCommand(command) {
    socket.emit('command', command);
    console.log(`Sent command: ${command}`);
}

function connect() {
    sendCommand('command')
}
function sleep() {
    return new Promise(resolve => setTimeout(resolve, ms));
}
// rc a b c d
// a: left/right
// b: forward/backward
// c: up/down
// d: yaw
// space: emergency stop
document.addEventListener('keydown', (event) => {
    switch (event.key) {
        case 'w':
            sendCommand('rc 0 100 0 0');
            break;
        case 's':
            sendCommand('rc 0 -100 0 0');
            break;
        case 'a':
            sendCommand('rc -100 0 0 0');
            break;
        case 'd':
            sendCommand('rc 100 0 0 0');
            break;
        case 'ArrowUp':
            sendCommand('rc 0 0 100 0');
            break;
        case 'ArrowDown':
            sendCommand('rc 0 0 -100 0');
            break;
        case 'q':
            sendCommand('rc 0 0 0 -100');
            break;
        case 'e':
            sendCommand('rc 0 0 0 100');
            break;
        case 't':
            sendCommand('takeoff');
            break;
        case 'l':
            sendCommand('land');
            break;
        case '`':
            sendCommand('emergency');
            break;
        case 'ArrowLeft':
            sendCommand('flip l');
            break;
        case 'ArrowRight':
            sendCommand('flip r');
            break;
        case 'f':
            sendCommand('flip f');
            break;
        case 'b':
            sendCommand('flip b');
            break;
    }
});

document.addEventListener('keyup', (event) => {
    switch (event.key) {
        case 'w':
            sendCommand('rc 0 0 0 0');
            break;
        case 's':
            sendCommand('rc 0 0 0 0');
            break;
        case 'a':
            sendCommand('rc 0 0 0 0');
            break;
        case 'd':
            sendCommand('rc 0 0 0 0');
            break;
        case 'ArrowUp':
            sendCommand('rc 0 0 0 0');
            break;
        case 'ArrowDown':
            sendCommand('rc 0 0 0 0');
            break;
        case 'q':
            sendCommand('rc 0 0 0 0');
            break;
        case 'e':
            sendCommand('rc 0 0 0 0');
            break;
    }
});

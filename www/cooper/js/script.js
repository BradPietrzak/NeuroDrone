const socket = io();

function sendCommand(command) {
    socket.emit('command', command);
    console.log(`Sent command: ${command}`);
}

function connect() {
    sendCommand('command')
}

document.addEventListener('keydown', (event) => {
    switch (event.key) {
        case 'w':
            sendCommand('forward 50');
            break;
        case 's':
            sendCommand('back 50');
            break;
        case 'a':
            sendCommand('left 50');
            break;
        case 'd':
            sendCommand('right 50');
            break;
        case 'ArrowUp':
            sendCommand('up 50');
            break;
        case 'ArrowDown':
            sendCommand('down 50');
            break;
        case 'q':
            sendCommand('ccw 90');
            break;
        case 'e':
            sendCommand('cw 90');
            break;
        case 't':
            sendCommand('takeoff');
            break;
        case 'l':
            sendCommand('land');
            break;
    }
});
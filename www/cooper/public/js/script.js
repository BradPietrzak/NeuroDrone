const socket = io();

function sendCommand(command) {
    socket.emit('command', command);
    console.log(`Sent command: ${command}`);
}

async function connect() {
    const levelDiv = document.getElementById('connect');

    try {
        const diditconnect = await sendCommand('command');
        levelDiv.style.backgroundColor = '#4caf50';  // Green for success
    } catch (error) {
        console.error('Error occurred while connecting:', error);
        levelDiv.style.backgroundColor = '#f44336';  // Red for error
    }
}

function sleep() {
    ms = 3000
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
        case '`':
            sendCommand('emergency');
            break;
        case 'ArrowLeft':
            sendCommand('flip l');
            sleep();
            break;
        case 'ArrowRight':
            sendCommand('flip r');
            sleep();
            break;
        case 'f':
            sendCommand('flip f');
            sleep();
            break;
        case 'b':
            sendCommand('flip b');
            sleep();
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

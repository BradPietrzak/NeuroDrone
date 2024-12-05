import * as MODEL from "/js/3d.js";

const socket = io();

function sendCommand(command) {
    socket.emit('command', command);
    console.log(`Sent command: ${command}`);
}

export async function connect() {
    const levelDiv = document.getElementById('connect');
    
    try {
        const diditconnect = await sendCommand('command');
        sendCommand('streamon');
        socket.emit('start-video');
        levelDiv.style.backgroundColor = '#4caf50';  // Green for success
    } catch (error) {
        console.error('Error occurred while connecting:', error);
        levelDiv.style.backgroundColor = '#f44336';  // Red for error
    }
}

function sleep() {
    let ms = 3000
    return new Promise(resolve => setTimeout(resolve, ms));
}

// rc a b c d
// a: left/right
// b: forward/backward
// c: up/down
// d: yaw
// ~: emergency stop
document.addEventListener('keydown', (event) => {
    switch (event.key) {
        case 'w':
            sendCommand('rc 0 50 0 0');
            MODEL.modelPosition(0, 0, -3, 0);
            break;
        case 's':
            sendCommand('rc 0 -50 0 0');
            MODEL.modelPosition(0, 0, 3, 0);
            break;
        case 'a':
            sendCommand('rc -50 0 0 0');
            MODEL.modelPosition(-3, 0, 0, 0);
            break;
        case 'd':
            sendCommand('rc 50 0 0 0');
            MODEL.modelPosition(3, 0, 0, 0);
            break;
        case 'ArrowUp':
            sendCommand('rc 0 0 50 0');
            MODEL.modelPosition(0, 3, 0, 0);
            break;
        case 'ArrowDown':
            sendCommand('rc 0 0 -50 0');
            MODEL.modelPosition(0, -3, 0, 0);
            break;
        case 'q':
            sendCommand('rc 0 0 0 -50');
            MODEL.modelPosition(0, 0, 0, 0.5);
            break;
        case 'e':
            sendCommand('rc 0 0 0 50');
            MODEL.modelPosition(0, 0, 0, -0.5);
            break;
        case 't':
            sendCommand('takeoff');
            MODEL.takeoff();
            break;
        case 'l':
            sendCommand('land');
            MODEL.land(false);
            break;
        case '`':
            sendCommand('emergency');
            MODEL.land(true);
            break;
        case 'c':
            sendCommand('command');
            break;
        case 'ArrowLeft':
            sendCommand('flip l');
            MODEL.flipL();
            sleep();
            break;
        case 'ArrowRight':
            sendCommand('flip r');
            MODEL.flipR();
            sleep();
            break;
        case 'f':
            sendCommand('flip f');
            MODEL.flipF();
            sleep();
            break;
        case 'b':
            sendCommand('flip b');
            MODEL.flipB();
            sleep();
            break;
    }
});

document.addEventListener('keyup', (event) => {
    switch (event.key) {
        case 'w':
        case 's':
        case 'a':
        case 'd':
        case 'ArrowUp':
        case 'ArrowDown':
        case 'q':
        case 'e':
            sendCommand('rc 0 0 0 0');
            MODEL.modelPosition(0, 0, 0, 0);
            break;
    }
});

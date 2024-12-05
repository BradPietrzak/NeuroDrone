const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const router = express.Router();
const {sleep, sendCommand} = require('../index');


router.post('/', async (req, res) => {
    const {type, key} = req.body;

    if (type === 'keydown') {
        switch (key) {
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
            default: break;
        }
    } else if (type === 'keyup') {
        switch (key) {
            case 'w':
            case 's':
            case 'a':
            case 'd':
            case 'ArrowUp':
            case 'ArrowDown':
            case 'q':
            case 'e':
                sendCommand('rc 0 0 0 0');
                break;
            default:
                break;
        }
    }

    res.status(200).send();
});



module.exports = router;

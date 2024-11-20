//router for logins
const { Neurosity } = require('@neurosity/sdk');
const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const router = express.Router();
const { processLogin, main } = require('../index');




router.post("/", async(req,res) => {
   
    console.log("test")
   // res.sendFile(path.join(__dirname,'../headset/controls.html'));
   try{
    const {username,password,deviceID} = req.body;

    if (!processLogin(username,password,deviceID)){
        console.log('Login Error')
        return res.status(400).send("Invalid Login");
    }

    const neurosity = new Neurosity({
        deviceID
    })

    const loggedIn= await main(username, password, neurosity);
    if(loggedIn){
        res.sendFile(path.join(__dirname, '../headset/controls.html'));
    }
    else{
        console.log("Login Failed");
        res.status(401).send('Failed to login');
    }
   }
   catch(error){
    console.log(error);
    res.status(500).send('error occured');
   }


});

module.exports = router;
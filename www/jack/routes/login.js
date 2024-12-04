const { Neurosity } = require('@neurosity/sdk');
const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const router = express.Router();
const { processLogin, main} = require('../index');




router.post("/", async(req,res) => {
   
    console.log("test")
   // res.sendFile(path.join(__dirname,'../headset/controls.html'));
   try{
    const {username,password,deviceID} = req.body;

    if (!processLogin(username,password,deviceID)){
        console.log('Login Error')
        return res.redirect('/login-error');
    }

    const neurosity = new Neurosity({
        deviceId:deviceID,
        timesync: true
    })

    const loggedIn= await main(username, password, neurosity);
    if(loggedIn){

        res.sendFile(path.join(__dirname, '../headset/controls.html'));
    }
    else{
        console.log("Login Failed");
        return res.redirect('/login-error');

    }
   }
   catch(error){
    console.log(error);
    return res.redirect('/login-error');
   }
});
router.get("/login-error", (req, res) => { 
    res.sendFile(path.join(__dirname, '../headset/error.html'));
});


module.exports = router;
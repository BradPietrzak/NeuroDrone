//router for logins
const express = require('express');
const path = require('path');
const router = express.Router();


router.get("/", (req,res)=> {
    res.sendFile(path.join(__dirname,'../headset/controls.html'));
})
router.get("/new", (req,res)=> {
    res.send("New Login");
})


module.exports = router


const { Neurosity } = require("@neurosity/sdk");
require("dotenv").config();

const deviceId=process.env.DEVICE_ID||"";
const email = process.env.EMAIL ||"";
const password = process.env.PASSWD ||"";

const verifyEnvs = (email, password,deviceId) => {
    const invalidEnv=(env) => {
        return env === "" || env === 0;
    };
    if(invalidEnv(email) || invalidEnv(password) || invalidEnv(deviceId)){
        console.error( "Please verify deviceId, email and password are in .env file, quitting..."
        );
        process.exit(0);
    }
};
verifyEnvs(email,password,deviceId);
console.log('${email} attempting to authenticate to ${deviceId}');

const neurosity = new Neurosity({
    deviceId
});
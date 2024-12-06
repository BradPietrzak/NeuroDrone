const THREE = require('three'); 
const { GLTFLoader } = require('three/addons/loaders/GLTFLoader.js')


const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera();
camera.position.x = -23;
camera.position.y = 7;

const renderer = new THREE.WebGLRenderer({alpha: true});
renderer.setSize(300, 300);
document.getElementById('controls').append(renderer.domElement);

const light = new THREE.AmbientLight(0xFFFFFF);
scene.add(light);

let model;
let targetPos = new THREE.Vector3(0, -5, 0);
let targetRot = new THREE.Euler(0, 0, 0);

let mixer;

let inMotion = false;
let targetSpeed = 0, currSpeed = 0;

let propellers;

const loader = new GLTFLoader();
loader.load('models/drone_WIP.glb', function (gltf) {
    model = gltf.scene;
    scene.add(model);
    camera.lookAt(model.position);
    model.position.y = -5;

    mixer = new THREE.AnimationMixer(model);

    // Initialize propellor animations
    gltf.animations.forEach((clip) => {
        mixer.clipAction(clip).play();
    });
    
    animate();
});

let flipType = null;
let startTime = null;
let time = null;
let flipDur = 0.5;

let flipPosAdj = 2;

function animate() {
    //Handle Flipping
    if (startTime != null) {
        time = performance.now();
        const elapsed = (time - startTime) / 1000;
        const flipRotation = (Math.PI * 2) - (Math.PI * 2 * (elapsed / flipDur)); // Complete a 360-degree flip
        const posAdj = Math.sin(Math.PI * elapsed / flipDur) * flipPosAdj;
        switch(flipType) {
            case 'f':
                model.rotation.z = flipRotation;
                model.position.y = 2 * posAdj;
                break;
            case 'b':
                model.rotation.z = -flipRotation;
                model.position.y = 2 * posAdj;
                break;
            case 'l':
                model.rotation.x = flipRotation;
                model.position.z = -posAdj;
                break;
            case 'r':
                model.rotation.x = -flipRotation;
                model.position.z = posAdj;
                break;
            default:
                break;
        }
        if (elapsed >= flipDur)
            startTime = null;
    }
    else {
        // Smooth Movement
        model.position.lerp(targetPos, 0.1);
        model.rotation.x = THREE.MathUtils.lerp(model.rotation.x, targetRot.x, 0.1);
        model.rotation.y = THREE.MathUtils.lerp(model.rotation.y, targetRot.y, 0.1);
        model.rotation.z = THREE.MathUtils.lerp(model.rotation.z, targetRot.z, 0.1);
    }

    // Adjust Propeller Speed
    if (targetSpeed == 0 && currSpeed - targetSpeed < 0.001) currSpeed = targetSpeed;
    else if (currSpeed > targetSpeed) currSpeed -= 0.001;
    else if (currSpeed < targetSpeed) currSpeed += 0.001;
    
    if (mixer) {
        mixer.update(currSpeed);
    }

    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

function takeoff() {
    inMotion = true;
    targetSpeed = 0.05;
    modelPosition(0, 0, 0, 0);
}
function land(emergency) {
    targetSpeed = 0;
    if (emergency) currSpeed = 0;
    modelPosition(0, -5, 0, 0);
    inMotion = false;
}

function flipF() {
    if (startTime === null && inMotion) {
        startTime = performance.now();
        flipType = 'f';
    }
}
function flipB() {
    if (startTime === null && inMotion)  {
        startTime = performance.now();
        flipType = 'b';
    }
}
function flipL() {
    if (startTime === null && inMotion)  {
        startTime = performance.now();
        flipType = 'l';
    }
}
function flipR() {
    if (startTime === null && inMotion)  {
        startTime = performance.now();
        flipType = 'r';
    }
}

 function modelPosition(z, y, x, yaw) {
    if (!inMotion) return;
    x *= -1;
    // X rotation with backward/forward
    if (z > 0) targetRot.x = 0.3;
    else if (z < 0) targetRot.x = -0.3;
    else targetRot.x = 0;
    
    // Z rotation with left/right
    if (x > 0) targetRot.z = -0.3;
    else if (x < 0) targetRot.z = 0.3;
    else targetRot.z = 0;

    targetPos.x = x;
    targetPos.y = y;
    targetPos.z = z;
    targetRot.y = yaw;
}

module.exports = {takeoff,land,flipF,flipB,flipL,flipR,modelPosition};
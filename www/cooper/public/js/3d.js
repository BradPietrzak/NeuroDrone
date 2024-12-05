import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera();
camera.position.x = -20;
camera.position.y = 7;

const renderer = new THREE.WebGLRenderer({alpha: true});
renderer.setSize(300, 300);
document.body.prepend(renderer.domElement);

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

    gltf.animations.forEach((clip) => {
        mixer.clipAction(clip).play();  // Play each animation (or choose a specific one)
    });

    propellers = [
        model.getObjectByName("Object_10"), // 0, 0
        model.getObjectByName("Object_6"),  // 0, 1
        model.getObjectByName("Object_14"), // 1, 0
        model.getObjectByName("Object_18")  // 1, 1
    ];

    for (let i = 0; i < 4; i++) {
        console.log(propellers[i]);
    }
    // Get propellers into proper rotations
    
    animate();
});



function animate() {
    requestAnimationFrame(animate);

    // Smooth Movement
    model.position.lerp(targetPos, 0.1);
    model.rotation.x = THREE.MathUtils.lerp(model.rotation.x, targetRot.x, 0.1);
    model.rotation.y = THREE.MathUtils.lerp(model.rotation.y, targetRot.y, 0.1);
    model.rotation.z = THREE.MathUtils.lerp(model.rotation.z, targetRot.z, 0.1);

    // Adjust Propeller Speed
    if (targetSpeed == 0 && currSpeed - targetSpeed < 0.001) currSpeed = targetSpeed;
    else if (currSpeed > targetSpeed) currSpeed -= 0.001;
    else if (currSpeed < targetSpeed) currSpeed += 0.001;
    
    if (mixer) {
        mixer.update(currSpeed);  // Update by the time step (0.01 for smooth playback)
    }
    // Rotate Propellers
    //propellers[0].rotation.y += currSpeed; // Working
    //propellers[1].rotation.x += currSpeed;
    //propellers[2].rotation.y += currSpeed;
    //propellers[2].rotation.y += currSpeed;
    //propellers[3].rotation.y += currSpeed; // Working

    renderer.render(scene, camera);
}

export function takeoff() {
    inMotion = true;
    targetSpeed = 0.05;
    modelPosition(0, 0, 0, 0);
}
export function land(emergency) {
    targetSpeed = 0;
    if (emergency) currSpeed = 0;
    modelPosition(0, -5, 0, 0);
    inMotion = false;
}


export function modelPosition(z, y, x, yaw) {
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
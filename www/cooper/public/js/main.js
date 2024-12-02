import * as THREE from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera();

// Adjust to face drone properly
camera.position.x = -20;
camera.rotation.y = -Math.PI / 2;
const rotZ = 0.5;

const renderer = new THREE.WebGLRenderer({alpha: true});
renderer.setSize(300, 300);
document.body.prepend(renderer.domElement);

const light = new THREE.AmbientLight(0xFFFFFF);
scene.add(light);

let mesh;


const loader = new GLTFLoader();
loader.load('models/dji_tello.glb', function (gltf) {
    mesh = gltf.scene;
    mesh.rotation.z = rotZ;
    scene.add(mesh);
    animate();
});

function animate() {
    requestAnimationFrame(animate);

    renderer.render(scene, camera);
}


export function modelPosition(z, y, x, yaw) {

    x *= -1;
    // X rotation with backward/forward
    if (z > 0) mesh.rotation.x = 0.3;
    else if (z < 0) mesh.rotation.x = -0.3;
    else mesh.rotation.x = 0;
    
    // Z rotation with left/right
    if (x > 0) mesh.rotation.z = -0.3 + rotZ;
    else if (x < 0) mesh.rotation.z = 0.3 + rotZ;
    else mesh.rotation.z = rotZ;

    mesh.position.x = x;
    mesh.position.y = y;
    mesh.position.z = z;
    mesh.rotation.y = yaw;
}
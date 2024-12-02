import * as THREE from "three";
import { STLLoader } from "three/addons/loaders/STLLoader.js";

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera();
camera.position.z = 5;

const renderer = new THREE.WebGLRenderer({alpha: true});
renderer.setSize(300, 300);
document.body.prepend(renderer.domElement);

const light = new THREE.AmbientLight(0xFFFFFF);
scene.add(light);

const loader = new STLLoader();
let mesh;
let center;
loader.load('models/tello_v2.stl', function (geometry) {
    const material = new THREE.MeshPhongMaterial({ color: 0x666666 });
    mesh = new THREE.Mesh(geometry, material);
    mesh.scale.x = 0.1;
    mesh.scale.y = 0.1;
    mesh.scale.z = 0.1;
    mesh.position.z = -15;
    mesh.rotation.x = 35;
    center = mesh.position;
    scene.add(mesh);
    function animate() {
        requestAnimationFrame(animate);

        renderer.render(scene, camera);
    }

    animate();
});

export function modelCenter() {
    mesh.position.x = center.x;
    mesh.position.y = center.y;
    mesh.position.z = center.z;
}
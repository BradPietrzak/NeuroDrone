import * as THREE from "three";
import { STLLoader } from "three/addons/loaders/STLLoader.js";

// 1. Set up the scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 2. Create a light source
const light = new THREE.AmbientLight(0xFFFFFF);  // Ambient light
scene.add(light);

// 3. Set up the loader
const loader = new STLLoader();

// 4. Load the STL model
loader.load('three_tests/tello_v2.stl', function (geometry) {
    const material = new THREE.MeshPhongMaterial({ color: 0xFFFFFF }); // Change color as needed
    const mesh = new THREE.Mesh(geometry, material);
    mesh.scale.x = 0.1;
    mesh.scale.y = 0.1;
    mesh.scale.z = 0.1;

    mesh.position.z = -10;
    mesh.rotation.x = 35;
    scene.add(mesh);

    // Center the model
    geometry.computeBoundingBox();
    const center = new THREE.Vector3();
    geometry.boundingBox.getCenter(center);
    mesh.position.sub(center);

    // Position the camera to view the model
    camera.position.z = 5;

    // 5. Animation loop to render the scene
    function animate() {
        requestAnimationFrame(animate);

        // Rotate the model for animation
        mesh.rotation.y += 0.01;

        renderer.render(scene, camera);
    }

    animate();
});

// 6. Handle window resizing
window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});
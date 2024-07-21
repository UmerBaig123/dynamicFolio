
const getSpere = (size, color) => {
    const geometry = new THREE.SphereGeometry(size, 32, 32);
const texture = new THREE.TextureLoader().load("/static/photos/asphalt.png");
texture.wrapS = THREE.RepeatWrapping;
texture.wrapT = THREE.RepeatWrapping;
const material = new THREE.MeshStandardMaterial( { 
    roughness:1,
    metalness:0,
    color:color,
    // emissive:0x000000,
    // map: new THREE.TextureLoader().load(),
    map: texture,
    // mapColor: 0xfff,
    bumpScale: 0.001,
 } );

    return new THREE.Mesh(geometry, material);
}
const getDirectionalLight = (color,intensity) => {
    var light = new THREE.DirectionalLight(color, intensity);
    // light.castShadow = true;
    return light;
}
const scene = new THREE.Scene();

const sphere = getSpere(7, 0x4AF626);
sphere.position.set(6,1,0);
scene.add(sphere);
// var light = getDirectionalLight(0xffffff,1);
// light.position.set(0, 10, 10);
// scene.add(light);

const camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 );
camera.position.z = 10;
// camera.lookAt(-1,-7,0);
const amblight = new THREE.AmbientLight( 0xffffff,0.5 ); // soft white light
scene.add( amblight );
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setClearColor( 0x000000, 0 );
renderer.setPixelRatio( window.devicePixelRatio*0.2)
renderer.setSize( window.innerWidth*0.7, window.innerHeight*0.7);
const controls = new OrbitControls( camera, renderer.domElement );
document.getElementById("root").appendChild( renderer.domElement );
renderer.setAnimationLoop( animate );
var light2 = getDirectionalLight(0xffffff,0.5);
light2.position.set(0,0,5);
// light1.target = sphere;
light2.target = sphere;
scene.add(light2);
controls.update();
function animate() {
    var pixelRatio = renderer.getPixelRatio();
    if(pixelRatio < window.devicePixelRatio){
        renderer.setPixelRatio(pixelRatio+0.01)
    }
	// sphere.rotation.x += 0.01;
    controls.update();
    // light2.position.set(camera.position.x,camera.position.y, camera.position.z);
	sphere.rotation.z+= 0.01;
	renderer.render( scene, camera );
}
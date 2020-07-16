var Sphere = function(_renderer, _audio) {

	this.is_init = false;

	this.renderer = _renderer;
	this.audio = _audio;

	this.width = _renderer.width;
	this.height = _renderer.height;

	this.now = Date.now();
	this.duration = 10000; 

	this.init_scene();
}

Sphere.prototype.init_scene = function() {

	this.scene = new THREE.Scene();

	// lights
	this.directional_light = new THREE.DirectionalLight(0xffffff, 2);
	this.directional_light.position.set(.5, 0, 1);

	this.ambient_light = new THREE.AmbientLight(0);

	// geometry and material
	this.geom = new THREE.SphereBufferGeometry(2, 20, 20);
	this.material = new THREE.MeshLambertMaterial();
	this.sphere = new THREE.Mesh(this.geom, this.material);

	// scene
	this.scene.add(this.directional_light);
	this.scene.add(this.ambient_light);
	this.scene.add(this.sphere);

}

Sphere.prototype.update = function() {

	let _bass = this.audio.get_bass();
	let _mid = this.audio.get_mid();
	let _high = this.audio.get_high();

	console.log(_bass, _mid, _high);

	// map _bass, _mid, _high to _r, _g, _b: [0, 1] -> [0, 255]
	let _r = _bass * 255.0;
	let _g = _mid * 255.0;
	let _b = _high * 255.0;

	console.log(_r, _g, _b);

	this.material.color.setRGB(_r, _g, _b);
	// this.material.specular.setRGB(_r, _g, _b); // only for the phong material

	// render
	this.renderer.renderer.render(this.scene, this.renderer.get_camera());

	// animate
	this.animate();
}

Sphere.prototype.animate = function() {

	let _now = Date.now();
	let _delta = _now - this.now;

	// update the current time
	this.now = Date.now();

	var fract = _delta / this.duration;
	var angle = Math.PI * 2 * fract;

	this.sphere.rotation.y += angle;

}

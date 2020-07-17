var Mesh = function(_renderer, _audio) {

	this.is_init = false;

	this.renderer = _renderer;
	this.audio = _audio;

	this.width = _renderer.width;
	this.height = _renderer.height;

	this.now = Date.now();
	this.duration = 10000; 

	this.init_scene();
}

Mesh.prototype.init_scene = function() {

	this.scene = new THREE.Scene();

	// lights
	// directional light
	this.directional_light = new THREE.DirectionalLight(0xffffff, 2);
	this.directional_light.position.set(.5, 0, 1);

	// ambient light
	this.ambient_light = new THREE.AmbientLight(0);

	// geometry and material
	this.geom = new THREE.PlaneBufferGeometry(1, 1);
	this.material = load(bin_vert, bin_frag);
	this.mesh = new THREE.Mesh(this.geom, this.material);

	// scene
	this.scene.add(this.directional_light);
	this.scene.add(this.ambient_light);
	this.scene.add(this.mesh);

	function load(_vert, _frag){

		return new THREE.ShaderMaterial({
			uniforms: {
				u_red: {value: 0.0},
				u_green: {value: 0.0},
				u_blue: {value: 0.0}
			},
			vertexShader: _vert,
			fragmentShader: _frag
		});
	};

}

Mesh.prototype.update = function() {

	let _bass = this.audio.get_bass();
	let _mid = this.audio.get_mid();
	let _high = this.audio.get_high();

	console.log(_bass, _mid, _high);

	// shader material --> uniforms variables
	this.material.uniforms.u_red.value = _bass;
	this.material.uniforms.u_green.value = _mid;
	this.material.uniforms.u_blue.value = _high;

	// render
	this.renderer.renderer.render(this.scene, this.renderer.get_camera());

	// animate
	this.animate();
}

Mesh.prototype.animate = function() {

	let _now = Date.now();
	let _delta = _now - this.now;

	// update the current time
	this.now = Date.now();

	var fract = _delta / this.duration;
	var angle = Math.PI * 2 * fract;

	this.mesh.rotation.y += angle;

}

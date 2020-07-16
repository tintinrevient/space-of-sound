var ThreeRenderer = function(_target) {

	this.width = document.documentElement.clientWidth;
	this.height = document.documentElement.clientHeight;

	this.matrix = new THREE.PerspectiveCamera(45, this.width / this.height, 0.1, 100.);
	this.matrix.position.z = 5.;
	this.matrix.aspect = this.width / this.height;
	this.matrix.updateProjectionMatrix();

	this.init_renderer();
	this.append_renderer_to_dom(_target);

	window.addEventListener('resize', this.resize.bind(this), false);
}

ThreeRenderer.prototype.init_renderer = function() {

	this.renderer = new THREE.WebGLRenderer();

	this.renderer.setPixelRatio(window.devicePixelRatio);
	this.renderer.setSize(this.width, this.height);

	this.renderer.autoClear = true;
	this.renderer.shadowMap.enabled = true;
	this.renderer.shadowMap.type = THREE.PCFShadowMap;

	console.log("renderer is set with", this.width, "by", this.height);

}

ThreeRenderer.prototype.resize = function() {

	this.width = document.documentElement.clientWidth;
	this.height = document.documentElement.clientHeight;

	this.matrix.aspect = this.width / this.height;
	this.matrix.updateProjectionMatrix();

	this.renderer.setPixelRatio(window.devicePixelRatio);
	this.renderer.setSize(this.width, this.height);

	console.log("camera and renderer is resized with", this.width, "by", this.height);

}

ThreeRenderer.prototype.append_renderer_to_dom = function(_target) {

	_target.appendChild(this.renderer.domElement);

	console.log("renderer is appended to", _target.nodeName);
}

ThreeRenderer.prototype.get_camera = function() {
	return this.matrix;
}

ThreeRenderer.prototype.render = function(_queue) {

	for(let i = 0; i < _queue.length; i++) {
		this.renderer.clearDepth(false);

		// render the object in the queue
		_queue[i]();
	}
}


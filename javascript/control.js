var Control = function(_audio) {
	
	this.params = new function() {
		this.audio_gain = 15.;
	}

	this.audio = _audio;

	var gui = new dat.GUI();
	gui.add(this.params, 'audio_gain', 0., 500.).onChange(this.update.bind(this));

	this.update();
}

Control.prototype.update = function() {

	console.log(this.audio);
	console.log('audio gain (default):', this.params.audio_gain);

	this.audio.set_gain(this.params.audio_gain);
}
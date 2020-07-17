var AudioAnalyzer = function(gain) {

	this.is_init = false;

	this.bass = 0.;
    this.mid = 0.;
    this.high = 0.;
    this.level = 0.;

    this.cutout = 0.5;

    navigator.getUserMedia = navigator.getUserMedia ||
                         	 navigator.webkitGetUserMedia ||
                          	 navigator.mozGetUserMedia ||
                          	 navigator.msGetUserMedia;

    if(navigator.getUserMedia) {

    	console.log('navigator getUserMedia supported.');

    	navigator.getUserMedia({
    		audio: true,
    	}, this.init.bind(this, gain), this.init_without_stream.bind(this));

    }
}

AudioAnalyzer.prototype.init = function(gain, _stream) {

	console.log('init audio analyzer with stream.');

	const _ctx = new (window.AudioContext || 
        			  window.webkitAudioContext || 
                      window.mozAudioContext || 
        			  window.msAudioContext)();

    let _source = _ctx.createMediaStreamSource(_stream);

    this.analyzer = _ctx.createAnalyser();
    this.analyzer.fftSize = 256;
    this.fftSize = 256;
    this.buffer_length = this.analyzer.frequencyBinCount; // frequency bin count
    this.audio_buffer = new Uint8Array(this.buffer_length); // audio buffer

    this.gain = _ctx.createGain();

    _source.connect(this.gain);
    this.gain.connect(this.analyzer);
    this.gain.gain.value = gain || 15.;

    this.is_init = true;

    console.log("audio analyzer is init");

}

AudioAnalyzer.prototype.init_without_stream = function() {

	console.log('init audio analyzer without stream');
}

AudioAnalyzer.prototype.update = function() {

	if(this.is_init) {

        let _bass = 0., _mid = 0., _high = 0.;

        this.analyzer.getByteFrequencyData(this.audio_buffer);

        const _bin_split = this.buffer_length / 3.;

        for(let i = 0; i < this.buffer_length; i++) {

            let _val = this.audio_buffer[i] / 256;

            // filter out the noise
            if(_val < this.cutout) _val = 0.; 
            
            // lower bins -> _bass
            // mid bins -> _mid
            // higher bins -> _high
            if(i < _bin_split) {
                _bass += _val; 
            } else if(i >= _bin_split && i < _bin_split*2) {
                _mid += _val;
            } else if(i >= _bin_split*2) {
                _high += _val;
            }
        }

        // normalize _bass, _mid, _high
        _bass = _bass / _bin_split;
        _mid = _mid / _bin_split;
        _high = _high / _bin_split;

        console.log(_bass, _mid, _high);

        this.bass = this.bass > _bass ? this.bass * .96 : _bass;
        this.mid = this.mid > _mid ? this.mid * .96 : _mid;
        this.high = this.high > _high ? this.high * .96 : _high;

        this.bass = Math.max(Math.min(this.bass, 1.), 0.);
        this.mid = Math.max(Math.min(this.mid, 1.), 0.);
        this.high = Math.max(Math.min(this.high, 1.), 0.);

        this.level = (this.bass + this.mid + this.high) / 3.;
    }
}

AudioAnalyzer.prototype.set_gain = function(_val) {
	if(this.gain) this.gain.gain.value = _val;
}

AudioAnalyzer.prototype.get_bass = function() {
	return this.bass == undefined ? 0. : this.bass;
}

AudioAnalyzer.prototype.get_mid = function() {
	return this.mid == undefined ? 0. : this.mid;
}

AudioAnalyzer.prototype.get_high = function() {
	return this.high == undefined ? 0. : this.high;
}

AudioAnalyzer.prototype.get_level = function() {
	return this.level == undefined ? 0. : this.level;
}


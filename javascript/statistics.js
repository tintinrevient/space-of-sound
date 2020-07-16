var Statistics = function() {
	
	var stats = new Stats();
	stats.setMode(0); // 0: fps, 1: ms

    document.getElementById("stats").appendChild(stats.domElement);
}
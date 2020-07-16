var m_ctrl;
var m_stats;
var m_audio_analyzer;
var m_renderer;

var m_sphere;
var m_render_queue;

var init = function() {

	m_renderer = new ThreeRenderer(document.body);

	m_audio_analyzer = new AudioAnalyzer();

	m_ctrl =  new Control(m_audio_analyzer);
	m_stats = new Statistics();

	m_sphere = new Sphere(m_renderer, m_audio_analyzer);

	// setup render queue
    m_render_queue = [
    	m_sphere.update.bind(m_sphere)
    ];

}

var update = function() {

	requestAnimationFrame(update);

	// update audio analyzer
    m_audio_analyzer.update();

    // update renderer
    m_renderer.render(m_render_queue);
}

document.addEventListener("DOMContentLoaded", function(){
	init();
	update();
});
var ws = null;

function connect() {
	var host = $("#host").val();
	ws = new WebSocket("ws://" + host + ":8888/piface");

	ws.onmessage = function(evt) {
		// console.log(evt.data);
		var piface = JSON.parse(evt.data);
		update(piface);
	};

	ws.onclose = function(evt) {
		console.log("Connection close ..");
		$("#host").css("background", "#bd1143"); 
		$('#input').css('display', 'none')
		$('#output').css('display', 'none')
		$('#connect').show()
	};

	ws.onopen = function(evt) {
		console.log("WebSocket open ..")
		$("#host").css("background", "#7eb52b"); 
		$('#input').css('display', 'block')
		$('#output').css('display', 'block')
		$('#connect').hide()
	};
}

function update(piface) {

	for (var i=0; i<8; i++) {

		// input
		if (piface['in'][i] == '0') {
			$('#in_' + i).css('background', '#333');
			$('#in_' + i + '_state').html('Off');
		}
		else {
			$('#in_' + i).css('background', '#159');
			$('#in_' + i + '_state').html('On');
		}

		// output
		if (piface['out'][i] == '0') {
			$('#out_' + i).css('background', '#333');
			$('#out_' + i + '_state').html('Off');
		}
		else {
			$('#out_' + i).css('background', '#bd1143');
			$('#out_' + i + '_state').html('On');
		}
	}
}


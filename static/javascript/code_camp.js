function load_code_mirror_blocks(pre_code_num_lines) {
	var user_code_editor = CodeMirror.fromTextArea(
	    document.getElementById("user_code"), {
	        mode: {
	            name: "python",
	            version: 2,
	            singleLineStringErrors: false
	        },
	        lineNumbers: true,
	        firstLineNumber: pre_code_num_lines+1,
	        indentUnit: 4,
	        tabMode: "shift",
	        matchBrackets: true
	});

	var pre_code_editor = CodeMirror.fromTextArea(
	  document.getElementById("pre_code"), {
	    mode: {
	        name: "python",
	        version: 2,
	        singleLineStringErrors: false
	    },
	    lineNumbers: true,
	    indentUnit: 4,
	    tabMode: "shift",
	    matchBrackets: true,
	    readOnly: true,
	  });
	document.body.style.visibility='visible';
}

function show_message(message) {
	console.log("showing message");
	if (message) alert(message);
}
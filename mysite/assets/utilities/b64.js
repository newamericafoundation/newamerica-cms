var fs = require('fs');

fs.readFile('mysite/assets/svg/dropdown.svg', function(err, buffer) {
	if (err) { return console.log(err); }
	console.log(buffer.toString('base64'));
});
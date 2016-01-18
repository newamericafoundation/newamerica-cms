// Use this script to create base64-encoded svg files and appropriate CSS declarations.

var fs = require('fs');

var filePath = 'mysite/assets/svg/dropdown.svg';

fs.readFile(filePath, function(err, buffer) {
	if (err) { return console.log(err); }
	var svgString = buffer.toString('base64');
	var style = "background-image: url('" + "data:image/svg+xml;base64," + svgString + "');"
	console.log(style);
});
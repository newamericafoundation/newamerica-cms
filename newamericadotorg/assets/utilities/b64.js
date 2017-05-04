// Use this script to create base64-encoded svg files and appropriate CSS declarations.

var fs = require('fs');

const filePath = 'newamericadotorg/assets/images/dropdown.svg';

fs.readFile(filePath, function(err, buffer) {
	if (err) { return console.log(err); }
	var encodedSvg = buffer.toString('base64');
	var encodedSvgUrl = "data:image/svg+xml;base64," + encodedSvg;
	var style = "background-image: url('" + encodedSvgUrl + "');"
	console.log(encodedSvgUrl);
});

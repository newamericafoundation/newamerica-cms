var express = require('express');

var app = express();

app.use(express.static(__dirname + '/../'));

app.set('view engine', 'jade');
app.set('views', __dirname + '/views');

app.get('/', function(req, res) {
	res.render('index');
});

[ 'home', 'post', 'press-releases', 'our-people' ].forEach(function(mainUrlFragment) {
	app.get('/' + mainUrlFragment, function(req, res) {
		res.render(mainUrlFragment);
	});
});

app.listen(3000);

var express = require('express');

var app = express();

app.use(express.static(__dirname + '/../'));

app.set('view engine', 'jade');
app.set('views', __dirname + '/views');

app.get('/', function(req, res) {
	res.render('index');
});

app.get('/home', function(req, res) {
	res.render('home');
});

app.get('/post', function(req, res) {
	res.render('post');
});

app.get('/press-releases', function(req, res) {
	res.render('press-releases');
});

app.listen(3000);
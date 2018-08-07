const { Response, Headers, Request } = require('whatwg-fetch');

global.Repsponse = Response;
global.Headers = Headers;
global.Request = Request;

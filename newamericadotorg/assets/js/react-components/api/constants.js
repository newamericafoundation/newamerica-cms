let baseurl;

switch(process.env.NODE_ENV){
  case 'production':
    baseurl = 'https://newamerica.org/api/';
  case 'preview':
    baseurl = 'https://na-preview.herokuapp.com/api/';
  case 'staging':
    baseurl = 'https://na-staging.herokuapp.com/api/';
  default:
    baseurl = 'http://localhost:8000/api/';
}

export const BASEURL = baseurl;
export const SET_PARAMS = 'SET_PARAMS';
export const SET_PARAM = 'SET_PARAM';
export const SET_ENDPOINT = 'SET_ENDPOINT';
export const RECEIVE_RESULTS = 'RECEIVE_RESULTS';
export const RECEIVE_AND_APPEND_RESULTS = 'RECEIVE_AND_APPEND_RESULTS';
export const SET_BASE = 'SET_BASE';
export const SET_TEMPLATE_URL = 'SET_TEMPLATE_URL';
export const RECEIVE_RENDERED_TEMPLATE = 'RECEIVE_RENDERED_TEMPLATE';
export const SET_HAS_NEXT = 'SET_HAS_NEXT';
export const SET_HAS_PREVIOUS = 'SET_HAS_PREVIOUS';
export const SET_PAGE = 'SET_PAGE';
export const SET_RESPONSE = 'SET_RESPONSE';

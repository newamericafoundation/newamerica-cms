let baseurl;

switch(process.env.NODE_ENV){
  case 'production':
    baseurl = 'https://na-preview.herokuapp.com/api/';
    break;
  case 'preview':
    baseurl = 'https://na-preview.herokuapp.com/api/';
    break;
  case 'staging':
    baseurl = 'https://na-staging.herokuapp.com/api/';
    break;
  default:
    baseurl = `${window.location.origin}/api/`;
}

export const BASEURL = baseurl;
export const SET_PARAMS = 'SET_PARAMS';
export const SET_QUERY_PARAM = 'SET_QUERY_PARAM';
export const SET_QUERY = 'SET_QUERY';
export const SET_ENDPOINT = 'SET_ENDPOINT';
export const RECEIVE_RESULTS = 'RECEIVE_RESULTS';
export const RECEIVE_AND_APPEND_RESULTS = 'RECEIVE_AND_APPEND_RESULTS';
export const RECEIVE_AND_PREPEND_RESULTS = 'RECEIVE_AND_PREPEND_RESULTS';
export const SET_BASE = 'SET_BASE';
export const SET_TEMPLATE_URL = 'SET_TEMPLATE_URL';
export const RECEIVE_RENDERED_TEMPLATE = 'RECEIVE_RENDERED_TEMPLATE';
export const SET_HAS_NEXT = 'SET_HAS_NEXT';
export const SET_HAS_PREVIOUS = 'SET_HAS_PREVIOUS';
export const SET_PAGE = 'SET_PAGE';
export const SET_RESPONSE = 'SET_RESPONSE';
export const SET_FETCHING_STATUS = 'SET_FETCHING_STATUS';

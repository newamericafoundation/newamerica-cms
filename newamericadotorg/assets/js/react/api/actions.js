import {
  SET_PARAMS, SET_QUERY_PARAM, SET_QUERY, SET_ENDPOINT, RECEIVE_RESULTS,
  RECEIVE_AND_APPEND_RESULTS, SET_BASE, BASEURL,
  SET_TEMPLATE_URL, RECEIVE_RENDERED_TEMPLATE,
  SET_HAS_NEXT, SET_HAS_PREVIOUS, SET_PAGE, SET_RESPONSE,
  SET_FETCHING_STATUS
} from './constants';
import getNestedState from '../../utils/getNestedState';

export const setParams = (component, {endpoint, query, baseUrl}) => ({
  type: SET_PARAMS,
  component,
  endpoint,
  query,
  baseUrl
});

export const setBase = (component, baseUrl) => ({
  type: SET_BASE,
  component,
  baseUrl
});


export const setQueryParam = (component, {key, value}) => ({
  type: SET_QUERY_PARAM,
  component,
  key,
  value
});

export const setQuery = (component, query) => ({
  type: SET_QUERY,
  component,
  query
});

export const setEndpoint = (component, endpoint) => ({
  type: SET_ENDPOINT,
  component,
  endpoint
});

export const setFetchingStatus = (component, status) => ({
  type: SET_FETCHING_STATUS,
  component,
  status
});

export const receiveResults = (component, results) => ({
  type: RECEIVE_RESULTS,
  component,
  results
});

export const appendResults = (component, results) => ({
  type: RECEIVE_AND_APPEND_RESULTS,
  component,
  results
});

export const setResponse = (component, response) => ({
  type: SET_RESPONSE,
  component,
  response
});


export const setHasNext = (component, hasNext) => ({
  type: SET_HAS_NEXT,
  component,
  hasNext
});

export const setHasPrevious = (component, hasPrevious) => ({
  type: SET_HAS_PREVIOUS,
  component,
  hasPrevious
});

export const setPage = (component, page) => ({
  type: SET_PAGE,
  component,
  page
});

export const setTemplateUrl = (component, templateUrl) => ({
  type: SET_TEMPLATE_URL,
  component,
  templateUrl
})

export const receiveTemplate = (component, template) => ({
  type: RECEIVE_RENDERED_TEMPLATE,
  component,
  template
});

const parseResponse = (json) => {
  let results, hasNext, hasPrevious, page, count;
  if(json.results){
    results = json.results;
    hasNext = json.next!==null;
    hasPrevious = json.previous!==null;
    page = 1;
    count = json.count;
    let re = /.+page=([0-9]+)/;

    if(hasNext){
      let next = re.exec(json.next);
      page = next ? +next[1]-1 : 1;
    } else if(hasPrevious){
      let next = re.exec(json.previous);
      page = next ? +next[1]+1 : 1;
    }
  } else {
    results = json;
    hasNext = false;
    hasPrevious = false;
    page = 1;
    count = null;
  }

  return {
    hasNext, hasPrevious, page, results, count
  }
};

export const fetchData = (component, callback=()=>{}, pend) => (dispatch,getState) => {
  let state = getNestedState(getState(), component);
  let params = state.params;
  let url = new URL(`${params.baseUrl}${params.endpoint}/`);
  for(let k in params.query)
    url.searchParams.append(k, params.query[k]);

  dispatch(setFetchingStatus(component, true));
  return fetch(url, {
      headers: {'X-Requested-With': 'XMLHttpRequest'}
    }).then(response => {
      return response.json();
    }).then(json => {
      let response = parseResponse(json);
      response.pend = pend;
      callback(response);
      dispatch(setResponse(component, response));
    });
}

export const fetchAndAppend = (component, callback=()=>{}) => {
  return fetchData(component, callback, 'append');
}

export const fetchAndPrepend = (component, callback=()=>{}) => {
  return fetchData(component, callback, 'prepend');
}

export const fetchTemplate = (component, callback=()=>{}) => (dispatch,getState) => {
  let url = getState()[component].templateUrl;
  return fetch(url,{
    headers: {'X-Requested-With': 'XMLHttpRequest'}
  }).then(html => {
    dispatch(receiveTemplate(component, html.data));
    callback();
  });
}

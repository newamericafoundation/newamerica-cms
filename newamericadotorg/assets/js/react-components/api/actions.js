import {
  SET_PARAMS, SET_PARAM, SET_ENDPOINT, RECEIVE_RESULTS,
  RECEIVE_AND_APPEND_RESULTS, SET_BASE, BASEURL,
  SET_TEMPLATE_URL, RECEIVE_RENDERED_TEMPLATE
} from './constants';

export const setParams = (component, {endpoint, query}) => {
  return {
    type: SET_PARAMS,
    component,
    endpoint,
    query
  }
}

export const setBase = (component, baseUrl) => {
  return {
    type: SET_BASE,
    component,
    baseUrl
  }
}

export const setParam = (component, {key, value}) => {
  return {
    type: SET_PARAM,
    component,
    key,
    value
  };
}

export const setEndpoint = (component, endpoint) => {
  return {
    type: SET_ENDPOINT,
    component,
    endpoint
  };
}

export const receiveResults = (component, results) => {
  return {
    type: RECEIVE_RESULTS,
    component,
    results
  }
}

export const appendResults = (component, results) => {
  return {
    type: RECEIVE_AND_APPEND_RESULTS,
    component,
    results
  }
}

export const setTemplateUrl = (component, templateUrl) => ({
  type: SET_TEMPLATE_URL,
  component,
  templateUrl
})

export const receiveTemplate = (component, template) => ({
  type: RECEIVE_RENDERED_TEMPLATE,
  component,
  template
})

export const fetchData = (component, callback=()=>{}) => (dispatch,getState) => {
  let params = getState()[component].params;
  let url = new URL(`${params.baseUrl}${params.endpoint}/`);
  for(let k in params.query)
    url.searchParams.append(k, params.query[k]);

  return fetch(url, {
      headers: {'X-Requested-With': 'XMLHttpRequest'}
    }).then(response => {
      return response.json();
    }).then(json => {
      dispatch(receiveResults(component,json.results));
      callback();
    });
}

export const fetchAndAppend = (component, callback=()=>{}) => (dispatch,getState) => {
  let params = getState()[component].params;
  let url = new URL(`${params.baseUrl}${params.endpoint}/`);
  for(let k in params.query)
    url.searchParams.append(k, params.query[k]);

  return fetch(url, {
    headers: {'X-Requested-With': 'XMLHttpRequest'}
  }).then(json => {
    dispatch(appendResults(component,json.data));
    callback();
  });
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

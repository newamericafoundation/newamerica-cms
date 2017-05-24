import {
  SET_PARAMS, SET_PARAM, SET_ENDPOINT, RECEIVE_RESULTS,
  RECEIVE_AND_APPEND_RESULTS, SET_BASE, BASEURL,
  SET_TEMPLATE_URL, RECEIVE_RENDERED_TEMPLATE,
  SET_HAS_NEXT, SET_HAS_PREVIOUS, SET_PAGE, SET_RESPONSE
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
  let results = json.results,
  hasNext = json.next!==null,
  hasPrevious = json.previous!==null,
  page = 1,
  re = /.+page=([0-9]+)/;

  if(hasNext){
    page = (+re.exec(json.next)[1])-1;
  } else if(hasPrevious){
    let next = +re.exec(json.previous)[1];
    page = next ? next : 1;
  }

  return {
    hasNext, hasPrevious, page, results
  }
};

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
      let response = parseResponse(json);

      dispatch(setResponse(component, response));
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
  }).then(response => {
    return response.json();
  }).then(json => {
    let response = parseResponse(json);
    response.append = true;

    dispatch(setResponse(component, response));
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

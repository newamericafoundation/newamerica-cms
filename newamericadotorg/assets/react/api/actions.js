import {
  SET_PARAMS, SET_QUERY_PARAM, SET_QUERY, RESET_QUERY, SET_ENDPOINT, RECEIVE_RESULTS,
  RECEIVE_AND_APPEND_RESULTS, SET_BASE, BASEURL,
  SET_TEMPLATE_URL, RECEIVE_RENDERED_TEMPLATE,
  SET_HAS_NEXT, SET_HAS_PREVIOUS, SET_PAGE, SET_RESPONSE,
  SET_FETCHING_STATUS, SET_HAS_RESULTS
} from './constants';

import getNestedState from '../../lib/utils/get-nested-state';
import { handleResponse, generateUrl, parseResponse } from './action-helpers';
import cache from '../cache';

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

export const resetQuery = (component, query) => ({
  type: RESET_QUERY,
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

export const setHasResults = (component, status) => ({
  type: SET_HAS_RESULTS,
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
});

export const receiveTemplate = (component, template) => ({
  type: RECEIVE_RENDERED_TEMPLATE,
  component,
  template
});

export const fetchData = (component, callback=()=>{}, pend) => (dispatch,getState) => {
  let state = getNestedState(getState(), component);
  let url = generateUrl(state.params)
  let request = `${url.pathname}${url.searchParams.toString()}`;
  let response = cache.get(request);

  if(response){
    response.pend = pend;
    callback(response);
    dispatch(setResponse(component, response));
    dispatch({ component: 'site', type: 'SITE_IS_LOADING', isLoading: false });
    return ()=>{};
  }

  dispatch(setFetchingStatus(component, true));
  dispatch({ component: 'site', type: 'SITE_IS_LOADING', isLoading: true });

  return fetch(url.toString(), {
      headers: {'X-Requested-With': 'XMLHttpRequest'}
    }).then(response => {
      return response.json();
    }).then(json => {
      let response = parseResponse(json);
      response.pend = pend;

      if(!window.user.isAuthenticated && !response.error)
        cache.set(request, response, new Date().getTime() + 6000); // expire in 10 minues


      dispatch({ component: 'site', type: 'SITE_IS_LOADING', isLoading: false });
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

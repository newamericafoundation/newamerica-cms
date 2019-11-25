import {
  SET_PARAMS, SET_QUERY_PARAM, SET_QUERY, RESET_QUERY, SET_ENDPOINT, RECEIVE_RESULTS,
  RECEIVE_AND_APPEND_RESULTS, SET_BASE, BASEURL,
  SET_TEMPLATE_URL, RECEIVE_RENDERED_TEMPLATE,
  SET_HAS_NEXT, SET_HAS_PREVIOUS, SET_PAGE, SET_RESPONSE, APPEND_RESPONSE, PREPEND_RESPONSE,
  SET_IS_FETCHING, SET_HAS_RESULTS, SET_FETCHING_ERROR, SET_FETCHING_SUCCESS,
  SET_FETCHING_FAILURE
} from './constants';

import getNestedState from '../../lib/utils/get-nested-state';
import { generateUrl, parseResponse } from './action-helpers';
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

export const setIsFetching = (component, status) => ({
  type: SET_IS_FETCHING,
  component,
  status
});

export const setFetchingError = (component, error) => ({
  type: SET_FETCHING_ERROR,
  component,
  error
});

export const setFetchingFailure = (component, error) => ({
  type: SET_FETCHING_FAILURE,
  component,
  error
});

export const setFetchingSuccess = (component) => ({
  type: SET_FETCHING_SUCCESS,
  component
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

export const setResponse = (component, response, operation='replace') => ({
  type: SET_RESPONSE,
  component,
  response,
  operation
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

export const fetchData = (component, callback=()=>{}, operation='replace', tries=0) => (dispatch,getState) => {
  let state = getNestedState(getState(), component);
  let url = generateUrl(state.params)
  let request = `${url.pathname}${url.searchParams.toString()}-withnextprevparams`;
  let cachedResponse = cache.get(request);

  if(cachedResponse){
    callback(cachedResponse);
    dispatch(setResponse(component, cachedResponse, operation));
    dispatch({ component: 'site', type: 'SITE_IS_LOADING', isLoading: false });
    return ()=>{};
  }

  dispatch(setIsFetching(component, true));
  dispatch({ component: 'site', type: 'SITE_IS_LOADING', isLoading: true });

  return fetch(url.toString(), {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    }).then(response => {
      if (!response.ok) {
        throw Error(response.statusText);
      }
      return response.json();
    }).then(jsonResponse => {
      if (jsonResponse.error) {
        throw Error(jsonResponse.message);
      }
      return parseResponse(jsonResponse);
    }).then(json => {
      if(!window.user.isAuthenticated){
        try {
          cache.set(request, json, new Date().getTime() + (1000 * 60 * 5)); // expire in 5 minutes
        } catch (e){
          cache.clearAll();
          cache.set(request, json, new Date().getTime() + (1000 * 60 * 5));
        }
      }
      dispatch({ component: 'site', type: 'SITE_IS_LOADING', isLoading: false });
      dispatch(setFetchingSuccess(component));
      callback(json);
      dispatch(setResponse(component, json, operation));

    }).catch(function(error) {
      dispatch(setFetchingError(component, error));
      if(tries < 3){
        setTimeout(() => {
          dispatch(fetchData(component, callback, operation, tries+1));
        }, 500);
      } else {
        dispatch(setFetchingFailure(component, error));
        dispatch({ component: 'site', type: 'SITE_IS_LOADING', isLoading: false });
      }
    });
}

export const fetchAndAppend = (component, callback=()=>{}) => {
  return fetchData(component, callback, 'append');
}

export const fetchAndPrepend = (component, callback=()=>{}) => {
  return fetchData(component, callback, 'prepend');
}

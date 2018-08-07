import {
  SET_PARAMS, SET_QUERY_PARAM, SET_QUERY, RESET_QUERY, SET_ENDPOINT, RECEIVE_RESULTS,
  RECEIVE_AND_APPEND_RESULTS, RECEIVE_AND_PREPEND_RESULTS, SET_BASE, BASEURL,
  SET_TEMPLATE_URL, RECEIVE_RENDERED_TEMPLATE,
  SET_HAS_NEXT, SET_HAS_PREVIOUS, SET_PAGE, SET_RESPONSE,
  SET_IS_FETCHING, SET_HAS_RESULTS, SET_FETCHING_ERROR, SET_FETCHING_SUCCESS,
  SET_FETCHING_FAILURE
} from './constants';

const paramsState = {
  baseUrl: BASEURL, endpoint: 'post', query: {}
}

export const params = (state=paramsState, action) => {
  switch(action.type) {
    case SET_PARAMS:
      return {
        baseUrl: action.baseUrl || state.baseUrl,
        endpoint: action.endpoint || state.endpoint,
        query: (action.query ? { ...state.query, ...action.query } : state.query)
      };
    case SET_QUERY_PARAM:
      return {
        ...state,
        query: {
          ...state.query,
          [action.key]: action.value
        }
      };
    case SET_QUERY:
      return {
        ...state,
        query: {
          ...state.query,
          ...action.query
        }
      };
    case RESET_QUERY:
      return {
        ...state,
        query: action.query || {}
      }
    case SET_ENDPOINT:
      return {
        ...state,
        endpoint: action.endpoint
      }
    case SET_BASE:
      return {
        ...state,
        baseUrl: action.baseUrl
      }
    default:
      return state;
  }
}

export const responseStatus = (state={ status: 'OK', error: false }, action) => {
  switch(action.type) {
    case SET_IS_FETCHING:
      if(action.status === true)
        return {
          status: 'FETCHING',
          error: false
        }
      return state;
    case SET_FETCHING_ERROR:
      return {
        status: 'FAILING',
        error: action.error
      }
    case SET_FETCHING_SUCCESS:
      return {
        status: 'OK',
        error: false
      }
    case SET_FETCHING_FAILURE:
      return {
        status: 'FAILED',
        error: action.error
      }
    default:
      return state;
  }
}

export const results = (state=[], action) => {
  switch(action.type) {
    case SET_RESPONSE:
      if(action.operation==='append')
        return [...state, ...action.response.results];
      else if(action.operation=='prepend')
        return [...action.response.results, ...state];
      else
        return action.response.results;
    case RECEIVE_AND_APPEND_RESULTS:
      return  [...state, ...action.results];
    case RECEIVE_AND_PREPEND_RESULTS:
      return  [...action.results, ...state];
    case RECEIVE_RESULTS:
      return action.results;
    default:
      return state;
  }
}

export const isFetching = (state=false, action) => {
  switch(action.type){
    case SET_RESPONSE:
      return false;
    case SET_IS_FETCHING:
      return action.status;
    default:
      return state;
  }
}

export const hasResults = (state=false, action) => {
  switch(action.type){
    case SET_RESPONSE:
      return true;
    case SET_HAS_RESULTS:
      return action.status;
    default:
      return state;
  }
}

export const count = (state=null, action) => {
  switch(action.type){
    case SET_RESPONSE:
      return action.response.count || null;
    default:
      return state;
  }
}

export const hasNext = (state=false, action) => {
  switch(action.type){
    case SET_RESPONSE:
      return action.response.hasNext;
    case SET_HAS_NEXT:
      return action.hasNext;
    default:
      return state;
  }
}

export const hasPrevious = (state=false, action) => {
  switch(action.type){
    case SET_RESPONSE:
      return action.response.hasPrevious;
    case SET_HAS_PREVIOUS:
      return action.hasPrevious;
    default:
      return state;
  }
}

export const page = (state=1, action) => {
  switch(action.type){
    case SET_RESPONSE:
      return action.response.page;
    case SET_PAGE:
      return action.page;
    default:
      return state;
  }
}

export const templateUrl = (state='', action) => {
  switch(action.type) {
    case SET_TEMPLATE_URL:
      return action.templateUrl;
    default:
      return state;
  }
}

export const templateResult = (state={}, action) => {
  switch(action.type){
    case RECEIVE_RENDERED_TEMPLATE:
      return action.templateResult;
    default:
      return state;
  }
}

const reducers = {
  params,
  responseStatus,
  results,
  hasNext,
  hasPrevious,
  count,
  page,
  isFetching,
  hasResults
}

export default reducers;

import {
  SET_PARAMS, SET_QUERY_PARAM, SET_QUERY, SET_ENDPOINT, RECEIVE_RESULTS,
  RECEIVE_AND_APPEND_RESULTS, RECEIVE_AND_PREPEND_RESULTS, SET_BASE, BASEURL,
  SET_TEMPLATE_URL, RECEIVE_RENDERED_TEMPLATE,
  SET_HAS_NEXT, SET_HAS_PREVIOUS, SET_PAGE, SET_RESPONSE,
  SET_FETCHING_STATUS
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

export const results = (state=[], action) => {
  switch(action.type) {
    case SET_RESPONSE:
      if(!action.response.results) return null;
      if(action.response.pend==='append')
        return [...state, ...action.response.results];
      else if(action.response.pend=='prepend')
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
    case SET_FETCHING_STATUS:
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
      return action.response.hasNext || null;
    case SET_HAS_NEXT:
      return action.hasNext;
    default:
      return state;
  }
}

export const hasPrevious = (state=false, action) => {
  switch(action.type){
    case SET_RESPONSE:
      return action.response.hasPrevious || null;
    case SET_HAS_PREVIOUS:
      return action.hasPrevious;
    default:
      return state;
  }
}

export const page = (state=1, action) => {
  switch(action.type){
    case SET_RESPONSE:
      return action.response.page || null;
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
  results,
  hasNext,
  hasPrevious,
  count,
  page,
  isFetching,
  templateUrl,
  templateResult
}

export default reducers;

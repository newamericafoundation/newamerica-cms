import {
  fetchData, fetchAndAppend, fetchAndPrepend, setEndpoint, setQueryParam, setParams,
  setQuery, resetQuery, setBase, receiveResults
} from '../actions';
import { BASEURL } from '../constants';
import getNestedState from '../../../lib/utils/get-nested-state';

let defaultResponse = { isFetching: false, hasNext: false, hasPrevious: false, count: 0, results: [] };

export const mapStateToProps = (state, { name, baseUrl }) => {
  let componentState = getNestedState(state, name);
  return {
    response: componentState ?
      (componentState.results ? componentState : defaultResponse) :
      defaultResponse,
    baseUrl: baseUrl || state.site.baseUrl || BASEURL
  }
};

export const mapDispatchToProps = (dispatch, props) => ({
  setParams: ({ endpoint, query, baseUrl }, eager) => {
    dispatch(setParams(props.name, { endpoint, query, baseUrl }));
    if(eager===true) dispatch(fetchData(props.name));
  },

  setEndpoint: (endpoint, eager) => {
    dispatch(setEndpoint(props.name, endpoint));
    if(eager===true) dispatch(fetchData(props.name));
  },

  setQueryParam: (key, value, eager) => {
    dispatch(setQueryParam(props.name, {key, value}));
    if(eager===true) dispatch(fetchData(props.name));
  },

  setQuery: (query, eager) => {
    dispatch(setQuery(props.name, query));
    if(eager===true) dispatch(fetchData(props.name));
  },

  resetQuery: (query, eager) => {
    dispatch(resetQuery(props.name, query));
    if(eager===true) dispatch(fetchData(props.name));
  },

  setBase: (baseUrl, eager) => {
    dispatch(setBase(props.name, baseUrl));
    if(eager===true) dispatch(fetchData(props.name));
  },

  fetchData: (callback) => {
    dispatch(fetchData(props.name, callback));
  },

  fetchAndAppend: (callback) => {
    dispatch(fetchAndAppend(props.name, callback));
  },

  fetchAndPrepend: (callback) => {
    dispatch(fetchAndPrepend(props.name, callback));
  },

  receiveResults: (val) => {
    dispatch(receiveResults(props.name, val));
  },

  clearResults: () => {
    dispatch(receiveResults(props.name, []))
  },

  dispatch

});

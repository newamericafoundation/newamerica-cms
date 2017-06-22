import {
  fetchData, fetchAndAppend, fetchAndPrepend, setEndpoint, setQueryParam, setParams,
  setQuery, setBase, receiveResults, setFetchingStatus
} from '../actions';
import getNestedState from '../../../utils/getNestedState';

let defaultResponse = { isFetching: false, hasNext: false, hasPrevious: false, count: 0, results: [] };

export const mapStateToProps = (state, { name }) => {
  let componentState = getNestedState(state, name);
  return {
    response: componentState ?
      (componentState.results ? componentState : defaultResponse) :
      defaultResponse
  }
};

export const mapDispatchToProps = (dispatch, props) => ({
  setParams: ({ endpoint, query, baseUrl }, eager) => {
    dispatch(setParams(props.name, { endpoint, query, baseUrl }));
    if(eager===false) return;
    if(props.eager || eager) dispatch(fetchData(props.name));
  },

  setEndpoint: (endpoint, eager) => {
    dispatch(setEndpoint(props.name, endpoint));
    if(eager===false) return;
    if(props.eager || eager) dispatch(fetchData(props.name));
  },

  setQueryParam: (key, value, eager) => {
    dispatch(setQueryParam(props.name, {key, value}));
    if(eager===false) return;
    if(props.eager || eager) dispatch(fetchData(props.name));
  },

  setQuery: (query, eager) => {
    dispatch(setQuery(props.name, query));
    if(eager===false) return;
    if(props.eager || eager) dispatch(fetchData(props.name));
  },

  setBase: (baseUrl, eager) => {
    dispatch(setBase(props.name, baseUrl));
    if(eager===false) return;
    if(props.eager || eager) dispatch(fetchData(props.name));
  },

  setFetchingStatus: (status) => {
    dispatch(setFetchingStatus(props.name, status));
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
  }

});

import { createStore, applyMiddleware, combineReducers } from 'redux';
import thunkMiddleware from 'redux-thunk'

import apiReducers from './api/reducers';
import siteReducer from './reducers';
import * as components from './installed_components';
import getNestedState from '../utils/get-nested-state';
import { SET_ANY_STATE } from './constants';

let initialState = { site: { adHoc: {}, scrollPosition: 0, scrollEvents: [], scrollDirection: 'FORWARD' }};

let defaultReducer = combineReducers(apiReducers);

let reducers = { 'site': siteReducer };

// Create hash of reducers for each component, adding apiReducers
for(let k in components){
  let name = components[k].NAME.split('.')[0];
  initialState[name] = {};

  if(components[k].REDUCERS)
    reducers[name] = combineReducers({ ...apiReducers, ...components[k].REDUCERS });
  else
    reducers[name] = defaultReducer;
}

const setAnyState = (state) => {
  if(state instanceof Array)
    return [...state];
  if(state instanceof Object)
    return {...state};
  return state;
}

// nest component data by giving name like `componentName.subName.subSubName`;
const setNestedState = (state, componentName, action, rdcr) => {
  let i = componentName.indexOf('.');
  let name = i === -1 ? componentName : componentName.slice(0,i);
  let componentState = state[name] || {};
  if(!rdcr) rdcr = reducers[name] || defaultReducer;

  if(i===-1){
    if(rdcr===SET_ANY_STATE) return { [name]: setAnyState(action.state) };
    return { [name]: rdcr(componentState, action) };
  }

  let subName = componentName.slice(i+1, componentName.length);

  return {
    [name]: {
      ...componentState,
      ...setNestedState(componentState, subName, action, rdcr)
    }
  };
}

// Roll our own top-level reducer using above hash
let reducer = (state=initialState, action) => {
  // Each action needs the name of the component in action.component
  if(action.type && action.component){
    let rdcr = action.type == SET_ANY_STATE ? SET_ANY_STATE : false;
    return {
      ...state,
      ...setNestedState(state, action.component, action, rdcr)
    }
  }

  return state;
};

export default createStore(
  reducer,
  applyMiddleware(thunkMiddleware)
);

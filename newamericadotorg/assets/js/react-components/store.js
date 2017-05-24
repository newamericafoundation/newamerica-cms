import { createStore, applyMiddleware, combineReducers } from 'redux';
import thunkMiddleware from 'redux-thunk'

import apiReducers from './api/reducers';
import { reducers as eventReducers } from './events';

import * as components from './installed_components';

let initialState = {};

let defaultReducer = combineReducers(apiReducers);
let siteReducer = combineReducers({...eventReducers});

let reducers = { 'site': siteReducer };

// Create hash of reducers for each component, adding apiReducers
for(let k in components){
  let name = components[k].NAME
  initialState[name] = {};

  if(components[k].REDUCERS)
    reducers[name] = combineReducers({ ...apiReducers, ...components[k].REDUCERS });
  else
    reducers[name] = defaultReducer;
}

// Roll our own top-level reducer using above hash
let reducer = (state=initialState, action) => {
  // Each action needs the name of the component in action.component
  if(action.type && action.component){
    let componentState = state[action.component];
    let componentReducer = reducers[action.component] ? reducers[action.component] : defaultReducer;
    return {
      ...state,
      [action.component]: componentReducer(componentState, action)
    }
  }

  return state;
};

export default createStore(
  reducer,
  applyMiddleware(thunkMiddleware)
);

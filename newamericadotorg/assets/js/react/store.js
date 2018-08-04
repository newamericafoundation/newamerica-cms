import { createStore, applyMiddleware } from 'redux';
import thunkMiddleware from 'redux-thunk'

import { siteReducer } from './reducers';

export default createStore(
  siteReducer.reducer,
  applyMiddleware(thunkMiddleware)
);

import './scss/base/critical.scss';

import React from 'react';
import ReactDOM from 'react-dom';
import * as ReactRedux from 'react-redux';
import Redux from 'redux';

window.React = React;
window.ReactDOM = ReactDOM;
window.ReactRedux = ReactRedux;
window.Redux = Redux;

import addEventListeners from './lib/add-event-listeners';
import addObservers from './lib/add-observers';

import reactRenderer from './react/react-renderer';
import store from './react/store';
import actions from './react/actions';
import Fetch from './react/api/components/Fetch';
import Response from './react/api/components/Response';

const _Fetch = (props) => (
  <ReactRedux.Provider store={store}>
    <Fetch {...props} />
  </ReactRedux.Provider>
);

const _Response = (props) => (
  <ReactRedux.Provider store={store}>
    <Response {...props} />
  </ReactRedux.Provider>
);

window.newamericadotorg = {
  init: function(settings={ baseUrl: undefined }){
    if(settings.baseUrl)
      store.dispatch({ component: 'site', type: 'SET_SITE_BASEURL', url: settings.baseUrl });

    addEventListeners();
    addObservers();
  },
  reactRenderer,
  actions,
  Fetch: _Fetch,
  Response: _Response
};

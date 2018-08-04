import React from 'react';

import addEventListeners from './lib/add-event-listeners';
import addObservers from './lib/add-observers';

import reactRenderer from './react/react-renderer';
import actions from './react/actions';
import Fetch from './react/api/components/Fetch';
import Response from './react/api/components/Response';

window.newamericadotorg = {
  init: function(){
    addEventListeners();
    addObservers();
  },
  reactRenderer,
  actions,
  Fetch,
  Response
};

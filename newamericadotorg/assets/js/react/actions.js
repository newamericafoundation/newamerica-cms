import { fetchData, setParams } from './api/actions';
import getNestedState from '../utils/get-nested-state';
import setScrollEvents from '../utils/scroll-events';
import store from './store';

// constants
const SET_SCROLL_POSITION = 'SET_SCROLL_POSITION';
const ADD_SCROLL_EVENT = 'ADD_SCROLL_EVENT';
const SET_AD_HOC_STATE = 'SET_AD_HOC_STATE';

// reducers
const scrollPosition = (state=0, action) => {
  switch(action.type){
    case SET_SCROLL_POSITION:
      return action.position;
    default:
      return state;
  }
}

const scrollEvents = (state=[], action) => {
  switch(action.type){
    case ADD_SCROLL_EVENT:
      return [...state, action.eventObject];
    default:
      return state;
  }
}

const adHoc = (state={}, action) => {
  switch(action.type){
    case SET_AD_HOC_STATE:
      return {...state, ...action.object};
    default:
      return state;
  }
}

export const reducers = {
  scrollPosition,
  scrollEvents,
  adHoc
}

// actions
const setScrollPosition = (position) => {
  store.dispatch({
    type: SET_SCROLL_POSITION,
    position: position,
    component: 'site'
  });
}

const addScrollEvent = ({ onEnter, onLeave, enter, leave, offsetTop=-5, offsetBottom=0, selector }) => {
  let els = document.querySelectorAll(selector);
  if(!els.length) return;
  store.dispatch({
    type: ADD_SCROLL_EVENT,
    component: 'site',
    eventObject: { onEnter, onLeave, enter, leave, offsetTop, offsetBottom, els }
  });
}

const setAdHocState = (obj) => {
  store.dispatch({
    type: SET_AD_HOC_STATE,
    component: 'site',
    object: obj
  });
}

const getState = (name) => {
  return getNestedState(store.getState(), name);
}

const getAdHocState = (name) => {
  return getNestedState(store.getState(), `site.adHoc.${name}`);
}

const observerFactory = function(stateName, onChange){
  let currentState;
  return function(){
    let nextState = getNestedState(store.getState(), stateName);
    if(nextState !== currentState) {
      onChange(nextState, currentState);
      currentState = nextState;
    }
  }
}

const addAdHocObserver = ({ stateName, onChange }) => {
  let observer = observerFactory(`site.adHoc.${stateName}`, onChange);
  return store.subscribe(observer);
}

const addObserver = ({ stateName, onChange }) => {
  let observer = observerFactory(stateName, onChange);
  return store.subscribe(observer);
}

export const actions = {
  setScrollPosition,
  addScrollEvent,
  setAdHocState,
  getState,
  getAdHocState,
  addAdHocObserver,
  addObserver
}

// events
const scrollPositionEvent = () => {
  let prevScrollPosition = window.scrollY, scrollPosition = 0;
  window.addEventListener('scroll', (e)=>{
    prevScrollPosition = scrollPosition;
    scrollPosition = window.scrollY;
    setScrollPosition(scrollPosition);
    setScrollEvents(scrollPosition, prevScrollPosition)
    e.preventDefault();
  }, false);
}

// currently initiated in ./site.js
export const events = {
  scrollPosition: scrollPositionEvent
}

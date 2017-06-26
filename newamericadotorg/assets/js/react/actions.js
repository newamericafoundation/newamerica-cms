import { fetchData, setParams } from './api/actions';
import { getNestedState, smoothScroll } from '../utils/index';
import store from './store';

// constants
const SET_SCROLL_POSITION = 'SET_SCROLL_POSITION';
const ADD_SCROLL_EVENT = 'ADD_SCROLL_EVENT';
const SET_SCROLL_DIRECTION = 'SET_SCROLL_DIRECTION';
const RELOAD_SCROLL_EVENT = 'RELOAD_SCROLL_EVENT';
const RELOAD_SCROLL_EVENTS = 'RELOAD_SCROLL_EVENTS';
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

const scrollDirection = (state='FORWARD', action) => {
  switch(action.type){
    case SET_SCROLL_DIRECTION:
      return action.direction;
    default:
      return state;
  }
}

const scrollEvents = (state=[], action) => {
  switch(action.type){
    case ADD_SCROLL_EVENT:
      return [...state, action.eventObject];
    case RELOAD_SCROLL_EVENT:
      // assumes 1 event for each selector...
      let index;
      for(let i=0;i<state.length; i++){
        if(state[i].selector==action.selector){
          index = i;
          break;
        }
      }
      if(!index) return state;
      let e = state.splice(index,1);
      return [...state, {...e, els: document.querySelectorAll(e.selector)}];
    case RELOAD_SCROLL_EVENTS:
      let events = [];
      for(let e of state)
        events.push({...e, els: document.querySelectorAll(e.selector)});
      return events;
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
  scrollDirection,
  scrollEvents,
  adHoc
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

// actions
class Actions {
  setScrollPosition = (position) => {
    window.scrollTo(0, position);
    store.dispatch({
      type: SET_SCROLL_POSITION,
      position: position,
      component: 'site'
    });
    return this;
  }

  addScrollEvent = ({
    onEnter, onLeave, enter, leave, offset, enterOffset, leaveOffset,
    triggerPoint, selector
  }) => {
    let els = document.querySelectorAll(selector);
    if(!els.length) return;
    store.dispatch({
      type: ADD_SCROLL_EVENT,
      component: 'site',
      eventObject: {
        onEnter, onLeave, enter, leave, selector,
        offset, enterOffset, leaveOffset, triggerPoint, els
      }
    });

    return this;
  }

  smoothScroll = smoothScroll

  setScrollDirection = (direction) => {
    store.dispatch({
      type: SET_SCROLL_DIRECTION,
      component: 'site',
      direction
    });
    return this;
  }

  reloadScrollEvents = (selector) => {
    store.dispatch({
      type: selector ? RELOAD_SCROLL_EVENT : RELOAD_SCROLL_EVENTS,
      component: 'site',
      selector
    });

    return this;
  }

  setAdHocState = (obj) => {
    store.dispatch({
      type: SET_AD_HOC_STATE,
      component: 'site',
      object: obj
    });
    return this;
  }

  getState = (name) => {
    return getNestedState(store.getState(), name);
  }

  getAdHocState = (name) => {
    return getNestedState(store.getState(), `site.adHoc.${name}`);
  }

  addAdHocObserver = ({ stateName, onChange }) => {
    let observer = observerFactory(`site.adHoc.${stateName}`, onChange);
    store.subscribe(observer);
    return this;
  }

  addObserver = ({ stateName, onChange }) => {
    let observer = observerFactory(stateName, onChange);
    store.subscribe(observer);
    return this;
  }
}

export const actions = new Actions();
export default actions;

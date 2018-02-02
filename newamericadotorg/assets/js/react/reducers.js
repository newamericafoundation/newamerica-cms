import { combineReducers } from 'redux';
import triggerScrollEvents from '../utils/trigger-scroll-events';
import {
  SET_SCROLL_POSITION, SET_SCROLL_DIRECTION, ADD_SCROLL_EVENT,
  RELOAD_SCROLL_EVENT, RELOAD_SCROLL_EVENTS, TRIGGER_SCROLL_EVENTS, SET_AD_HOC_STATE,
  SET_SCROLL, SET_IS_SCROLLING, SET_SEARCH_STATE, TOGGLE_MOBILE_MENU,
  SET_SITE_BASEURL, SITE_IS_LOADING
} from './constants';

// reducers
const scrollEvents = (state=[], action) => {
  switch(action.type){
    case ADD_SCROLL_EVENT:
      return [...state, action.eventObject];
    case RELOAD_SCROLL_EVENT:
      let e = state.splice(action.event.index,1)[0];
      return [...state, {...e, els: document.querySelectorAll(e.selector)}];
    case RELOAD_SCROLL_EVENTS:
      let events = [];
      for(let e of state)
        events.push({...e, els: document.querySelectorAll(e.selector)});
      return events;
    case TRIGGER_SCROLL_EVENTS:
      // not best redux practice, but easiest way to retrigger scroll events when
      // there is no scroll is through reducer
      triggerScrollEvents(window.scrollY, window.scrollY, 'FORWARD', state);
      return state;
    default:
      return state;
  }
}

const scroll = (state={position: 0, direction: 'FORWARD', events: [], isScrolling: false}, action) => {
  switch(action.type){
    case SET_SCROLL_POSITION:
      return { ...state, position: action.position };
    case SET_SCROLL_DIRECTION:
      return { ...state, direction: action.direction };
    case SET_SCROLL:
      return { ...state, ...action.scroll };
    case SET_IS_SCROLLING:
      return { ...state, isScrolling: action.isScrolling };
    case ADD_SCROLL_EVENT:
    case RELOAD_SCROLL_EVENTS:
    case RELOAD_SCROLL_EVENT:
    case TRIGGER_SCROLL_EVENTS:
      return { ...state, events: scrollEvents(state.events, action)};
    default:
      return state;
  }
}

const searchIsOpen = (state=false, action) => {
  switch(action.type){
    case SET_SEARCH_STATE:
      return action.state;
    default:
      return state;
  }
}

const mobileMenuIsOpen = (state=false, action) => {
  switch(action.type){
    case TOGGLE_MOBILE_MENU:
      return !state;
    default:
      return state;
  }
}

const baseUrl = (state=false, action) => {
  switch(action.type){
    case SET_SITE_BASEURL:
      return action.url;
    default:
      return state;
  }
}

const isLoading = (state=false, action) => {
  switch(action.type){
    case SITE_IS_LOADING:
      return action.isLoading;
    default:
      return state;
  }
}

let reducer = combineReducers({
  scroll,
  searchIsOpen,
  mobileMenuIsOpen,
  baseUrl,
  isLoading
});

const siteReducer = (state, action) => {
  return{
    ...state,
    ...reducer(state, action)
  }
}

export default siteReducer;

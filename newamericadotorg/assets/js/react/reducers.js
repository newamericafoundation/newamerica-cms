import {
  SET_SCROLL_POSITION, SET_SCROLL_DIRECTION, ADD_SCROLL_EVENT,
  RELOAD_SCROLL_EVENT, RELOAD_SCROLL_EVENTS, SET_AD_HOC_STATE
} from './constants';

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
      let e = state.splice(action.event.index,1)[0];
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

export default {
  scrollPosition,
  scrollDirection,
  scrollEvents,
  adHoc
}

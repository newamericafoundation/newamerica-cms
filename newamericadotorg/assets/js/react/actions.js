import { fetchData, setParams } from './api/actions';
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

const addScrollEvent = ({ onEnter, onLeave, enter, leave, offsetTop=0, offsetBottom=0, selector }) => {
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

const getAdHocState = (name) => {
  return store.getState().site.adHoc[name];
}

const addAdHocObserver = ({ stateName, onChange }) => {
  if(!getAdHocState(stateName)) setAdHocState({ [stateName]: null });
  let observer = function(){
    let currentState;
    return function(){
      let nextState = getAdHocState(stateName);
      if(nextState !== currentState) {
        onChange(nextState, currentState);
        currentState = nextState;
      }
    }
  }();
  return store.subscribe(observer);
}

const checkEvents = (scrollPosition, prevScrollPosition) => {
  let direction = scrollPosition < prevScrollPosition ? 'REVERSE' : 'FORWARD';
  let events = store.getState().site.scrollEvents;
  const ENTER_CLASS = 'scroll-entered';
  const LEFT_CLASS = 'scroll-left';
  const IN_VIEW_CLASS = 'scroll-in-view';
  for(let e of events){
    for(let el of e.els){
      let rect = el.getBoundingClientRect(),
      markedEntered = el.classList.contains(ENTER_CLASS),
      markedLeft = el.classList.contains(LEFT_CLASS),
      markedInView = el.classList.contains(IN_VIEW_CLASS),
      hasEntered = rect.top + e.offsetTop <= 0,
      hasLeft = -rect.top > el.offsetHeight + e.offsetBottom,
      inView = hasEntered && !hasLeft;

      if(inView && !markedInView){
        if(e.onEnter) e.onEnter(el, direction);
        el.classList.remove(LEFT_CLASS);
        el.classList.add(IN_VIEW_CLASS);
      }
      if(hasEntered && !markedEntered){
        if(e.enter) e.enter(el, direction);
        el.classList.remove(LEFT_CLASS);
        el.classList.add(ENTER_CLASS);
      }
      // account for scenarios where scroll speed skips over element
      if(!hasEntered && (markedInView||markedLeft||markedEntered)){
        if(e.onLeave) e.onLeave(el, direction);
        el.classList.remove(IN_VIEW_CLASS);
        el.classList.remove(ENTER_CLASS);
        el.classList.remove(LEFT_CLASS);
      }
      if(hasLeft && markedInView){
        if(e.onLeave) e.onLeave(el, direction);
        el.classList.remove(IN_VIEW_CLASS);
        el.classList.remove(LEFT_CLASS);
      }
      if(hasLeft && !markedLeft){
        if(e.leave) e.leave(el, direction);
        el.classList.add(LEFT_CLASS);
      }
    }
  }
}

export const actions = {
  setScrollPosition,
  addScrollEvent,
  setAdHocState,
  getAdHocState,
  addAdHocObserver
}

// events
const scrollPositionEvent = () => {
  let prevScrollPosition = window.scrollY, scrollPosition = 0;
  window.addEventListener('scroll', (e)=>{
    prevScrollPosition = scrollPosition;
    scrollPosition = window.scrollY;
    setScrollPosition(scrollPosition);
    checkEvents(scrollPosition, prevScrollPosition)
    e.preventDefault();
  }, false);
}

// currently initiated in ./site.js
export const events = {
  scrollPosition: scrollPositionEvent
}

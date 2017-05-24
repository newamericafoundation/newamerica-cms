import { fetchData, setParams } from '../react-components/api/actions';
import store from '../react-components/store';

// constants
const SET_SCROLL_POSITION = 'SET_SCROLL_POSITION';

// reducers
const scrollPosition = (state=0, action) => {
  switch(action.type){
    case SET_SCROLL_POSITION:
      return action.position;
    default:
      return state;
  }
}

export const reducers = {
  scrollPosition
}

// actions
const setScrollPosition = (position) => {
  store.dispatch({
    type: SET_SCROLL_POSITION,
    position: position,
    component: 'site'
  });
}

export const actions = {
  setScrollPosition
}

// events
const scrollPositionEvent = () => {
  window.addEventListener('scroll', (e)=>{
    setScrollPosition(window.scrollY);
    e.preventDefault();
  }, false);
}

// currently initiated in ./site.js
export const events = {
  scrollPosition: scrollPositionEvent
}

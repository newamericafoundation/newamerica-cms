import { fetchData, setParams } from '../react-components/api/actions';
import store from '../react-components/store';

// constants
const SET_SCROLL_POSITION = 'SET_SCROLL_POSITION';
const component = 'site';

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

// events
const scrollPositionEvent = (position) => {
  window.addEventListener('scroll', (e)=>{
    store.dispatch({
      type: SET_SCROLL_POSITION,
      position: position || window.scrollY,
      component
    });
  });
}

// currently initiated in ./site.js
export const events = {
  scrollPosition: scrollPositionEvent
}

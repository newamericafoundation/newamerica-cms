import actions from './react/actions';
import store from './react/store';
import triggerScrollEvents from './utils/trigger-scroll-events';

let listeners = [
  function() {
    let prevScrollPosition = window.scrollY, scrollPosition = 0;
    window.addEventListener('scroll', (e)=>{
      scrollPosition = window.scrollY;
      let direction = scrollPosition < prevScrollPosition ? 'REVERSE' : 'FORWARD';
      prevScrollPosition = scrollPosition;

      actions.setScrollPosition(scrollPosition);
      actions.setScrollDirection(direction);
      triggerScrollEvents(scrollPosition, prevScrollPosition, direction, store.getState().site.scrollEvents);

      e.preventDefault();
    }, false);
  }
];

export default () => {
  for(let listener of listeners) listener();
}

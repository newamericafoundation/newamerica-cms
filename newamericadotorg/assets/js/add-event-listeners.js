import actions from './react/actions';
import store from './react/store';
import triggerScrollEvents from './utils/trigger-scroll-events';

let listeners = [
  function onScroll() {
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
  },

  function anchorLinkClick(){
    let anchors = document.querySelectorAll('.anchor-link');
    for(let anchor of anchors) {
      anchor.addEventListener('click', (e) => {
        let offset = e.target.getAttribute('data-anchor-offset') || 0;
        actions.smoothScroll(e.target.getAttribute('href'), { offset: +offset });
        e.preventDefault();
      });
    }
  },

  function scrollTarget(){
    actions.addScrollEvent({
      selector: '.scroll-target'
    });
  }
];

export default () => {
  for(let listener of listeners) listener();
}

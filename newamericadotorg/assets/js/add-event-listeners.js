import actions from './react/actions';
import store from './react/store';
import triggerScrollEvents from './utils/trigger-scroll-events';

let listeners = [
  function onScroll() {
    let timeout = 0;
    let onscroll = (e) => {
      clearTimeout(timeout);
      actions.setIsScrolling(true);
      timeout = setTimeout(()=>{
        actions.setIsScrolling(false);
      }, 50);
    }

    window.addEventListener('scroll', onscroll, false);
    window.addEventListener('touchmove', onscroll, false);
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

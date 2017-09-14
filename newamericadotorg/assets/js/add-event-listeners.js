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
      }, 17);
    }

    window.addEventListener('scroll', onscroll, false);
    window.addEventListener('touchmove', onscroll, false);
  },

  function anchorLinkClick(){
    let anchors = document.getElementsByClassName('anchor-link');
    for(let anchor of anchors) {
      anchor.addEventListener('click', function(e){
        let offset = this.getAttribute('data-anchor-offset') || 0;
        actions.smoothScroll(this.getAttribute('href'), { offset: +offset });
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

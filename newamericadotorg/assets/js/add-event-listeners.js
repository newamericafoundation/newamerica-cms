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

    window.addEventListener('scroll', onscroll, true);
    window.addEventListener('touchmove', onscroll, true);
  },

  function fadeInImages(){
    let images = document.querySelectorAll('.fade-in-image');
    if(images){
      for(let i = 0; i<images.length; i++){
        images[i].onload = function(){ this.classList.add('loaded'); }
      }
    }
  },

  function openSearch(){
    let search = document.querySelector('.header__nav__search');
    if(!search) return;
    search.addEventListener('click', function(){
      store.dispatch({
        type: 'SET_SEARCH_IS_OPEN',
        component: 'site',
        isOpen: true
      });
    });
  },

  function closeSearch(){
    let searchInput = document.getElementById('search-input');
    if(!searchInput) return;
    searchInput.addEventListener('blur', function(){
      store.dispatch({
        type: 'SET_SEARCH_IS_OPEN',
        component: 'site',
        isOpen: false
      });
    });
  },

  function anchorLinkClick(){
    let anchors = document.getElementsByClassName('anchor-link');
    for(let i = 0; i < anchors.length; i++) {
      anchors[i].addEventListener('click', function(e){
        let offset = this.getAttribute('data-anchor-offset') || 0;
        actions.smoothScroll(this.getAttribute('href'), { offset: +offset });
        e.preventDefault();
      });
    }
  },

  function menuToggle(){
    let menu = document.getElementById('mobile-menu-toggle');
    if(!menu) return;
    menu.addEventListener('click', function(){
      store.dispatch({
        type: 'TOGGLE_MOBILE_MENU',
        component: 'site'
      });
    });
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

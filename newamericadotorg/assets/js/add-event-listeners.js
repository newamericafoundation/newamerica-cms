import actions from './react/actions';
import store from './react/store';
import triggerScrollEvents from './utils/trigger-scroll-events';
import dataVizEvents from './data-viz-events';

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


  function onResize() {
    let timeout = 0;
    let onresize = (e) => {
      requestAnimationFrame(()=>{
        actions.setWindowWidth(document.documentElement.clientWidth);
      });
    }
    window.addEventListener('resize', onresize );
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

  dataVizEvents,

  function scrollTarget(){
    actions.addScrollEvent({
      selector: '.scroll-target'
    });
  },

  function activeDropdownToggle(){
    let drops = document.querySelectorAll('.header__nav__dropdown-list__dropdown__main-link.drop');
    if(!drops) return;
    for(let drop of drops){
      drop.addEventListener('click', function(e){
        e.stopPropagation();
        store.dispatch({
          type: 'TOGGLE_ACTIVE_DROPDOWN',
          component: 'site',
          el: this
        });
      });
    }

    document.body.addEventListener('click', () => {
      store.dispatch({
        type: 'TOGGLE_ACTIVE_DROPDOWN',
        component: 'site',
        el: null
      });
    });
  },

  function loadFadeInImage(){
    let images = document.querySelectorAll('.fade-in-image');
    if(!images) return;
    for(let i=0; i<images.length; i++){
      let img = images[i];
      if(img.complete || img.readyState === 4){
        img.classList.add('loaded');
        continue;
      }
      images[i].addEventListener('load', function(){
        this.classList.add('loaded');
      });
    }
  }
];

export default () => {
  for(let listener of listeners) listener();
}

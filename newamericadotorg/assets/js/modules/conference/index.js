import $ from 'jquery';
import scrollr from '../../utilities/scrollr.js';
import speakerSetup from './speaker-expand.js';

export default function() {

  speakerSetup();

  if(!$('body').hasClass('conference-template')) return;

  let navItems = $('.conference-template .navigation-item a, .conference-template .go-to-about');

  navItems.click(function(e){
    e.preventDefault();
    scrollr.smoothScroll($(this).attr('href'), -75, ()=>{
      activeNav($(this));
    });
  });

  scrollr
    .addTrigger('.conference-template section.section-nav', {
      onEnter: function($el,triggerEl){
        if(triggerEl.window.isScrolling) return;

        let id = $el.attr('id');
        let navItem = $(`.navigation-item [href^="#${id}"]`);
        activeNav(navItem);
      },
      offset: -75
    })
    .addTrigger('#hero',{
      hasLeft: function(){
          $('body').addClass('fixed');
      },
      onEnter: function($el,triggerEl){
        if(triggerEl.window.direction === "REVERSE")
          $('body').removeClass('fixed');
      }
    });

  function activeNav($nav){
    navItems.removeClass('active');
    $nav.addClass('active');
    $('.navbar').stop().animate(
      {'scrollLeft':$nav.offset().left-15},
      350
    );
  }
}

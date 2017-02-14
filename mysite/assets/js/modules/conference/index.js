import $ from 'jquery';
import scrollr from '../../utilities/scrollr.js';
import speakerSetup from './speaker-expand.js';

export default function() {

  speakerSetup();

  if(!$('body').hasClass('conference-template')) return;

  let navItems = $('.conference-template .navigation-item a, .conference-template .go-to-about');
  let isScrolling = false;

  navItems.click(function(e){
    e.preventDefault();
    isScrolling = true;
    let id = $(this).attr('href');
    scrollr.smoothScroll(id,-75, ()=>{
      isScrolling=false;
      activeNav($(this));
    });
  });

  scrollr
    .addTrigger('.conference-template section.section-nav', {
      onEnter: function($el){
        if(isScrolling) return;

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
      onEnter: function($el,trigger){
        if(trigger.window.direction === "REVERSE")
          $('body').removeClass('fixed');
      }
    });

  function activeNav($nav){
    navItems.removeClass('active')
    $nav.addClass('active');
    $('.navbar').stop().animate(
      {'scrollLeft':$nav.offset().left-15},
      350
    );
  }
}

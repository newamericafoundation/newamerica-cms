import $ from 'jquery';
import scrollr from '../../utilities/scrollr.js';
import expand from './speaker-expand.js';

export default function() {
  $(document).ready(function(){

    expand();
    let navItems = $('.conference-template .navigation-item a');
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

    $('.conference-template section.section').each(function(){
      let id = this.getAttribute('id');
      let navItem = $(`.navigation-item [href^="#${id}"]`);

      scrollr.addTrigger(this,{
        onEnter: function(el,trigger){
          if(isScrolling) return;
          activeNav(navItem);
        },
        offset: -75
      });
    });

    if(!$('body').hasClass('conference-template')) return;

    scrollr.addTrigger('#hero',{
      hasLeft: function(el,trigger){
          $('body').addClass('fixed');
      },
      onEnter: function(el,trigger){
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

  });
}

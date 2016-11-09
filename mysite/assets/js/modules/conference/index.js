import $ from 'jquery';
import scrollr from '../../utilities/scrollr.js';

export default function() {
  $(document).ready(function(){
    let navItems = $('.conference-template .navigation-item a');

    navItems.click(function(){
      let id = $(this).attr('href');
      scrollr.smoothScroll(id,-75);
    });

    $('.conference-template section.section').each(function(){
      let id = `${this.getAttribute('id')}`;
      let navItem = $(`.navigation-item [href^="#${id}"]`);

      scrollr.addTrigger(this,{
        onEnter: function(el,trigger){
          navItems.removeClass('active')
          navItem.addClass('active');
        },
        offset: -75
      });

    });

    scrollr.addTrigger('#hero',{
      onLeave: function(el,trigger){
          $('body').addClass('fixed');
      },
      onEnter: function(el,trigger){
        if(trigger.window.direction === "REVERSE")
          $('body').removeClass('fixed');
      }
    });

  });
}

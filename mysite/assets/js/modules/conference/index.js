import $ from 'jquery';
import scrollr from '../../utilities/scrollr.js';
import expand from './speaker-expand.js';

export default function() {
  $(document).ready(function(){
    expand();
    let navItems = $('.conference-template .navigation-item a');

    navItems.click(function(e){
      e.preventDefault();
      let id = $(this).attr('href');
      scrollr.smoothScroll(id,-75);
    });

    $('.conference-template section.section').each(function(){
      let id = `${this.getAttribute('id')}`;
      let navItem = $(`.navigation-item [href^="#${id}"]`);

      scrollr.addTrigger(this,{
        onEnter: function(el,trigger){
          if(!navItem.hasClass('active')){
            navItems.removeClass('active')
            navItem.addClass('active');
          }
        },
        offset: -75
      });
    });

    if($('body').hasClass('conference-template')){
      scrollr.addTrigger('#hero',{
        hasLeft: function(el,trigger){
            $('body').addClass('fixed');
        },
        onEnter: function(el,trigger){
          if(trigger.window.direction === "REVERSE")
            $('body').removeClass('fixed');
        }
      });
    }
  });
}

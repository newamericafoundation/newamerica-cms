import $ from 'jquery';
import scrollr from '../../utilities/scrollr.js';


export default function(){
  if($('body').hasClass('template-indepthsection')) return;

  let navItems = $('.panel-nav a');
  let panels = $('.panel-section');

  if(!navItems) return;

  navItems.click(function(e){
    e.preventDefault();
    scrollr.smoothScroll($(this).attr('href'), -150 );
  });

  panels.each(function(){
    let id = this.getAttribute('id');
    scrollr.addTrigger(this,{
      onEnter: function(el){
        navItems.removeClass('is-selected');
        $(`#nav-${id}`).addClass('is-selected');
      },
      offset: -175
    });
  });


}

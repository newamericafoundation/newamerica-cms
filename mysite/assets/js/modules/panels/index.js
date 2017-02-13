import $ from 'jquery';
import scrollr from '../../utilities/scrollr.js';

export default function(){
  if($('body').hasClass('template-indepthsection')) return;

  let navItems = $('.panel-nav a');
  let anchors = $('.panel-anchor-link');
  let panels = $('.panel-section');
  let panelGroups = $('.panel-group');

  if(!navItems) return;

  navItems.click(anchorClick);
  anchors.click(anchorClick);

  panels.each(function(){
    let id = this.getAttribute('id');
    scrollr.addTrigger(this,{
      onEnter: function(el){
        navItems.removeClass('is-selected');
        $(`#nav-${id}`).addClass('is-selected');
        history.pushState(null,null,'#'+id);
      },
      offset: -175
    });
  });

  panelGroups.each(function(){
    let $t = $(this);
    scrollr.addTrigger(this,{
      onEnter: function(){
        panelGroups.removeClass('active');
        $t.addClass('active');
      },
      onLeave: function(){
        $t.removeClass('active');
      },
      offset: -150
    });
  });

}

function anchorClick(e){
  e.preventDefault();
  let href = $(this).attr('href');
  scrollr.smoothScroll(href, -150 );
  history.pushState(null,null,href)
}

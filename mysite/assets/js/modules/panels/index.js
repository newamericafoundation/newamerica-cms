import $ from 'jquery';
import scrollr from '../../utilities/scrollr.js';


export default function(){
  if($('body').hasClass('template-indepthsection')) return;

  let navItems = $('.panel-nav a');
  let anchors = $('.panel-anchor-link');
  let panels = $('.panel-section');

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


}

function anchorClick(e){
  e.preventDefault();
  let href = $(this).attr('href');
  scrollr.smoothScroll(href, -150 );
  history.pushState(null,null,href)
}

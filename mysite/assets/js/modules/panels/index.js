import $ from 'jquery';
import scrollr from '../../utilities/scrollr.js';

export default function(){
  if($('body').hasClass('template-indepthsection')) return;

  let navItems = $('.panel-nav a');
  let anchors = $('.panel-anchor-link');
  let panels = $('.panel-section');
  let panelGroups = $('.panel-group');
  let header = $('.post-header-container');

  if(!navItems) return;
  showContents();

  navItems.click(anchorClick);
  anchors.click(anchorClick);

  scrollr.addTrigger(header[0],{
    onEnter: showContents,
    offset: -250
  });

  panelGroups.each(function(){
    let $t = $(this);
    scrollr.addTrigger(this,{
      onEnter: function(){
        $('.panel-nav').removeClass('active');
        panelGroups.removeClass('active');
        $t.addClass('active');
      },
      onLeave: function(){
        $t.removeClass('active');
      },
      offset: -150
    });
  });

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

function showContents(){
  $('.panel-nav').first().addClass('active');
  $('.panel-group').first().addClass('active');
}

function anchorClick(e){
  e.preventDefault();
  let href = $(this).attr('href');
  scrollr.smoothScroll(href, -150 );
  history.pushState(null,null,href)
}

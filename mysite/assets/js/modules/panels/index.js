import $ from 'jquery';
import scrollr from '../../utilities/scrollr.js';

export default function(){
  if($('body').hasClass('template-indepthsection')) return;

  let navItems = $('.panel-nav a');
  let anchors = $('.panel-anchor-link');

  if(!navItems) return;
  //showContents();

  navItems.click(anchorClick);
  anchors.click(anchorClick);
  $('.touch .cd-nav-trigger').click(function(){
    $('.touch #cd-vertical-nav').toggleClass('open');
  });
  $('.touch #cd-vertical-nav a').click(function(){
    $('.touch #cd-vertical-nav').removeClass('open');
  });
  
  scrollr
    .addTrigger('.post-header-container',{
      onEnter: showContents,
      offset: -250
    })
    .addTrigger('.panel-group',{
      onEnter: function($el, triggerEl, trigger){
        $('.panel-nav').removeClass('active');
        trigger.$elements.removeClass('active');
        $el.addClass('active');
      },
      onLeave: function($el){
        $el.removeClass('active');
      },
      offset: -150
    })
    .addTrigger('.panel-section',{
      onEnter: function($el){
        let id = $el.attr('id');
        navItems.removeClass('is-selected');
        $(`#nav-${id}`).addClass('is-selected');
        history.pushState(null,null,'#'+id);
      },
      offset: -175
    });
}

function showContents(){
  //$('.panel-nav').first().addClass('active');
  //$('.panel-group').first().addClass('active');
  history.pushState(null,null,'#');
}

function anchorClick(e){
  e.preventDefault();
  let href = $(this).attr('href');
  scrollr.smoothScroll(href, -150 );
  history.pushState(null,null,href)
}

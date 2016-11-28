const breakpoint = 640;
const cols = 3;

export default function(){

  let expander = new Expander();
  let $speakers = $('.speaker');
  let $window = $(window);

  $speakers.each(function(i){
    let $t = $(this);
    let position = i+1;

    $t.data({
      active: false,
      index: i,
      position: position,
      row: Math.ceil(position/cols),
      column: position%cols === 0 ? cols : position%cols
    });
  }).click(function(){
    let $t = $(this);
    let d = $t.data();
    let afterIndex = d.index+cols-d.column;
    if(afterIndex>$speakers.length-1) afterIndex = $speakers.length-1;
    if($window.width() < breakpoint) afterIndex = d.index;

    let expandAfter = $speakers[afterIndex];
    let descriptionHeight = $t.find('.description').outerHeight();
    let center = $t.parent().position().left + $t.parent().outerWidth()/2;

    $t.find('.arrow').css('left',center-12.5);

    $speakers.not($t)
      .removeClass('active')
      .data('active', false);

    if(d.active){
      expander.hide();
      $t.removeClass('active')
        .data('active', false);
      return;
    }

    d.active = true;

    expander.setRow(d.row+1);

    if(expander.willChange() && expander.active){
      expander.el.one('transitionend webkitTransitionEnd',function(){
        expander.insertAfter(expandAfter, descriptionHeight);
        $t.addClass('active');
      });
      expander.hide();
    } else {
      expander.insertAfter(expandAfter, descriptionHeight);
      $t.addClass('active');
    }
  });

  $window.resize(function(){
    $speakers.each(function(){
      let $t = $(this);
      let d = $t.data();
      if(d.active) $t.click();
    })
  });

}

class Expander {
  constructor(){
    this.el = $('<div class="expander large-12 columns"></div>');
    this.oldRow = -1;
    this.row = -1;
    this.active = false;

    this.el.appendTo($('.speaker-list'));
  }

  setRow(r){
    this.oldRow = this.row;
    this.row = r;
    return this;
  }

  willChange(){
    if($(window).width() < breakpoint) return true;
    return this.oldRow !== this.row;
  }

  insertAfter(el,height){
    this.el.insertAfter($(el).parent());
    if(height!==null) this.show(height);

    return this;
  }

  show(height){
    this.el[0].style.height = `${this.el[0].scrollHeight}px`
    this.el[0].style.height = `${height}px`;
    reflow(this.el[0]);
    this.active = true;
    return this;
  }

  hide(){
    this.el[0].style.height = '';
    reflow(this.el[0]);
    this.active = false;
    return this;
  }

}

function reflow(el){
  return new Function('rf','return rf')(el.offsetHeight);
}

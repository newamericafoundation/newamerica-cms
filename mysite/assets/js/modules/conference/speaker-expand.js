const breakpoint = 640;
const cols = 3;

export default function(){

  let expander = new Expander();
  let $speakers = $('.speaker:not(.no-description)');
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
    expander.setCurrent($t);

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
        expander.insertAfter(expandAfter);
        $t.addClass('active');
      });
      expander.hide();
    } else {
      expander.insertAfter(expandAfter);
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
    this.el = $('<div class="expander large-12 columns"><span class="arrow" style="display:none;"></span><p></p></div>');
    this.text = this.el.find('p');
    this.arrow = this.el.find('.arrow');
    this.current = null;
    this.currentDescription = null;
    this.oldRow = -1;
    this.row = -1;
    this.active = false;

    this.el.appendTo($('.speaker-list'));
  }

  setCurrent($el){
    this.current = $el;
    this.currentDescription = $el.find('.description');
    return this;
  }

  centerArrow(){
    let center = this.current.parent().position().left + this.current.parent().outerWidth()/2;
    this.arrow.css('left',center-25);
    return this;
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

  insertAfter(el){
    this.el.insertAfter($(el).parent());
    this.show();
    this.centerArrow();
    return this;
  }

  show(){
    this.el[0].style.height = `${this.el[0].scrollHeight}px`
    this.el[0].style.height = `${this.currentDescription.outerHeight()}px`;
    this.text.html(this.currentDescription.html())[0].style.opacity = '1';
    reflow(this.el[0]);
    this.arrow.show();
    this.active = true;
    return this;
  }

  hide(){
    this.el[0].style.height = '';
    this.text.html('')[0].style.opacity = '0';
    reflow(this.el[0]);
    this.arrow.hide();
    this.active = false;
    return this;
  }

}

function reflow(el){
  return new Function('rf','return rf')(el.offsetHeight);
}

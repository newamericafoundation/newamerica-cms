export default function(){

  let expander = new Expander();
  let $speakers = $('.speaker');

  $speakers.each(function(i){
    let $t = $(this);
    let position = i+1;

    $t.data({
      active: false,
      index: i,
      position: position,
      row: Math.ceil(position/3),
      column: position%3 === 0 ? 3 : position%3
    });
  }).click(function(){
    let $t = $(this);
    let d = $t.data();
    let afterIndex = d.index+3-d.column;
    if(afterIndex>$speakers.length-1) afterIndex = $speakers.length-1;

    let expandAfter = $speakers[afterIndex];
    let descriptionHeight = $t.find('.description').outerHeight();
    let center = $t.parent().position().left + $t.parent().outerWidth()/2;

    $t.find('.arrow').css('left',center-12.5);

    $('.speaker.active').not($t).removeClass('active')
    $speakers.not($t).data('active', false);

    if(d.active){
      expander.hide();
      $t.removeClass('active');
      d.active = false;
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

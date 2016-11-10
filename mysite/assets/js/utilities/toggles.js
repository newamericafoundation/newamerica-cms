import $ from 'jquery';

$(document).ready(function(){
  $('[data-toggle]').each(function(){
    new Toggles(this);
  });
});

class Toggles {
  constructor(element){
    this.parent = $(element);
    this.type = this.parent.attr('data-toggle');
    this.toggleElements =
      element.hasAttribute('data-target') ?
      this.parent :
      (
        element.hasAttribute('data-toggle-child') ?
        this.parent.find(element.getAttribute('data-toggle-child')) :
        this.parent.children('[data-target]')
      );

    this.toggles = [];

    for(let i=0; i<this.toggleElements.length; i++){
      let toggle = new Toggle(this.toggleElements[i], this.type);
      this.toggles.push(toggle);

      toggle.element.click((event)=>{
        this.show(i);
      });
    }

    if(this.toggles.length && this.type=='tab') this.show(0);
  }

  show(index) {
    this.toggles[index].show();

    for(let t of this.toggles){
      if(t==this.toggles[index]) continue;
      if(t.active) t.hide();
    }

  }
}

class Toggle {
  constructor(element, type){
    this.element = $(element);
    this.type = type;
    this.target = $(this.element.attr('data-target'));
    this.active = false;

    if(this.type=='collapse') this.hide();
  }

  show() {
    if(this.type=='collapse') {
      if(this.active){
        this.hide();
        return;
      }

      this.target[0].style.height = 0;
      this.target[0].style.height = `${this.target[0].scrollHeight}px`;
      this.target.one('transitionend', ()=>{
        this.target[0].style.height = '';
      });
    }

    if(this.type=='tab') this.target.show();

    this.target.addClass('active');
    this.element.addClass('active');

    this.active = true;
  }

  hide() {

    if(this.type=='collapse'){
      this.target[0].style.height = `${this.target[0].scrollHeight}px`;
      reflow(this.target[0]);
      this.target[0].style.height = 0;
    }

    if(this.type=='tab') this.target.hide();

    this.element.removeClass('active');
    this.target.removeClass('active');

    this.active = false;
  }
}

function reflow(el){
  return new Function('rf', 'return rf')(el.offsetHeight);
}

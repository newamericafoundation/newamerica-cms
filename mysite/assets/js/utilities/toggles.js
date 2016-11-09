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
      this.parent.children('[data-target]');

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
    for(let t of this.toggles)
      t.hide();

    this.toggles[index].show();
  }
}

class Toggle {
  constructor(element, type){
    this.element = $(element);
    this.type = type;
    this.target = $(this.element.attr('data-target'));
    this.active = false;
  }

  show() {
    if(this.type=='collapse') {
      if(this.active){
        this.hide();
        return;
      }
    }

    if(this.type=='tab') this.target.show();

    this.element.addClass('active');
    this.target.addClass('active');

    this.active = true;
  }

  hide() {
    if(this.type=='tab') this.target.hide();

    this.element.removeClass('active');
    this.target.removeClass('active');

    this.active = false;
  }

}

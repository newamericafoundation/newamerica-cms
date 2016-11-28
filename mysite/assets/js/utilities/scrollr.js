import $ from 'jquery';

class Scrollr {
  constructor(){
    this.triggers = {};
    this.isActive = false;

    this.window = {
      lastPosition: 0,
      currentPosition: 0,
      speed: 0,
      direction: false
    }
  }

  start(){
    $(window).bind('scroll', this.fire);
    this.isActive = true;
  }

  stop(){
    $(window).unbind('scroll', this.fire);
    this.isActive = false;
  }

  fire = ()=>{
    this.window.lastPosition = this.window.currentPosition;
    this.window.currentPosition = $(window).scrollTop();
    this.window.speed = this.window.currentPosition - this.window.lastPosition;
    this.window.direction = this.window.speed > 0 ? 'FORWARD' : 'REVERSE'

    for(let k in this.triggers)
      this.triggers[k].fire(this.window);
  }

  triggersSize() {
    return Object.keys(this.triggers).length;
  }

  addTrigger(selector, configs){
    let i = this.triggersSize() + 1;
    this.triggers[i] = new Trigger(selector, configs)
    if(!this.isActive) this.start();
    return this;
  }

  removeTrigger(i){
    delete this.triggers[i];
    if(this.triggersSize()===0) this.stop();
    return this;
  }

  smoothScroll(selector,offset=0, onComplete=()=>{}) {
    let target = $(selector);
    $('body,html').animate(
    	{'scrollTop':target.offset().top+offset},
    	600, onComplete
    );
    return this;
	}
}

class Trigger {
  constructor(selector, {
    hasEntered=()=>{},
    hasLeft=()=>{},
    onEnter=()=>{},
    onLeave=()=>{},
    offset=0
  }){
    this.selector = selector;
    this.element = $(selector);
    this.offset = offset;

    this.isActive = false;
    this.window = {};

    this.events = {
      hasEntered: ()=>{ hasEntered(this.element, this); },
      hasLeft: ()=>{ hasLeft(this.element, this); },
      onEnter: ()=>{ onEnter(this.element, this); },
      onLeave: ()=>{ onLeave(this.element, this); }
    }
  }

  fire(_window){
    this.window = _window;

    let hasLeft = this.hasLeft(),
        hasEntered = this.hasEntered(),
        isBefore = this.isBefore();

    if(hasEntered) this.events.hasEntered();
    if(hasLeft) this.events.hasLeft();
    if((hasLeft || isBefore) && this.isActive){
      this.isActive=false;
      this.events.onLeave();
    } else if(hasEntered && !hasLeft && !this.isActive){
      this.isActive=true;
      this.events.onEnter();
    }
  }

  scrollTop(){
    return this.element.offset().top + this.offset;
  }

  isBefore(){
    return this.window.currentPosition < this.scrollTop();
  }

  hasEntered(){
    return this.window.currentPosition >= this.scrollTop();
  }

  hasLeft(){
    return this.window.currentPosition >= this.scrollTop() + this.element.outerHeight();
  }
}

const scrollr = new Scrollr();
export default scrollr;

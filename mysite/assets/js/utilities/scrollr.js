import $ from 'jquery';

class Scrollr {
  constructor(){
    this.triggers = {};
    this.isActive = false;

    this.window = {
      lastPosition: 0,
      currentPosition: 0,
      speed: 0,
      direction: false,
      isScrolling: false
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
    let name = configs.name ? configs.name :
    (typeof(selector) == 'string' ? selector : selector.nodeName);

    name = this.uniqueName(name);

    this.triggers[name] = new Trigger(selector, configs)
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
    this.window.isScrolling = true;
    $('body,html').animate(
    	{'scrollTop':target.offset().top+offset},
    	600, ()=>{ this.window.isScrolling=false; onComplete(); }
    );
    return this;
	}

  uniqueName(name){
    if(this.triggers[name]){
      let r = /[0-9]+$/;
      let i = name.match(r) ? +name.match(r)[0] + 1 : 1;
      return this.uniqueName(`${name}${i}`);
    } else {
      return name;
    }
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
    this.$elements = $(selector);
    this.triggerElements = [];

    this.$elements.each((i, el)=>{
      this.triggerElements.push(new TriggerElement(el, offset));
    });

    this.events = {
      hasEntered: (el)=>{ hasEntered(el.element, el, this); },
      hasLeft: (el)=>{ hasLeft(el.element, el, this); },
      onEnter: (el)=>{ onEnter(el.element, el, this); },
      onLeave: (el)=>{ onLeave(el.element, el, this); }
    }
  }

  fire(window){
    for(let el of this.triggerElements){
      el.setWindow(window)

      let hasLeft = el.hasLeft(),
          hasEntered = el.hasEntered(),
          isBefore = el.isBefore();

      if(hasEntered) this.events.hasEntered(el);
      if(hasLeft) this.events.hasLeft(el);
      if((hasLeft || isBefore) && el.isActive){
        el.isActive=false;
        this.events.onLeave(el);
      } else if(hasEntered && !hasLeft && !el.isActive){
        el.isActive=true;
        this.events.onEnter(el);
      }
    }
  }
}

class TriggerElement {
  constructor(el, offset=0){
    this.el = el;
    this.element = $(el);
    this.offset = offset;
    this.isActive = false;
  }

  setWindow(window){
    this.window = window;
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

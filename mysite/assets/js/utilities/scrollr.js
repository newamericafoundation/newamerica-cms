import $ from 'jquery';

class Scrollr {
  constructor(){
    this.triggers = {};
    this.isActive = false;
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
    for(let k in this.triggers)
      this.triggers[k].fire();
  }

  triggersSize() {
    return Object.keys(this.triggers).length;
  }

  addTrigger(selector, events){
    let i = this.triggersSize() + 1;
    this.triggers[i] = new Trigger(selector,events)
    if(!this.isActive) this.start();
    return this;
  }

  removeTrigger(i){
    delete this.triggers[i];
    if(this.triggersSize()===0) this.stop();
    return this;
  }
}

class Trigger {
  constructor(selector, {
    onEnter=()=>{},
    onLeave=()=>{},
    onLeaveForward=()=>{},
    onLeaveReverse=()=>{}
  }){
    this.selector = selector;
    this.element = $(selector);
    this.events = {
      onEnter: ()=>{ onEnter(this.element, this)},
      onLeave: ()=>{ onLeave(this.element, this)},
      onLeaveForward: ()=>{ onLeaveForward(this.element, this)},
      onLeaveReverse: ()=>{ onLeaveReverse(this.element, this)}
    }
    this.isActive = false;
  }

  fire(){
    let hasLeft = this.hasLeft(),
        hasEntered = this.hasEntered(),
        isBefore = this.isBefore();

    if(hasLeft && this.isActive){
      this.isActive=false;
      this.events.onLeaveForward();
      this.events.onLeave();
    } else if(hasEntered && !hasLeft && !this.isActive){
      this.isActive=true;
      this.events.onEnter();
    }
  }

  scrollTop(){
    return this.element.offset().top;
  }

  isBefore(){
    return $(window).scrollTop() < this.scrollTop();
  }

  hasEntered(){
    return $(window).scrollTop() >= this.scrollTop();
  }

  hasLeft(){
    return $(window).scrollTop() >= this.scrollTop() + this.element.outerHeight();
  }
}

const scrollr = new Scrollr();
export default scrollr;

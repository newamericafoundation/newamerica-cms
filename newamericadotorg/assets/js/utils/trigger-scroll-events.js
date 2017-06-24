/**
  Loop through a list of events and assign class names and fire events, if defined
  when element enters or leaves viewPoint
  Events are objects with properties:
  {
    els => an array of html elements,
    selector => document.querySelectorAll compatable string,
    triggerPoint => where in viewPort event should be triggered options: ['top', 'bottom', 'middle'],
    enterOffset => offset from triggerPoint for enter events. if defined as % (eg '50%'), offsets by % of element's outerHeight,
    leaveOffset => offset from triggerPoint for leave events. If defined as %, (eg '50%'), offsets by % of element's outerHeight,
    enter => event for any point the element has passed the triggerPoint,
    onEnter => event for the exact moment when element hits the triggerPoint,
    leave => event for any point the element (including outerHeight) is outside the triggerPoint,
    onLeave => event for the exact moment when element (including outerHeight) goes outside the triggerPoint
  }
**/

import store from '../react/store';

const getOffset = (el, attr) => {
  let offset = el.getAttribute(attr);
  if(!offset) return false;
  if(offset.indexOf('%')!=-1)
    return el.offsetHeight * offset.replace('%', '')/100;
  return +offset;
}

const getTriggerPointOffset = (triggerPoint, docHeight) => {
  switch(triggerPoint){
    case 'top':
      return 0;
    case 'bottom':
      return -docHeight;
    case 'middle':
      return -docHeight/2;
    default:
      return 0;
  }
}

const scrollEvents = (scrollPosition, prevScrollPosition, direction, events) => {
  let docHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);

  const ENTER_CLASS = 'scroll-entered';
  const LEFT_CLASS = 'scroll-left';
  const IN_VIEW_CLASS = 'scroll-in-view';
  for(let e of events){
    for(let el of e.els){
      let rect = el.getBoundingClientRect(),
      enterOffset = getOffset(el, 'data-scroll-enter-offset') || e.enterOffset || 0,
      leaveOffset = getOffset(el, 'data-scroll-leave-offset') || e.leaveOffset || 0,
      triggerPoint = el.getAttribute('data-scroll-trigger-point') || e.triggerPoint || 'top',
      triggerPointOffset = getTriggerPointOffset(triggerPoint, docHeight);

      let markedEntered = el.classList.contains(ENTER_CLASS),
      markedLeft = el.classList.contains(LEFT_CLASS),
      markedInView = el.classList.contains(IN_VIEW_CLASS),
      hasEntered = rect.top + enterOffset + triggerPointOffset <= 0,
      hasLeft = -rect.top > el.offsetHeight + leaveOffset + triggerPointOffset,
      inView = hasEntered && !hasLeft;

      if(inView && !markedInView){
        if(e.onEnter) e.onEnter(el, direction);
        el.classList.remove(LEFT_CLASS);
        el.classList.add(IN_VIEW_CLASS);
      }
      if(hasEntered && !markedEntered){
        if(e.enter) e.enter(el, direction);
        el.classList.remove(LEFT_CLASS);
        el.classList.add(ENTER_CLASS);
      }
      // account for scenarios where scroll speed skips over element
      if(!hasEntered && (markedInView||markedLeft||markedEntered)){
        if(e.onLeave) e.onLeave(el, direction);
        el.classList.remove(IN_VIEW_CLASS);
        el.classList.remove(ENTER_CLASS);
        el.classList.remove(LEFT_CLASS);
      }
      if(hasLeft && markedInView){
        if(e.onLeave) e.onLeave(el, direction);
        el.classList.remove(IN_VIEW_CLASS);
        el.classList.remove(LEFT_CLASS);
      }
      if(hasLeft && !markedLeft){
        if(e.leave) e.leave(el, direction);
        el.classList.add(LEFT_CLASS);
      }
    }
  }
}

export default scrollEvents;

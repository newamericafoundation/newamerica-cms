/**
  * Loop through a list of Events and when element enters or leaves viewPort
  * assign class names and fire event callbacks, if defined.
  *
  *
  * @typedef {Object} Event
  * @property {HtmlElement[]} els - (required) an array of html elements,
  * @property {string} selector - (required) document.querySelectorAll compatable string,
  * @property {string} triggerPoint - (default: 'top', options: 'top', 'middle', 'bottom') part of viewPort event is triggered,
  * @property {(number|string)} offset - (default: 0) offset for both enter and leave events. essentially shifts entire frame by this value. if defined as % (eg '50%'), offsets by % of element's outerHeight,
  * @property {(number|string)} enterOffset - (default: 0) offset from triggerPoint for enter events. if defined as % (eg '50%'), offsets by % of element's outerHeight,
  * @property {(number|string)} leaveOffset - (default: 0) offset from triggerPoint for leave events. If defined as %, (eg '50%'), offsets by % of element's outerHeight,
  * @property {eventCallback} enter - event for any point after the element has passed the triggerPoint,
  * @property {eventCallback} onEnter - event for the exact moment when element hits the triggerPoint,
  * @property {eventCallback} leave - event for any point after the element (including outerHeight) is outside the triggerPoint,
  * @property {eventCallback} onLeave - event for the exact moment when element (including outerHeight) goes outside the triggerPoint
  *
  * @callback eventCallback
  * @param {HtmlElement} el - the triggered html element
  * @param {string} direction - the direction scroll is moving ('FORWARD' or 'REVERSE')
  *
**/

const scrollEvents = (scrollPosition, prevScrollPosition, direction, events) => {
  let docHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);

  const ENTER_CLASS = 'scroll-entered';
  const LEFT_CLASS = 'scroll-left';
  const IN_VIEW_CLASS = 'scroll-in-view';
  for(let e of events){
    for(let el of e.els){
      let rect = el.getBoundingClientRect(),
      offset = getOffset(el, 'data-scroll-offset') || e.offset || 0,
      enterOffset = getOffset(el, 'data-scroll-enter-offset') || offset || e.enterOffset || 0,
      leaveOffset = getOffset(el, 'data-scroll-leave-offset') || offset || e.leaveOffset || 0,
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

function getOffset(el, attr) {
  let offset = el.getAttribute(attr);
  if(!offset) return false;
  if(offset.indexOf('%')!=-1)
    return el.offsetHeight * offset.replace('%', '')/100;
  return +offset;
}

function getTriggerPointOffset(triggerPoint, docHeight){
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

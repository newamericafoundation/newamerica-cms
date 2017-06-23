import store from '../react/store';

const scrollEvents = (scrollPosition, prevScrollPosition) => {
  let direction = scrollPosition < prevScrollPosition ? 'REVERSE' : 'FORWARD';
  let events = store.getState().site.scrollEvents;
  const ENTER_CLASS = 'scroll-entered';
  const LEFT_CLASS = 'scroll-left';
  const IN_VIEW_CLASS = 'scroll-in-view';
  for(let e of events){
    for(let el of e.els){
      let rect = el.getBoundingClientRect(),
      offsetTop = +el.getAttribute('data-scroll-offset-top') || e.offsetTop,
      offsetBottom = +el.getAttribute('data-scroll-offset-bottom') || e.offsetBottom,
      markedEntered = el.classList.contains(ENTER_CLASS),
      markedLeft = el.classList.contains(LEFT_CLASS),
      markedInView = el.classList.contains(IN_VIEW_CLASS),
      hasEntered = rect.top + offsetTop <= 0,
      hasLeft = -rect.top > el.offsetHeight + offsetBottom,
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

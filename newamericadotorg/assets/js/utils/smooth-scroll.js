/**
  * mostly from
  * https://pawelgrzybek.com/page-scroll-in-vanilla-javascript/
**/
import easings from './easings';
import getOffset from './get-offset';

const smoothScroll = (destination, options={}, callback) => {
  let duration = options.duration===0 ? 0 : (options.duration || 350),
  easing = options.easing || 'easeInOutQuad',
  offset = options.offset || 0,
  direction = options.direction || 'vertical',
  el = options.el || document.body;

  if(typeof el == 'string' && el.indexOf('#')===0)
    el = document.getElementById(el.replace('#', ''));
  if(typeof destination == 'string' && destination.indexOf('#')===0)
    destination = document.getElementById(destination.replace('#',''));

  let start,
  startTime = 'now' in window.performance ? performance.now() : new Date().getTime(),
  destinationOffset;

  if(direction=='vertical'){
    start = el.pageYOffset || el.scrollTop;
    destinationOffset = typeof destination === 'number' ? Math.ceil(destination + offset) : Math.ceil(getOffset(destination, el).top + offset);
  } else {
    start = el.pageXOffset || el.scrollLeft;
    destinationOffset = typeof destination === 'number' ? Math.ceil(destination + offset) : Math.ceil(getOffset(destination, el).left + offset);
  }
  
  if ('requestAnimationFrame' in window === false || duration===0) {
    if(direction=='vertical')
      el.scrollTop = destinationOffset;
    else
      el.scrollLeft = destinationOffset;
    if (callback) {
      callback();
    }
    return;
  }

  function scroll() {
    const now = 'now' in window.performance ? performance.now() : new Date().getTime();
    const time = Math.min(1, ((now - startTime) / duration));
    const timeFunction = easings[easing](time);
    const next = Math.ceil((timeFunction * (destinationOffset - start)) + start);

    if(direction=='vertical')
      el.scrollTop = next;
    else
      el.scrollLeft = next;

    if (next === destinationOffset) {
      if (callback) {
        callback();
      }
      return;
    }
    requestAnimationFrame(scroll);
  }

  scroll();
}

export default smoothScroll;

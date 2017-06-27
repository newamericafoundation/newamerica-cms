/**
  * mostly from
  * https://pawelgrzybek.com/page-scroll-in-vanilla-javascript/
**/

import easings from './easings';

const smoothScroll = ( destination, options={}, callback) => {
  let duration = options.duration || 350,
  easing = options.easing || 'easeInOutQuad',
  offset = options.offset || 0,
  direction = options.direction || 'vertical',
  el = options.el || document.body;

  if(typeof destination == 'string' && destination.indexOf('#')===0)
    destination = document.getElementById(destination.replace('#',''));

  let start,
  startTime = 'now' in window.performance ? performance.now() : new Date().getTime(),
  documentHeight,
  windowHeight,
  destinationOffset;

  if(direction=='vertical'){
    start = el.pageYOffset || el.scrollTop;
    documentHeight = Math.max(el.scrollHeight, el.offsetHeight, el.clientHeight);
    windowHeight = el.innerHeight || el.clientHeight;
    destinationOffset = typeof destination === 'number' ? Math.ceil(destination + offset) : Math.ceil(destination.getBoundingClientRect().top + start + offset - el.offsetTop);
  } else {
    start = el.pageXOffset || el.scrollLeft;
    documentHeight = Math.max(el.scrollWidth, el.offsetWidth, el.clientHeight);
    windowHeight = el.innerHeight;
    destinationOffset = typeof destination === 'number' ? Math.ceil(destination + offset) : Math.ceil(destination.getBoundingClientRect().left + start + offset - el.offsetLeft);
  }

  if ('requestAnimationFrame' in window === false) {
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

    let currentPoint;
    if(direction=='vertical')
      el.scrollTop = currentPoint = next;
    else
      el.scrollLeft = currentPoint = next;

    if (currentPoint === (destinationOffset)) {
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

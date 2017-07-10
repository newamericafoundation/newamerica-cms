import actions from './react/actions';
import store from './react/store';
import triggerScrollEvents from './utils/trigger-scroll-events';

let observers = [
  function scroll(){
    let prevPosition = window.scrollY || window.pageYOffset,
    direction, prevDirection, position = 0, animationFrame = 0, startTime = 0;
    const onscroll = () => {
      position = window.scrollY || window.pageYOffset;

      if(position===prevPosition) direction = prevDirection
      else direction = position < prevPosition ? 'REVERSE' : 'FORWARD';

      triggerScrollEvents(
        position, prevPosition, direction,
        store.getState().site.scroll.events
      );
      actions.setScroll({ position, direction });
      prevPosition = position;
      prevDirection = direction;
      animationFrame = window.requestAnimationFrame(onscroll);
    }

    actions.addObserver({
      stateName: 'site.scroll.isScrolling',
      onChange: (isScrolling) => {
        if(isScrolling)
          animationFrame = window.requestAnimationFrame(onscroll);
        else
          window.cancelAnimationFrame(animationFrame);
      }
    });
  },

  function scrollDirection(){
    let body = document.getElementsByTagName('body')[0];
    actions.addObserver({
      stateName: 'site.scroll.direction',
      onChange: (direction) => {
        if(direction=='FORWARD') body.classList.remove('scroll-reverse');
        else body.classList.add('scroll-reverse');
      }
    });
  }
];

export default () => {
  for(let observer of observers) observer();
}

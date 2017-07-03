import actions from './react/actions';
import store from './react/store';
import triggerScrollEvents from './utils/trigger-scroll-events';

let observers = [
  function scroll(){
    let body = document.getElementsByTagName('body')[0];
    let prevPosition = window.scrollY, position = 0, animationFrame = 0, startTime = 0;
    const onscroll = () => {
      let position = window.scrollY;

      let direction = position < prevPosition ? 'REVERSE' : 'FORWARD';
      if(direction=='FORWARD') body.classList.remove('scroll-reverse');
      else body.classList.add('scroll-reverse');

      triggerScrollEvents(
        position, prevPosition, direction,
        store.getState().site.scroll.events
      );
      prevPosition = position;
      actions.setScroll({ position, direction });
      animationFrame = window.requestAnimationFrame(onscroll);
    }

    actions.addObserver({
      stateName: 'site.scroll.isScrolling',
      onChange: (isScrolling) => {
        if(isScrolling)
          animationFrame = window.requestAnimationFrame(onscroll);
        else
          window.cancelAnimationFrame(animationFrame);}
    });
  }
];

export default () => {
  for(let observer of observers) observer();
}

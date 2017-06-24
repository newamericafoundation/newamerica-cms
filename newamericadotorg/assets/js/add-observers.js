import actions from './react/actions';

let observers = [
  function(){
    let body = document.getElementsByTagName('body')[0];
    actions.addObserver({
      stateName: 'site.scrollDirection',
      onChange: (dir) => {
        if(dir=='FORWARD') body.classList.remove('scroll-reverse');
        else body.classList.add('scroll-reverse');
      }
    });
  },

  function(){
    actions.addScrollEvent({
      selector: '.scroll-target'
    });
  }
];

export default () => {
  for(let observer of observers) observer();
}

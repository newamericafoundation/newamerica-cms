import { render } from 'react-dom';
import { Provider } from 'react-redux';
import { camelize, getProps } from '../utils/index';

export default class Composer {
  constructor(store){
    this.store = store;
    this.components = {};
  }

  add(COMPONENT) {
    if(COMPONENT.MULTI)
      this.__addMulti__(COMPONENT.NAME, COMPONENT.ID, COMPONENT.APP);
    else
      this.__add__(COMPONENT.NAME, COMPONENT.ID, COMPONENT.APP);
  }

  __addMulti__(name, id, App) {
    let selector = `compose__${id}`;
    let els = document.getElementsByClassName(selector);
    if(!this.components[selector])
      this.components[selector] = { components: [], multi: true };

    for(let i=0; i<els.length; i++){
      let app = this.__render__(els[i], App, i);
      this.components[selector].components.push({ name:`name.${i}`, selector, el: els[i], app });
      // if(els[i].hasAttribute('replace-this')){
      //   els[i].parentNode.insertBefore(els[i].firstChild, els[i]);
      //   els[i].parentNode.removeChild(els[i]);
      // }
    }

    if(els.length===0)
      this.components[selector].render = () => { this.__addMulti__(name, id, App); }
    else
      this.components[selector].render = () => { console.warn(`${name} is already rendered!`); }
  }

  __add__(name, id, App) {
    let selector = `compose__${id}`;
    let el = document.getElementById(selector);
    this.components[selector] = { name, selector, el, multi: false }

    if(el){
      this.components[selector].app = this.__render__(el, App);

      if(el.hasAttribute('replace-this')){
        el.parentNode.insertBefore(el.firstChild, el);
        el.parentNode.removeChild(el);
      }
      this.components[selector].render = () => { console.warn(`${name} is already rendered!`); }
    } else {
      this.components[selector].render = () => { this.__add__(name, id, App); }
    }
  }

  __render__(el, App, index=0){
    let props = getProps(el);
    props.index = index;
    return render(
      <Provider store={this.store}><App {...props}/></Provider>,
      el
    );
  }
}

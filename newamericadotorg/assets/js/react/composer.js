import { render } from 'react-dom';
import { Provider } from 'react-redux';
import { camelize } from '../utils/index';

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
    this.components[name] = { components: [], multi: true };

    for(let i=0; i<els.length; i++){
      let app = this.__render__(els[i], App);
      this.components[name].components.push({ name, selector, el: els[i], app });
    }

    if(els.length===0)
      this.components[name].render = () => { this.__addMulti__(name, id, App); }
    else
      this.components[name].render = () => { console.warn(`${name} is already rendered!`); }
  }

  __add__(name, id, App) {
    let selector = `compose__${id}`;
    let el = document.getElementById(selector);
    this.components[name] = { name, selector, el, multi: false }

    if(el){
      this.components[name].app = this.__render__(el, App);
      this.components[name].render = () => { console.warn(`${name} is already rendered!`); }
    } else {
      this.components[name].render = () => { this.__add__(name, id, App); }
    }
  }

  __render__(el, App){
    let props = getProps(el);
    return render(
      <Provider store={this.store}><App {...props}/></Provider>,
      el
    );
  }
}

function getProps(el){
  let props = {};
  for(let i=0; i<el.attributes.length; i++){
    let attr = el.attributes[i],
    name = attr.nodeName,
    val = attr.nodeValue;
    if(name.indexOf('data-')!==-1){
      props[camelize(name.replace('data-',''))] = val;
    }
  }
  return props;
}

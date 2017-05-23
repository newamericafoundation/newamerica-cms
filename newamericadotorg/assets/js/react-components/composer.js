import { render } from 'react-dom';
import { Provider } from 'react-redux';

export default class Composer {
  constructor(store){
    this.store = store;
    this.components = {};
  }

  add(COMPONENT) {
    return this._add(COMPONENT.NAME, COMPONENT.ID, COMPONENT.APP);
  }

  _add(name, _id, App, warn) {
    const store = this.store;
    const id = `compose__${_id}`;
    const el = document.getElementById(id);

    if(!this.components[name])
      this.components[name] = { name, id, el, app: null };

    if(el) {
      this.components[name].app = render(
        <Provider store={store}><App/></Provider>, el );

      this.components[name].render = function(){
        console.warn(`${name} is already rendered!`); }

    } else if(warn) {
      console.warn(`Document must have element with id '${id}' to render ${name} component.`);

    } else {
      this.components[name].render = () => {
        this._add(name,_id,App,true); }

    }
    return this;
  }
}

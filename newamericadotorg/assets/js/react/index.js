import Composer from './composer';
import { fetchData, setParams } from './api/actions';
import * as components from './installed_components';
import store from './store';

let composer = new Composer(store);
composer.installed_components = components;

composer.init = () => {
  store.dispatch(setParams('meta', { endpoint: 'meta' } ));
  store.dispatch(fetchData('meta'));

  for(let k in components)
    composer.add(components[k]);
}

export default composer;

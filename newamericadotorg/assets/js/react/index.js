import Composer from './composer';
import { fetchData, setParams } from './api/actions';
import * as components from './installed_components';
import store from './store';

let composer = new Composer(store);

composer.init = () => {
  store.dispatch(setParams('programData', { endpoint: 'program' } ));
  store.dispatch(fetchData('programData'));

  store.dispatch(setParams('contentTypes', { endpoint: 'content-types' }));
  store.dispatch(fetchData('contentTypes'));

  for(let k in components)
    composer.add(components[k]);
}

export default composer;

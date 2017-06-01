import Composer from './composer';
import * as components from './installed_components';
import store from './store';
import siteInit from './site';

let composer = new Composer(store);

composer.init = () => {
  siteInit();

  for(let k in components)
    composer.add(components[k]);
}

export default composer;

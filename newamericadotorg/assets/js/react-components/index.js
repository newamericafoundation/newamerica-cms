import Composer from './composer';
import * as components from './installed_components';
import store from './store';
import siteInit from './site';

let composer = new Composer(store);

// initialize on ready
if(document.readyState != 'loading') init();
else document.addEventListener('DOMContentLoaded', init);

function init() {
  siteInit();

  for(let k in components)
    composer.add(components[k]);
}

export default composer;

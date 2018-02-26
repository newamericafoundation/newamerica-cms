import Composer from './composer';
import { fetchData, setParams } from './api/actions';
import { SET_IP } from './constants';
import * as components from './installed_components';
import store from './store';
import cache from './cache';

let composer = new Composer(store);
composer.installed_components = components;

composer.init = () => {
  store.dispatch(setParams('meta', { endpoint: 'meta' } ));
  store.dispatch(fetchData('meta'));

  if(cache.get('publicIp')){
    store.dispatch({
      type: SET_IP,
      component: 'site',
      ip: cache.get('publicIp')
    });
  } else {
    fetch('https://freegeoip.net/json/').then((response)=>(
      response.json()
    )).then((json)=>{
      cache.set('publicIp', json.ip, new Date().getTime() + 3600000);
      store.dispatch({
        type: SET_IP,
        component: 'site',
        ip: json.ip
      });
    });
  }

  for(let k in components)
    composer.add(components[k]);
}

export default composer;

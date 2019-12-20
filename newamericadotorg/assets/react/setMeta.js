import store from './store';
import { fetchData, setParams } from './api/actions';

const setMeta = () => {
  store.dispatch(setParams('meta', { endpoint: 'meta' } ));
  store.dispatch(fetchData('meta'));
}

export default setMeta;

import store from './store';
import cache from './cache';

const setMeta = () => {
  store.dispatch(setParams('meta', { endpoint: 'meta' } ));
  cache.set('/api/meta/',
    {
      count: 0,
      hasNext: false,
      hasPrevious: false,
      page: 1,
      results: window.meta
    }
  );
  store.dispatch(fetchData('meta'));
}

export default setMeta;

import * as REDUCERS from './reducers';

import { NAME, ID } from './constants';
import Filters from './components/Filters';
import ContentList from './components/ContentList';

const APP = () => (
  <section className="content-list-wrapper container">
      <Filters />
      <ContentList />
  </section>
)

export default {
  NAME, ID, APP, REDUCERS
};

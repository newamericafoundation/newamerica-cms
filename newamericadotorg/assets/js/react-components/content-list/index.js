import * as REDUCERS from './reducers';
import { NAME, ID } from './constants';
import SiteFilter from './components/SiteFilter';
import ContentList from './components/ContentList';

const APP = () => (
  <section className="content-list-wrapper container">
      <SiteFilter />
      <ContentList />
  </section>
)

export default {
  NAME, ID, APP, REDUCERS
};

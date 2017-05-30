import { Route, Switch } from 'react-router-dom';
import Filter from './PeopleFilter';
import { connect } from 'react-redux';

export const Routes = () => (
  <Switch>
    <Route path="/board/" component={Filter} other="ald;jga;gj;ajg"/>
    <Route path="/leadership/" component={Filter} />
    <Route path='/our-people/programs/' component={Filter} />
    <Route path="/our-people/" component={Filter} />
    <Route path="/central-staff/" component={Filter} />
    <Route path="/:programSlug/our-people/" component={Filter} />
  </Switch>
);

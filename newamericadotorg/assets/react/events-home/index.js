import React, { Component, Suspense } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { NAME, ID } from './constants';
import { Response } from '../components/API';
import { LoadingDots } from '../components/Icons';

const Events = React.lazy(() =>
  import(/* webpackChunkName: "na-events" */ './components/Events')
);

const Loading = () => (
  <div className="loading-icon-container">
    <LoadingDots />
  </div>
);

class Routes extends Component {
  render() {
    return (
      <Router>
        <div className="container">
          <Route
            path="/events/"
            render={props => (
              <Events {...props} program={this.props.response.results} />
            )}
          />{' '}
          {/*hack for compatability with Program/Event component*/}
        </div>
      </Router>
    );
  }
}

class APP extends Component {
  render() {
    let { contentTypes, programs } = this.props;
    return (
      <Suspense fallback={<Loading />}>
        <Response component={Routes} name="meta" />
      </Suspense>
    );
  }
}

export default { NAME, ID, APP };

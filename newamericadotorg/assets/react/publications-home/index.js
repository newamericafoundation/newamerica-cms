import { Route } from 'react-router-dom';
import GARouter from '../ga-router';
import React, { Component, Suspense } from 'react';
import { Response } from '../components/API';
import { NAME, ID } from './constants';
import { LoadingDots } from '../components/Icons';

const Publications = React.lazy(() =>
  import(/* webpackChunkName: "na-publications" */ './components/Publications')
);

const Loading = () => (
  <div className="loading-icon-container">
    <LoadingDots />
  </div>
);

class Routes extends Component {
  render() {
    let {
      response: { results }
    } = this.props;
    return (
      <div className="container">
        <GARouter>
          <div className="homepage__publications">
            <Route
              path="/:contentType/"
              render={props => (
                <Publications
                  content_types={results.content_types}
                  programs={results.programs}
                  {...props}
                />
              )}
            />
          </div>
        </GARouter>
      </div>
    );
  }
}

class APP extends Component {
  render() {
    return (
      <Suspense fallback={<Loading />}>
        <Response component={Routes} name="meta" />
      </Suspense>
    );
  }
}

export default {
  NAME,
  ID,
  APP
};

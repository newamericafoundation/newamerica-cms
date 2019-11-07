import React, { Component, Suspense } from 'react';
import { Route, Switch } from 'react-router-dom';
import GARouter from '../ga-router';
import { Fetch, Response } from '../components/API';
import { NAME, ID } from './constants';
import { LoadingDots } from '../components/Icons';

const OurStory = React.lazy(() =>
  import(/* webpackChunkName: "na-our-story" */ './pages/OurStory')
);
const PressRoom = React.lazy(() =>
  import(/* webpackChunkName: "na-press-room" */ './pages/PressRoom')
);
const OurFunding = React.lazy(() =>
  import(/* webpackChunkName: "na-our-funding" */ './pages/OurFunding')
);
const Jobs = React.lazy(() =>
  import(/* webpackChunkName: "na-jobs" */ './pages/Jobs')
);
const Programs = React.lazy(() =>
  import(/* webpackChunkName: "na-programs" */ './pages/Programs')
);
const Subscribe = React.lazy(() =>
  import(/* webpackChunkName: "na-subscribe" */ './pages/Subscribe')
);
const Search = React.lazy(() =>
  import(/* webpackChunkName: "na-search" */ './pages/Search')
);

const Loading = () => (
  <div className="loading-icon-container">
    <LoadingDots />
  </div>
);

class Routes extends Component {
  componentDidMount() {
    let { dispatch } = this.props;
    dispatch({
      type: 'RELOAD_SCROLL_EVENTS',
      component: 'site'
    });
  }
  render() {
    let props = this.props;
    return (
      <div className="home__panels">
        <Route
          path="/jobs/"
          render={_props => <Jobs {...props} {..._props} />}
        />
        <Route
          path="/our-story/"
          render={_props => <OurStory {...props} {..._props} />}
        />
        <Route
          path="/press-room/"
          render={_props => <PressRoom {...props} {..._props} />}
        />
        <Route
          path="/our-funding/"
          render={_props => <OurFunding {...props} {..._props} />}
        />
      </div>
    );
  }
}

class APP extends Component {
  render() {
    let { pageId, title, slug } = this.props;
    return (
      <Suspense fallback={<Loading />}>
        <GARouter>
          <Switch>
            <Route
              path="/programs/"
              render={() => (
                <Fetch
                  endpoint={`program`}
                  fetchOnMount={true}
                  name={NAME}
                  component={Programs}
                />
              )}
            />
            <Route path="/search/" render={props => <Search {...props} />} />
            <Route
              path="/subscribe/"
              render={() => <Response name="meta" component={Subscribe} />}
            />
            <Route
              path="/(jobs|our-story|press-room|our-funding)/"
              render={props => (
                <Fetch
                  endpoint={`home/${pageId}`}
                  fetchOnMount={true}
                  {...props}
                  name={NAME}
                  component={Routes}
                />
              )}
            />
          </Switch>
        </GARouter>
      </Suspense>
    );
  }
}

export default { APP, ID, NAME };

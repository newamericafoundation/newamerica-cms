import React, { Component } from 'react';
import BasicHeader from './components/BasicHeader';
import Tabs from '../components/Tabs';
import Tab from '../components/Tab';
import Body from './components/Body';
import Authors from './components/Authors';
import { NAME, ID } from './constants';
import { Fetch, Response } from '../components/API';
import { Route, Switch, Redirect } from 'react-router-dom';
import GARouter from '../ga-router';
import store from '../store';
import { setResponse } from '../api/actions';

const SinglePage = ({ report, dispatch, location }) => (
  <div className={`report report--polling-dashboard single-page`}>
    <div className="container">
      <BasicHeader report={report} />

      <Tabs>
        <Tab title={'Survey Reports'}>
          <p>Reports</p>
        </Tab>
        <Tab title={'About'}>
          <p>About</p>
        </Tab>
      </Tabs>

      <Body
        section={report.sections[0]}
        report={report}
        dispatch={dispatch}
        location={location}
      />

      <div
        className="container report__body single-page-body margin-0"
        id="authors"
      >
        <div className="post-body-wrapper">
          <h3 className="margin-bottom-25">Authors</h3>
          <Authors authors={report.authors} md={true} />
        </div>
      </div>

      {report.acknowledgments && (
        <div
          className="container report__body single-page-body margin-0"
          id="acknowledgments"
        >
          <div className="post-body-wrapper">
            <h3 className="margin-top-0 margin-bottom-25">
              Acknowledgments
            </h3>
            <div
              className="report__acknowledgments"
              dangerouslySetInnerHTML={{
                __html: report.acknowledgments,
              }}
            />
          </div>
        </div>
      )}
    </div>
  </div>
);

class SurveysHome extends Component {
  constructor(props) {
    super(props);
  }
  componentDidMount() {
    let { report } = this.props;
    this.props.dispatch({
      type: 'RELOAD_SCROLL_EVENTS',
      component: 'site',
    });
  }
  render() {
    let { location, match, report, redirect, dispatch } = this.props;
    return (
      <div>
        <SinglePage {...this.props} />
      </div>
    );
  }
}

class Routes extends Component {
  reportRender = (props) => {
    let {
      response: { results },
    } = this.props;
    return (
      <SurveysHome
        {...props}
        dispatch={this.props.dispatch}
        report={results}
      />
    );
  };

  redirect = (props) => {
    let {
      response: { results },
    } = this.props;
    return (
      <Redirect
        to={`${props.match.url}${results.sections[0].slug}`}
      />
    );
  };

  render() {
    let {
      response: { results },
    } = this.props;
    if (!results) return null;
    return (
      <GARouter>
        <Switch>
          <Route
            path={`/admin/pages`}
            render={() => <Redirect to={results.url} />}
          />
          <Route
            path="/:program/reports/:reportTitle/:sectionSlug?"
            render={this.reportRender}
          />
          <Route
            path="/:program/:subprogram/reports/:reportTitle/:sectionSlug?"
            render={this.reportRender}
          />
        </Switch>
      </GARouter>
    );
  }
}

class APP extends Component {
  componentDidMount() {
    if (window.initialState) {
      store.dispatch(
        setResponse(NAME, {
          count: 0,
          page: 1,
          hasNext: false,
          hasPrevious: false,
          results: window.initialState,
        })
      );
    }
  }

  render() {
    let { reportId } = this.props;

    if (window.initialState)
      return <Response name={NAME} component={Routes} />;

    return (
      <Fetch
        name={NAME}
        endpoint={`report/${reportId}`}
        fetchOnMount={true}
        component={Routes}
      />
    );
  }
}

export default { APP, NAME, ID };

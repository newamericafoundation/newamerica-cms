import { NAME, ID } from './constants';
import React, { Component } from 'react';
import { Fetch, Response } from '../components/API';
import { LoadingDots } from '../components/Icons';
import { setResponse } from '../api/actions';
import store from '../store';
import { Fetch, Response } from '../components/API';
import BasicHeader from './components/BasicHeader';
import Tabs from '../components/Tabs';
import Tab from '../components/Tab';
import AboutTab from './components/AboutTab';
import SurveysTab from './components/SurveysTab';

class SurveyHomepage extends Component {
  state = {
    loaded: false,
  };
  componentDidMount() {
    setTimeout(() => {
      this.setState({ loaded: true });
    }, 1500);
  }

  render() {
    let {
      response: { results },
    } = this.props;

    return (
      <div className={`report report--polling-dashboard single-page`}>
        <div className="container">
          <BasicHeader report={results} />

          <Tabs>
            <Tab title={'Survey Reports'}>
              <SurveysTab data={results} />
            </Tab>
            <Tab title={'About'}>
              <AboutTab report={results} />
            </Tab>
          </Tabs>
        </div>
      </div>
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
    let { programId } = this.props;

    if (window.initialState)
      return <Response name={NAME} component={Routes} />;

    return (
      <Fetch
        name={NAME}
        endpoint={`program/survey/${programId}`}
        fetchOnMount={true}
        component={SurveyHomepage}
      />
    );
  }
}

export default { NAME, ID, APP };

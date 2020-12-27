/* DocumentMeta defined in ./components/Nav.js */

import { NAME, ID } from './constants';
import React, { Component } from 'react';
import { Fetch } from '../components/API';
import { LoadingDots } from '../components/Icons';
import BasicHeader from './components/BasicHeader';
import Tabs from '../components/Tabs';
import Tab from '../components/Tab';
import AboutTab from './components/AboutTab';
import SurveysTab from './components/SurveysTab';

class SurveyHomepage extends Component {
  render() {
    let {
      response: { results },
    } = this.props;

    return (
      <div className={`report report--polling-dashboard single-page`}>
        <div className="container">
          <BasicHeader data={results} />

          <Tabs>
            <Tab title={'Survey Reports'}>
              <SurveysTab data={results} />
            </Tab>
            <Tab title={'About'}>
              <AboutTab data={results} />
            </Tab>
          </Tabs>
        </div>
      </div>
    );
  }
}

const LoadingState = ({ title }) => (
  <div className="container">
    <div className="program__header margin-bottom-10">
      <div className="program__heading__wrapper">
        <h1 className="margin-0 promo">{title}</h1>
      </div>
    </div>
    <div className="horizontal-nav">
      <ul className="inline">
        <li>
          <h5>&nbsp;</h5>
        </li>
      </ul>
    </div>
    <div className="margin-top-60">
      <LoadingDots />
    </div>
  </div>
);

class APP extends Component {
  render() {
    let { programId, programType } = this.props;

    return (
      <div>
        <Fetch
          component={SurveyHomepage}
          name={NAME}
          loadingState={<LoadingState title={''} />}
          endpoint={`program/survey/${programId}`}
          fetchOnMount={true}
          programType={programType}
        />
      </div>
    );
  }
}

export default { NAME, ID, APP };

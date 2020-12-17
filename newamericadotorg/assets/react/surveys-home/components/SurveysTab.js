import './SurveysTab.scss';
import React, { Component } from 'react';
import FilterBlock from '../../components/FilterBlock';
import TeaserListing from '../../components/TeaserListing';

class SurveysTab extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    const { surveyData } = this.props;

    return (
      <div className="surveys-tab">
        {/* <FilterBlock /> */}
        <TeaserListing surveys={surveyData} />
      </div>
    );
  }
}

export default SurveysTab;

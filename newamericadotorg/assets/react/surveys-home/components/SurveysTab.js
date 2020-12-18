import './SurveysTab.scss';
import React, { Component } from 'react';
import {
  format as formatDate,
  subDays,
  isWithinRange,
  subMonths,
  subYears,
} from 'date-fns/esm';
import TeaserListing from '../../components/TeaserListing';

class SurveysTab extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
    };

    this.buildFilters = this.buildFilters.bind(this);
  }
  buildFilters() {
    let topics = [];
    let demographics = [];
    let organization = [];

    this.props.surveys.dashboard.map((survey, i) => {
      topics = topics.concat(survey.tags);
      demographics = demographics.concat(survey.demographics);
      organization = organization.concat(survey.organization);
    });

    this.setState({
      filters: {
        topics: new Set(topics),
        demographics: new Set(demographics),
        organization: new Set(organization),
      },
    });
  }
  componentDidMount() {
    this.buildFilters();
  }

  render() {
    console.log(this.state);

    return (
      <div className="surveys-tab">
        <div className="checkbox__container checkbox__container-vertical">
          Filter List
        </div>

        <TeaserListing surveys={this.props.surveys} />
      </div>
    );
  }
}

export default SurveysTab;

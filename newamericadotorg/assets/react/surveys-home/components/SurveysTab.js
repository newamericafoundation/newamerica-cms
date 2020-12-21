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
import CtaCArd from '../../components/CtaCard';

class SurveysTab extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      tempFilters: [
        {
          label: 'Topics',
          options: [
            {
              label: 'Topic 1',
              id: 'topic-1',
              value: 'topic-1',
            },

            {
              label: 'Topic 2',
              id: 'topic-2',
              value: 'topic-2',
            },

            {
              label: 'Topic 3',
              id: 'topic-3',
              value: 'topic-3',
            },
          ],
        },
        {
          label: 'Demographics',
          options: [
            {
              label: 'Demographic 1',
              id: 'demographic-1',
              value: 'demographic-1',
            },

            {
              label: 'Demographic 2',
              id: 'demographic-2',
              value: 'demographic-2',
            },

            {
              label: 'Demographic 3',
              id: 'demographic-3',
              value: 'demographic-3',
            },
          ],
        },
        {
          label: 'Publication Date',
          options: [
            {
              label: 'Date - 3 months',
              id: '3-months',
              value: '3-months',
            },
            {
              label: 'Date - 6 months',
              id: '6-months',
              value: '6-months',
            },
          ],
        },
      ],
    };
    this.toggleCheckboxGroup = this.toggleCheckboxGroup.bind(this);
    this.buildFilters = this.buildFilters.bind(this);
  }
  toggleCheckboxGroup(index) {
    this.setState((prevState) => {
      const newItems = [...prevState.tempFilters];
      newItems[index].show = !newItems[index].show;
      return newItems[index];
    });
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
        <div className="surveys-tab__sidebar checkbox__container checkbox__container">
          {this.state.tempFilters.map((group, index) => (
            <div className="checkbox__group" key={index}>
              <h4
                className="checkbox__group-title"
                onClick={() => this.toggleCheckboxGroup(index)}
              >
                {group.label}
                <i
                  className={`fa fa-${group.show ? 'times' : 'plus'}`}
                ></i>
              </h4>
              {group.show &&
                group.options.map((option, i) => (
                  <div key={i} className="checkbox-group__options">
                    <input
                      value={option.value}
                      id={option.id}
                      type="checkbox"
                    />
                    <label
                      htmlFor={option.id}
                      className="checkbox__label"
                    >
                      {option.label}
                    </label>
                  </div>
                ))}
            </div>
          ))}
          <div className="margin-top-35">
            <CtaCArd
              title={'Call for Submissions'}
              description={
                'Know of a poll or report that should be added to our list?'
              }
              type={'email'}
              linkText={'Send us an email today.'}
              url={'user@sitename.com'}
            />
          </div>
        </div>

        <div className="surveys-tab__results">
          <TeaserListing surveys={this.props.surveys} />
          <div className="margin-top-25">
            <CtaCArd
              title={'Love all this insight?'}
              description={
                'Subscribe to our newsletter to receive updates on what’s new in Education Policy.'
              }
              type={'link'}
              linkText={'Subscribe'}
              url={'google.com'}
            />
          </div>
        </div>
      </div>
    );
  }
}

export default SurveysTab;

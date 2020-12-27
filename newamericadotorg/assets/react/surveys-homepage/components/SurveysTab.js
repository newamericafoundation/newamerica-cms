import React from 'react';
import CheckboxGroup from './CheckboxGroup';
import TeaserListing from './TeaserListing';
import './SurveysTab.scss';

class SurveysTab extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: {},
      tags: this.props.data.survey_home_page.surveys.reduce(
        (acc, cur) => {
          const tags = cur['tags'];
          tags.forEach((tag, i) => {
            acc[tag.title] = false;
          });

          return acc;
        },
        {}
      ),
      demos: this.props.data.survey_home_page.surveys.reduce(
        (acc, cur) => {
          const demos = cur['demos_key'];

          demos.forEach((demo, i) => {
            acc[demo.title] = false;
          });

          return acc;
        },
        {}
      ),
      orgs: this.props.data.survey_home_page.surveys.reduce(
        (acc, cur) => {
          const orgs = cur['org'];

          orgs.forEach((org, i) => {
            acc[org.title] = false;
          });

          return acc;
        },
        {}
      ),
      dateRange: {
        3: false,
        6: false,
        12: false,
        24: false,
        36: false,
      },
      sizeRange: {
        one: false,
        two: false,
        three: false,
        four: false,
      },
      dataType: {
        Qual: false,
        Quant: false,
        'Mixed Methods': false,
      },
      national: {
        represented: false,
        notRepresented: false,
      },
    };

    this.onFilterChange = this.onFilterChange.bind(this);
  }

  onFilterChange = (name, filter) => {
    this.setState({ [name]: filter });
  };

  render() {
    const {
      tags,
      demos,
      orgs,
      dateRange,
      sizeRange,
      dataType,
      national,
    } = this.state;

    const checkedValues = {
      tags: Object.keys(tags).filter((key) => tags[key] === true),
      demos: Object.keys(demos).filter((key) => demos[key] === true),
      orgs: Object.keys(orgs).filter((key) => orgs[key] === true),
      dateRange: Object.keys(dateRange).filter(
        (key) => dateRange[key] === true
      ),
      sizeRange: Object.keys(sizeRange).filter(
        (key) => sizeRange[key] === true
      ),
      dataType: Object.keys(dataType).filter(
        (key) => dataType[key] === true
      ),
      national,
    };

    return (
      <div className="surveys-tab">
        <div className="surveys-tab__sidebar">
          <CheckboxGroup
            title="Topic"
            options={Object.keys(tags).map((tag) => ({
              id: tag,
              checked: false,
              label: tag.charAt(0).toUpperCase() + tag.slice(1),
            }))}
            onChange={(filterState) =>
              this.onFilterChange('tags', filterState)
            }
          />

          <CheckboxGroup
            title="Demographic"
            options={Object.keys(demos).map((demo) => ({
              id: demo,
              checked: false,
              label: demo.charAt(0).toUpperCase() + demo.slice(1),
            }))}
            onChange={(filterState) =>
              this.onFilterChange('demos', filterState)
            }
          />
          <CheckboxGroup
            title="Publication Date"
            options={[
              { checked: false, label: 'Last 3 months', id: '3' },
              { checked: false, label: 'Last 6 months', id: '6' },
              { checked: false, label: 'Within 1 year', id: '12' },
              { checked: false, label: 'Within 2 years', id: '24' },
              { checked: false, label: '3+ years ago', id: '36' },
            ]}
            onChange={(filterState) =>
              this.onFilterChange('dateRange', filterState)
            }
          />
          <CheckboxGroup
            title="Sample Size"
            options={[
              { checked: false, label: '< 1,000', id: 'one' },
              { checked: false, label: '1,000 - 5,000', id: 'two' },
              {
                checked: false,
                label: '5,000 - 10,000',
                id: 'three',
              },
              { checked: false, label: '> 10,000', id: 'four' },
            ]}
            onChange={(filterState) =>
              this.onFilterChange('sizeRange', filterState)
            }
          />
          <CheckboxGroup
            title="Organization"
            options={Object.keys(orgs).map((org) => ({
              id: org,
              checked: false,
              label: org.charAt(0).toUpperCase() + org.slice(1),
            }))}
            onChange={(filterState) =>
              this.onFilterChange('orgs', filterState)
            }
          />

          <CheckboxGroup
            title="Type of Data"
            options={[
              { checked: false, label: 'Qualitative', id: 'qual' },
              {
                checked: false,
                label: 'Quantitative',
                id: 'quant',
              },
              {
                checked: false,
                label: 'Mixed Methods',
                id: 'mixed',
              },
            ]}
            onChange={(filterState) =>
              this.onFilterChange('dataType', filterState)
            }
          />

          <CheckboxGroup
            title="Sample Representaion"
            options={[
              {
                checked: false,
                label: 'Nationally Represented',
                id: 'represented',
              },
              {
                checked: false,
                label: 'Not Nationally Represented',
                id: 'notRepresented',
              },
            ]}
            onChange={(filterState) =>
              this.onFilterChange('national', filterState)
            }
          />
        </div>
        <div className="surveys-tab__results">
          <TeaserListing
            data={this.props.data.survey_home_page.surveys}
            checkedValues={checkedValues}
          />
        </div>
      </div>
    );
  }
}

export default SurveysTab;

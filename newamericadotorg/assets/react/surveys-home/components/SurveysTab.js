import './SurveysTab.scss';
import React, { Component } from 'react';
import TeaserListing from '../../components/TeaserListing';
import CtaCArd from '../../components/CtaCard';
import Sidebar from './Sidebar';

class SurveysTab extends Component {
  constructor(props) {
    super(props);
    this.state = {
      size: {
        one: true,
        two: true,
        three: true,
      },
      demographics: this.props.data.dashboard.reduce((acc, cur) => {
        cur['demographics'].forEach((demographic) => {
          if (!acc[demographic]) {
            acc[demographic] = true;
          }
        });
        return acc;
      }, {}),
      tags: this.props.data.dashboard.reduce((acc, cur) => {
        cur['tags'].forEach((tag) => {
          if (!acc[tag]) {
            acc[tag] = true;
          }
        });
        return acc;
      }, {}),
      organizations: this.props.data.dashboard.reduce((acc, cur) => {
        cur['organization'].forEach((organization) => {
          if (!acc[organization]) {
            acc[organization] = true;
          }
        });
        return acc;
      }, {}),
    };
    this.onFilterChange = this.onFilterChange.bind(this);
  }

  onFilterChange = (name, filter) => {
    console.log(name, filter);
    this.setState({ [name]: filter });
  };
  render() {
    const { size, demographics, tags, organizations } = this.state;

    let _data = this.props.data;

    _data = this.props.data.dashboard
      .filter((val) => {
        const demographic = val['demographics'];

        if (
          Object.keys(demographics).some(
            (key) => demographics[key] && demographic.includes(key)
          )
        ) {
          return true;
        } else {
          return false;
        }
      })
      .filter((val) => {
        const tagString = val['tags'];
        if (
          Object.keys(tags).some(
            (key) => tags[key] && tagString.includes(key)
          )
        ) {
          return true;
        } else {
          return false;
        }
      });

    console.log(_data);
    return (
      <div className="surveys-tab">
        <div className="surveys-tab__sidebar checkbox__container checkbox__container">
          <Sidebar
            onFilterChange={this.onFilterChange}
            tags={Object.keys(tags)}
            demographics={Object.keys(demographics)}
            organizations={Object.keys(organizations)}
          />
        </div>

        <div className="surveys-tab__results">
          <TeaserListing data={_data} />
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

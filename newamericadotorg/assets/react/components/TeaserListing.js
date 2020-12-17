import './TeaserListing.scss';
import React, { Component } from 'react';
import moment from 'moment';

class TeaserListing extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { surveys } = this.props;

    return (
      <div className="teaser-listing">
        <div className="teaser-listing__sort">
          <h3>{surveys.count} Results</h3>
          <div>
            <label htmlFor="">Sort by</label>
            <ul className="teaser-listing__sort-dropdown">
              <li>
                <button>Most recent</button>
              </li>
              <li>
                <button>Title (A-Z)</button>
              </li>
              <li>
                <button>Title (Z-A)</button>
              </li>
            </ul>
          </div>
        </div>
        <div className="teaser-listing__list container">
          {surveys.dashboard.map((item, index) => (
            <a
              href={item.url}
              className="teaser-listing__item card margin-bottom-10 row"
              key={`teaser-listing-item-${index}`}
            >
              <div className="col-sm-10">
                <h4 className="teaser-listing__item-title">
                  {item.title}
                </h4>
                <p className="teaser-listing__item-description margin-top-0">
                  {item.description}
                </p>
              </div>
              <div className="col-sm-2 teaser-listing__item-date">
                {moment(item.date).format('MMM Do YYYY')}
              </div>
            </a>
          ))}
        </div>
      </div>
    );
  }
}

export default TeaserListing;

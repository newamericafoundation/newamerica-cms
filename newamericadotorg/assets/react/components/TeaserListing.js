import './TeaserListing.scss';
import React, { Component } from 'react';
import moment from 'moment';

class TeaserListing extends Component {
  constructor(props) {
    super(props);
  }
  state = {
    isExanded: false,
    sortValue: {},
    sortOptions: [
      { title: 'Most Recent', value: 'recent' },
      { title: 'Title (A-Z)', value: 'desc' },
      { title: 'Title (Z-A)', value: 'asc' },
    ],
  };
  componentDidMount() {
    this.setState({ sortValue: this.state.sortOptions[0] });
  }
  render() {
    const { surveys } = this.props;
    const { isExpanded, sortValue, sortOptions } = this.state;

    return (
      <div className="teaser-listing">
        <div className="teaser-listing__header">
          <h3 className="margin-0">
            {surveys.dashboard.length} Results
          </h3>
          <div className="teaser-listing__sort-wrapper">
            <button
              className="teaser-listing__sort"
              onClick={() =>
                this.setState({ isExpanded: !isExpanded })
              }
            >
              <h6 className="with-caret--down margin-0">
                Sort by {sortValue.title}
              </h6>
            </button>

            {isExpanded && (
              <ul className="teaser-listing__sort-dropdown margin-bottom-0 margin-top-10">
                {sortOptions.map((option, i) => (
                  <li
                    key={`option--${i}`}
                    onClick={() =>
                      this.setState({
                        sortValue: option,
                        isExpanded: false,
                      })
                    }
                  >
                    {option.title}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
        <div className="teaser-listing__list">
          {surveys.dashboard.map((item, index) => (
            <a
              href={item.url}
              className="teaser-listing__item card margin-bottom-10"
              key={`teaser-listing-item-${index}`}
            >
              <div className="col-10">
                <h4 className="teaser-listing__item-title">
                  {item.title}
                </h4>
                <p className="teaser-listing__item-description margin-top-0">
                  {item.description}
                </p>
              </div>
              <div className="col-2 teaser-listing__item-date">
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

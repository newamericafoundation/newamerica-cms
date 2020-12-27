import './TeaserListing.scss';
import React, { Component } from 'react';
import { differenceInMonths } from 'date-fns/esm';
import { format } from 'date-fns';

class TeaserListing extends Component {
  constructor(props) {
    super(props);
  }
  state = {
    isExanded: false,
    sortBy: {},
    sortOptions: [
      { title: 'Most Recent', value: 'recent' },
      { title: 'Title (A-Z)', value: 'desc' },
      { title: 'Title (Z-A)', value: 'asc' },
    ],
  };
  componentDidMount() {
    this.setState({ sortBy: this.state.sortOptions[0] });
    const _data = this.props.data.sort((a, b) =>
      new Date(a.year, a.month) < new Date(b.year, b.month) ? 1 : -1
    );
    this.setState({ data: _data });
  }
  render() {
    const { checkedValues } = this.props;
    const { isExpanded, sortBy, sortOptions } = this.state;

    let _data = this.props.data;

    _data = this.props.data
      .filter((val) => {
        const tags = val['tags'];

        const exists =
          Object.values(checkedValues.tags).some((key) =>
            tags.some((tag) => tag.title === key)
          ) || checkedValues.tags.length === 0;

        if (exists) {
          return true;
        } else {
          return false;
        }
      })
      .filter((val) => {
        const demos = val['demos_key'];

        const exists =
          Object.values(checkedValues.demos).some((key) =>
            demos.some((demo) => demo.title === key)
          ) || checkedValues.demos.length === 0;

        if (exists) {
          return true;
        } else {
          return false;
        }
      })
      .filter((val) => {
        const orgs = val['org'];
        const exists =
          Object.values(checkedValues.orgs).some((key) =>
            orgs.some((org) => org.title === key)
          ) || checkedValues.orgs.length === 0;

        if (exists) {
          return true;
        } else {
          return false;
        }
      })
      .filter((val) => {
        const monthDiff = differenceInMonths(
          new Date(),
          new Date(val['year'], val['month'], 0)
        );

        const maxMonths = checkedValues.dateRange.length
          ? Math.max(...checkedValues.dateRange)
          : 0;

        if (checkedValues.dateRange.length === 0) {
          return true;
        }

        if (maxMonths === 36 && monthDiff >= 36) {
          return true;
        } else if (maxMonths === 0 || monthDiff <= maxMonths) {
          return true;
        }

        return false;
      })
      .filter((val) => {
        const num = +val['sample_number'];
        const size = checkedValues.sizeRange;

        if (size.length === 0) {
          return true;
        }

        if (size.includes('one')) {
          return num <= 1000;
        }
        if (size.includes('two')) {
          return num >= 1000 && num <= 5000;
        }
        if (size.includes('three')) {
          return num >= 5000 && num <= 10000;
        }
        if (size.includes('four')) {
          return num >= 10000;
        }
        return false;
      })
      .filter((val) => {
        const type = val['data_type'].map((el) => el.toLowerCase());

        const exists = type.some((item) =>
          checkedValues.dataType.includes(item)
        );

        if (
          checkedValues.dataType.length === 0 ||
          checkedValues.dataType.includes('mixed') ||
          exists
        ) {
          return true;
        }

        return false;
      })
      .filter((val) => {
        const type = val['national'];
        const selection = checkedValues.national;

        if (
          selection.represented === selection.notRepresented ||
          selection.represented === type
        ) {
          return true;
        }

        return false;
      })
      .sort((a, b) => {
        if (sortBy.value === 'asc') {
          return b.title.localeCompare(a.title);
        } else if (sortBy.value === 'desc') {
          return a.title.localeCompare(b.title);
        } else {
          return new Date(a.year, a.month) < new Date(b.year, b.month)
            ? 1
            : -1;
        }
      });

    return (
      <div className="teaser-listing">
        <div className="teaser-listing__header">
          <h3 className="margin-0">{_data.length} Results</h3>
          <div className="teaser-listing__sort-wrapper">
            <button
              className="teaser-listing__sort"
              onClick={() =>
                this.setState({ isExpanded: !isExpanded })
              }
            >
              <h6 className="with-caret--down margin-0">
                Sort by {sortBy.title}
              </h6>
            </button>

            {isExpanded && (
              <ul className="teaser-listing__sort-dropdown margin-bottom-0 margin-top-10">
                {sortOptions.map((option, i) => (
                  <li
                    key={`option--${i}`}
                    onClick={() =>
                      this.setState({
                        sortBy: option,
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
          {_data.map((item, index) => (
            <a
              href={item.url}
              className="teaser-listing__item card margin-bottom-10"
              key={`teaser-listing-item-${index}`}
            >
              <div className="col-9">
                <h4 className="teaser-listing__item-title">
                  {item.title}
                </h4>
                {item.description && (
                  <p className="teaser-listing__item-description">
                    {item.description}
                  </p>
                )}
              </div>
              <div className="col-3 teaser-listing__item-date">
                {format(
                  new Date(item.year, item.month, 1),
                  item.month ? 'MMM yyyy' : 'yyy'
                )}
              </div>
            </a>
          ))}
        </div>
      </div>
    );
  }
}

export default TeaserListing;

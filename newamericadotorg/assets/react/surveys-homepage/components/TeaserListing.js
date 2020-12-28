import './TeaserListing.scss';
import React, { Component } from 'react';
import { differenceInMonths } from 'date-fns/esm';
import { format } from 'date-fns';
import { LoadingDots } from '../../components/Icons';

class TeaserListing extends Component {
  constructor(props) {
    super(props);
    this.loadMore = this.loadMore.bind(this);
  }
  state = {
    isExanded: false,
    sortBy: {},
    maxRange: 20,
    isLoading: false,
    sortOptions: [
      { title: 'Most Recent', value: 'recent' },
      { title: 'Title (A-Z)', value: 'desc' },
      { title: 'Title (Z-A)', value: 'asc' },
    ],
  };
  componentDidMount() {
    this.setState({ sortBy: this.state.sortOptions[0] });
  }
  loadMore = () => {
    this.setState(
      {
        isLoading: true,
      },
      () => {
        setTimeout(() => {
          this.setState({
            isLoading: false,
            maxRange: this.state.maxRange + 20,
          });
        }, 750);
      }
    );
  };
  render() {
    const { checkedValues, searchTerm } = this.props;
    const { isExpanded, sortBy, sortOptions, maxRange } = this.state;

    let _data = this.props.data;

    _data = this.props.data
      .filter((val) => {
        const surveyTags = val['tags'];
        const checkedTags = Object.keys(checkedValues.tags).filter(
          (key) => checkedValues.tags[key] === true
        );
        const exists = Object.values(checkedTags).some((key) =>
          surveyTags.some((tag) => tag.title === key)
        );

        if (exists || checkedTags.length === 0) {
          return true;
        }
        return false;
      })
      .filter((val) => {
        const surveyDemos = val['demos_key'];
        const checkedDemos = Object.keys(checkedValues.demos).filter(
          (key) => checkedValues.demos[key] === true
        );

        const exists = Object.values(checkedDemos).some((key) =>
          surveyDemos.some((demo) => demo.title === key)
        );

        if (exists || checkedDemos.length === 0) {
          return true;
        }
        return false;
      })
      .filter((val) => {
        const surveyOrgs = val['org'];
        const checkedOrgs = Object.keys(checkedValues.orgs).filter(
          (key) => checkedValues.orgs[key] === true
        );
        const exists = Object.values(checkedOrgs).some((key) =>
          surveyOrgs.some((org) => org.title === key)
        );

        if (exists || checkedOrgs.length === 0) {
          return true;
        }
        return false;
      })
      .filter((val) => {
        const { dateRange } = checkedValues;
        const monthDiff = differenceInMonths(
          new Date(),
          new Date(val['year'], val['month'], 0)
        );

        const unfilter = Object.keys(dateRange).every(function (k) {
          return dateRange[k] === false;
        });

        if ((dateRange.five && monthDiff >= 36) || unfilter) {
          return true;
        }

        if (dateRange.dateFour) {
          return monthDiff <= 24;
        }
        if (dateRange.dateThree) {
          return monthDiff <= 12;
        }
        if (dateRange.dateTwo) {
          return monthDiff <= 6;
        }

        if (dateRange.dateOne) {
          return monthDiff <= 3;
        }

        return false;
      })
      .filter((val) => {
        const num = +val['sample_number'];
        const { sizeRange } = checkedValues;
        const unfilter = Object.keys(sizeRange).every(function (k) {
          return sizeRange[k] === false;
        });

        if ((sizeRange.sizeFour && num >= 10000) || unfilter) {
          return true;
        }
        if (sizeRange.sizeOne && sizeRange.sizeTwo) {
          return num < 5000;
        }

        if (sizeRange.sizeTwo && sizeRange.sizeThree) {
          return num < 10000;
        }

        if (sizeRange.sizeOne) {
          return num <= 1000;
        }
        if (sizeRange.sizeTwo) {
          return num >= 1000 && num <= 5000;
        }
        if (sizeRange.sizeThree) {
          return num >= 5000 && num <= 10000;
        }

        return false;
      })
      .filter((val) => {
        const type = val['data_type'].map((el) => el.toLowerCase());
        const checkedType = Object.keys(
          checkedValues.dataType
        ).filter((key) => checkedValues.dataType[key] === true);

        const exists = type.some((item) =>
          checkedType.includes(item)
        );

        if (exists || checkedType.length === 0) {
          return true;
        }

        if (checkedType.includes('mixed') && type.length > 1) {
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

    // Search filtering
    if (searchTerm !== '') {
      _data = _data.filter((row) => {
        const columns = Object.keys(row).filter((item) => {
          if (
            item === 'title' ||
            item === 'description' ||
            item === 'year' ||
            item === 'month'
          ) {
            return true;
          }
          return false;
        });

        return columns.some(
          (column) =>
            typeof row[column] === 'string' &&
            row[column]
              .toLowerCase()
              .includes(searchTerm.toLowerCase())
        );
      });
    }

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
          {_data.slice(0, maxRange).map((item, index) => (
            <a
              href={item.url_path
                .split('/')
                .filter((item) => item !== 'new-america')
                .join('/')}
              className="teaser-listing__item card margin-bottom-10"
              key={`teaser-listing-item-${index}`}
              target="_blank"
            >
              <div className="col-sm-9">
                <h4 className="teaser-listing__item-title">
                  {item.title}
                </h4>
                {item.description && (
                  <div
                    className="teaser-listing__item-description"
                    dangerouslySetInnerHTML={{
                      __html: item.description,
                    }}
                  />
                )}
              </div>
              <div className="col-sm-3 teaser-listing__item-date">
                {format(
                  new Date(item.year, item.month, 1),
                  item.month ? 'MMM yyyy' : 'yyy'
                )}
              </div>
            </a>
          ))}
          {this.state.maxRange <= _data.length && (
            <div className="teaser-listing__load-more">
              <button className="button" onClick={this.loadMore}>
                {this.state.isLoading ? <LoadingDots /> : 'Load more'}
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }
}

export default TeaserListing;

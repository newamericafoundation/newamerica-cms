import './Search.scss';
import React from 'react';

class Search extends React.Component {
  constructor(props) {
    super(props);
  }
  handleSearchInput = (e) => {
    this.props.handleSearchInput(e.target.value.toLowerCase());
  };
  render() {
    return (
      <div className="survey-search__wrapper">
        <h3 className="survey-search__label">{this.props.title}</h3>
        <div className="survey-search input">
          <div className="search-icon">
            <span className="glass"></span>
            <span className="handle"></span>
          </div>
          <input
            type="text"
            id="surveys-search-input"
            placeholder="Enter keyword or phrase..."
            onChange={this.handleSearchInput}
          />
        </div>
      </div>
    );
  }
}

export default Search;

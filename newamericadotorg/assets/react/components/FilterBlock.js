import './FilterBlock.scss';
import React, { Component } from 'react';

class FilterBlock extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    const { props } = this.props;
    console.log(props);
    return (
      <div>
        <h3>Filter Block</h3>
      </div>
    );
  }
}

export default FilterBlock;

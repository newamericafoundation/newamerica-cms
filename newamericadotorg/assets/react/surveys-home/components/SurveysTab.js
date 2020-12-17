import './SurveysTab.scss';
import React, { Component } from 'react';

class SurveysTab extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    const { props } = this.props;
    console.log(props);
    return (
      <div>
        <h3>Surveys Tab</h3>
      </div>
    );
  }
}

export default SurveysTab;

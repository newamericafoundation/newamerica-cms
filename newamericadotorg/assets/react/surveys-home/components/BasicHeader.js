import './BasicHeader.scss';
import React, { Component } from 'react';

class BasicHeader extends Component {
  render() {
    let { report } = this.props;

    return (
      <React.Fragment>
        <div className="basic-header">
          <div className="basic-header__breadcrumb">
            {report.programs.map((program, i) => (
              <h6
                className="link margin-0 with-caret--left"
                key={`program-${i}`}
              >
                <a href={program.url}>{program.name}</a>
              </h6>
            ))}
          </div>
          <div className="basic-header__content">
            <h1 className="basic-header__title margin-0 promo">
              {report.title || 'HigherEd Polling Dashboard'}
            </h1>
            <h6 className="basic-header__subtitle margin-top-25 margin-bottom-0">
              {report.subheading ||
                'A collection of reports, insights, and analyses exploring topics within Higher Education. Created for Researchers, Journalists, and the general public who have an interest understanding public opinion on Higher Education issues.'}
            </h6>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default BasicHeader;

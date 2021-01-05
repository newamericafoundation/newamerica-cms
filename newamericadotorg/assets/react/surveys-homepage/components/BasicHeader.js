import './BasicHeader.scss';
import React from 'react';

const BasicHeader = (props) => {
  const { data } = props;
  return (
    <div className="basic-header">
      <div className="basic-header__breadcrumb">
        <h6 className="link margin-0 with-caret--left">
          <a href="/education-policy">Education Policy</a>
        </h6>
      </div>
      <div className="basic-header__content">
        <h1 className="basic-header__title margin-0 promo">
          {data.title || 'HigherEd Polling Dashboard'}
        </h1>
        <h6 className="basic-header__subtitle margin-top-25 margin-bottom-0">
          {data.survey_home_page.subheading}
        </h6>
      </div>
    </div>
  );
};
export default BasicHeader;

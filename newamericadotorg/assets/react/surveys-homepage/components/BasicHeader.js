import './BasicHeader.scss';
import React from 'react';

const BasicHeader = (props) => {
  const { data } = props;

  return (
    <div className="basic-header">
      <div className="basic-header__breadcrumb">
        <h6 className="link margin-0 with-caret--left">
          <a href={data.parent.url}>
            {data.parent.title}
          </a>
        </h6>
      </div>
      <div className="basic-header__content">
        <h1 className="basic-header__title margin-0 promo">
          {data.title}
        </h1>
        <h6 className="basic-header__subtitle margin-top-25 margin-bottom-0">
          {data.subheading}
        </h6>
      </div>
    </div>
  );
};
export default BasicHeader;

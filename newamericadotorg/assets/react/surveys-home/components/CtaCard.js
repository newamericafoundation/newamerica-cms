import './CtaCard.scss';
import React from 'react';

const CtaCArd = (props) => {
  return (
    <div className={`cta-card cta-card--${props.type}`}>
      <div className="col--1">
        <h4 className="margin-0">Call for Submissions</h4>
        <p className="">
          Know of a poll or report that should be added to our list?
        </p>
      </div>
      <div className="col--2">
        {props.email ? (
          <a href={`mailto:${props.url}`}>{props.linkText}</a>
        ) : (
          <a href={props.url}>{props.linkText}</a>
        )}
      </div>
    </div>
  );
};

export default CtaCArd;

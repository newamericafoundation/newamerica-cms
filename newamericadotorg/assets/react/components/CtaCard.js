import './CtaCard.scss';
import React from 'react';

const CtaCArd = (props) => {
  return (
    <div className={`cta-card cta-card--${props.type}`}>
      <div className="col--1">
        <h4 className="margin-0">{props.title}</h4>
        <p className="">{props.description}</p>
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

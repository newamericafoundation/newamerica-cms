import './CtaCard.scss';
import React from 'react';

const CtaCard = (props) => {
  return (
    <div className={`cta-card cta-card--${props.type}`}>
      <div className="col--1">
        <h4 className="margin-0">{props.title}</h4>
        <p className="">{props.description}</p>
      </div>
      <div className="col--2">
        {props.type === 'email' ? (
          <a href={`mailto:${props.url}`}>{props.linkText}</a>
        ) : (
          <a href={props.url} target="_blank">
            {props.linkText}
          </a>
        )}
      </div>
    </div>
  );
};

export default CtaCard;

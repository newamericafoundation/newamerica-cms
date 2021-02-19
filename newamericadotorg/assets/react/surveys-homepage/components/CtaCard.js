import './CtaCard.scss';
import React from 'react';

const CtaCard = (props) => {
  return (
    <div className={`cta-card cta-card--${props.type}`}>
      <div>
        <h4 className="margin-0">{props.title}</h4>
        <p className="">{props.description}</p>
      </div>
      {props.type === 'email' ? (
        <a href={`mailto:${props.url}`}>{props.linkText}</a>
      ) : (
        <a href={props.url} target="_blank" className="button">
          {props.linkText}
        </a>
        )}
    </div>
  );
};

export default CtaCard;

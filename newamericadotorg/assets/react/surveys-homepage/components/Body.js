import './Body.scss';
import React from 'react';

const Body = (props) => {
  return (
    <div className="body-section">
      <h2 className="body-section__title">{props.title}</h2>
      <div
        className="body-section__description"
        dangerouslySetInnerHTML={{
          __html: props.body,
        }}
      />
      {props.children}
    </div>
  );
};

export default Body;

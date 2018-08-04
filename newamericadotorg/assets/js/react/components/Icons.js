import React from 'react';

export const Arrow = ({ direction, ...props }) => (
  <div className={`icon-arrow ${direction}`} {...props}>
    <div />
    <div />
    <div />
  </div>
);

export const Doc = (props) => (
  <div className={`icon-doc`} {...props}>
    <div />
    <div />
    <div />
    <div />
    <div />
  </div>
);

export const PlusX = ({x, white, ...props}) => (
  <div className={`icon-plus${x ? ' x' : ''}${white ? ' white' : ''}`} {...props}>
    <div />
    <div />
  </div>
);

export const LoadingDots = ({ color='black' }) => (
  <h5 className={`loading-dots centered ${color} block`}>
    <span>.</span><span>.</span><span>.</span>
  </h5>
);

export const Search = () => (
  <div className="search-icon">
    <span className="glass"></span>
    <span className="handle"></span>
  </div>
);

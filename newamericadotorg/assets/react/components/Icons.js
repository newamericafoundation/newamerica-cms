import './Icons.scss';

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

export const PlusX = ({x, white, large, ...props}) => (
  <div className={`icon-plus${x ? ' x' : ''}${white ? ' white' : ''}${ large ? ' lg' : ''}`} {...props}>
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

export const DataViz = ({ className, ...props }) => (
  <i className={`na-icon na-icon-data-viz ${className || ''}`} {...props}>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 9"><title>icon_data_viz</title><g id="Layer_2" data-name="Layer 2"><g id="Layer_1-2" data-name="Layer 1"><path d="M2,9H0V0H2ZM5.33,2h-2V9h2ZM8.67,0h-2V9h2ZM12,4.8H10V9h2Z"/></g></g></svg>
  </i>
);

export const Download = ({ className, ...props }) => (
  <i className={`na-icon na-icon-download ${className || ''}`} {...props}>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12"><title>icon_download</title><g id="Layer_2" data-name="Layer 2"><g id="Layer_1-2" data-name="Layer 1"><path d="M10.24,4.21,6,8.45,1.76,4.21,3.17,2.79,5,4.62V0H7V4.62L8.83,2.79ZM12,8H10v2H2V8H0v4H12Z"/></g></g></svg>
  </i>
);

export const Highlight = ({ className, ...props }) => (
  <i className={`na-icon na-icon-highlight ${className || ''}`} {...props}>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12"><title>icon_highlight</title><g id="Layer_2" data-name="Layer 2"><g id="Layer_1-2" data-name="Layer 1"><path d="M0,5l.29.28h0L2.84,7.74a.14.14,0,0,1,0,.06L2.73,12l3.6-1.89h.06l3.9,1.56-.8-4.33a.07.07,0,0,1,0-.06l2.49-3L8,3.75a.07.07,0,0,1,0,0L5.84,0,4.44,3.14l-.25.63a.12.12,0,0,1-.05,0l-1.46.37Z"/></g></g></svg>
  </i>
);

export const Report = ({ className, ...props }) => (
  <i className={`na-icon na-icon-report ${className || ''}`} {...props}>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 26"><title>icon_report_1</title><g id="Layer_2" data-name="Layer 2"><g id="Layer_1-2" data-name="Layer 1"><path d="M22,2V24H2V2H22m2-2H0V26H24V0ZM19,11H5v2H19Zm0-4H5V9H19Zm0,8H5v2H19Zm-3.5,4H5v2H15.5Z"/></g></g></svg>
  </i>
);

export const Resource = ({ className, ...props }) => (
  <i className={`na-icon na-icon-resource ${className || ''}`} {...props}>
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 11.7"><title>icon_resource</title><g id="Layer_2" data-name="Layer 2"><g id="Layer_1-2" data-name="Layer 1"><path d="M10.67,5.78A4.62,4.62,0,0,0,10.26,4l1.06-.84L9.89,1.32l-1.07.85a4.8,4.8,0,0,0-1.67-.81V0H4.85V1.36a4.72,4.72,0,0,0-1.67.81L2.11,1.32.68,3.12,1.74,4a4.66,4.66,0,0,0-.42,1.82L0,6.09.51,8.33,1.85,8A4.64,4.64,0,0,0,3,9.47L2.41,10.7l2.07,1,.59-1.22a4.73,4.73,0,0,0,.93.1,4.92,4.92,0,0,0,.94-.1l.58,1.22,2.07-1L9,9.46A4.75,4.75,0,0,0,10.15,8l1.34.3L12,6.08ZM6,7.81A1.92,1.92,0,1,1,7.91,5.89,1.92,1.92,0,0,1,6,7.81Z"/></g></g></svg>
  </i>
);

import React from 'react';

const Tab = (props) => {
  return (
    <li className="na-tabs__nav-item">
      <h5 className="link">
        <a
          className={`na-tabs__nav-link ${
            props.isActive ? 'active' : ''
          }`}
          onClick={() => props.onClick(props.tabIndex)}
        >
          {props.title}
        </a>
      </h5>
    </li>
  );
};

export default Tab;

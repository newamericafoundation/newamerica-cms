import React, { Component } from 'react';
class Tab extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <li className="na-tabs__nav-item">
        <h5 className="link">
          <a
            className={`na-tabs__nav-link ${
              this.props.isActive ? 'active' : ''
            }`}
            onClick={() => this.props.onClick(this.props.tabIndex)}
          >
            {this.props.title}
          </a>
        </h5>
      </li>
    );
  }
}

export default Tab;

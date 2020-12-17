import './Tabs.scss';
import React, { Component } from 'react';

class Tabs extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeTabIndex: 0,
    };
    this.handleTabClick = this.handleTabClick.bind(this);
  }

  handleTabClick(tabIndex) {
    tabIndex === this.state.activeTabIndex
      ? this.state.activeTabIndex
      : tabIndex;

    this.setState({
      activeTabIndex: tabIndex,
    });
  }

  renderNavTabs() {
    return React.Children.map(this.props.children, (child, index) => {
      return React.cloneElement(child, {
        onClick: this.handleTabClick,
        tabIndex: index,
        isActive: index === this.state.activeTabIndex,
      });
    });
  }

  setActiveTabContent() {
    const { children } = this.props;
    const { activeTabIndex } = this.state;
    if (children[activeTabIndex]) {
      return children[activeTabIndex].props.children;
    }
  }

  render() {
    return (
      <div className="na-tabs margin-top-10">
        <ul className="na-tabs__nav inline">
          {this.renderNavTabs()}
        </ul>
        <div className="na-tabs__active-content margin-top-35">
          {this.setActiveTabContent()}
        </div>
      </div>
    );
  }
}

export default Tabs;

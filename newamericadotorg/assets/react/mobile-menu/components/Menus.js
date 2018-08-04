import './Menus.scss';

import React, { Component } from 'react';
import { Response } from '../../components/API';
import { connect } from 'react-redux';
import Heading from './Heading';
import { PrimaryTab, SecondaryTab } from './Tabs';

class Menus extends Component {
  constructor(props) {
    super(props);
    this.state = { selectedTab: false };
  }

  componentDidUpdate(prevProps){
    if(this.props.isOpen !== prevProps.isOpen && this.props.isOpen === false) this.setState({ selectedTab: false });
  }

  switchTab = (selectedTab) => {
      this.setState({ selectedTab });
  }

  render() {
    let { isOpen } = this.props;
    let { selectedTab } = this.state;
    return(
      <div className={`mobile-menu ${selectedTab ? `secondary-tab-active ${selectedTab.toLowerCase()}-tab-open` : ''} ${isOpen ? 'open' : ''}`}>
        <Heading selectedTab={selectedTab} switchTab={this.switchTab} />
        <div className="mobile-menu__tabs-wrapper">
          <PrimaryTab switchTab={this.switchTab} />
          <SecondaryTab />
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  isOpen: state.site.mobileMenuIsOpen
});

export default Menus = connect(mapStateToProps)(Menus);

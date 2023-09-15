import React, { Component } from 'react';
import { createPortal } from 'react-dom';
import { Overlay } from '../report/components/OverlayMenu';
import { HomeSubscribe } from '../home-panels/pages/Subscribe';

import { connect } from 'react-redux';

const NAME = 'homeSubscribe';
const ID = 'home-subscribe';

class APP extends Component {
  state = {
    open: false
  }

  fixBody = () => {
    const top = window.pageYOffset;
    document.body.style.overflow = 'hidden';
    document.body.style.position = 'fixed';
    document.body.style.top = -top + 'px';
  };

  unfixBody = () => {
    document.body.style.overflow = 'auto';
    document.body.style.position = 'static';
    if (document.body.style.top)
      window.scrollTo(0, -document.body.style.top.replace('px', ''));

    document.body.style.top = null;
  };

  closeModal = () => {
    this.unfixBody();
    this.setState({open: false});
  }

  openModal = () => {
    this.fixBody();
    this.setState({open: true});
  }

  render() {
    let { programs, home_subscriptions } = JSON.parse(this.props.meta);
    return (
      <>
        <button onClick={this.openModal} className="button">Subscribe</button>

        {this.state.open && createPortal(
          <Overlay
            title="Subscribe"
            open={this.state.open}
            close={this.closeModal}
          ><HomeSubscribe programs={programs} subscriptions={home_subscriptions} dispatch={this.props.dispatch} /></Overlay>,
          document.body
        )}
      </>
    );
  }
}

APP = connect()(APP);

export default { APP, NAME, ID };

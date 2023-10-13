import React, { Component } from 'react';
import { createPortal } from 'react-dom';
import { Overlay } from '../report/components/OverlayMenu';
import Subscribe from '../program-page/components/Subscribe';

import { connect } from 'react-redux';

const NAME = 'subscribePage';
const ID = 'subscribe-page';

class APP extends Component {
  render() {
    let subscriptions = JSON.parse(this.props.subscriptions);
    return (<Subscribe subscriptions={subscriptions} />);
  }
}

APP = connect()(APP);

export default { APP, NAME, ID };

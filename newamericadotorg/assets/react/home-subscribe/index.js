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
    let allSubscriptions = home_subscriptions;
    programs.forEach(program => {
      let programSubscriptions = (program.subscriptions || []).map(subscription => {
        // On the site-wide subscription component, all non-site-wide
        // lists should be unchecked by default.
        let temp = Object.assign({}, subscription);
        temp.checked_by_default = false;
        return temp;
      });

      allSubscriptions = allSubscriptions.concat(programSubscriptions);
    });
    return (
      <div className="container">
			<a className="homepage__promo-link" onClick={this.openModal}>
				<h1 className="promo margin-0">
					<div className="block">
						<span><em>Stay in touch</em></span>
					</div>
				</h1>
				<h3 className="margin-top-35 margin-bottom-0">
					<div className="block">
						<span><em>Be the first to hear about the latest events and research from New America.</em></span>
					</div>
				</h3>
        <span className="button margin-top-35">Subscribe</span>
			</a>
      {this.state.open && createPortal(
        <Overlay
          title="Subscribe"
          open={this.state.open}
          close={this.closeModal}
        ><HomeSubscribe
           programs={programs}
           homeSubscriptions={home_subscriptions}
           subscriptions={allSubscriptions}
           dispatch={this.props.dispatch}
         />
        </Overlay>,
        document.body
      )}
		</div>
    );
  }
}

APP = connect()(APP);

export default { APP, NAME, ID };

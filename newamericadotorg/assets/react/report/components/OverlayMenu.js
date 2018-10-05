import './OverlayMenu.scss';

import React, { Component } from 'react';
import ContentMenu from './ContentMenu';
import { PlusX } from '../../components/Icons';

export default class OverlayMenu extends Component {

  constructor(props){
    super(props);
    this.state = {
      open: true
    }
  }


  expand = (title) => {


  }

  render(){
    let { children, open, closeMenu, openMenu, contentsPosition, hideAttachments } = this.props;
    return (
      <React.Fragment>
        <div className={`report__grey-out ${open ? 'active' : ''}`} onClick={closeMenu}/>
        <div className={`report__overlay ${open ? 'open' : ''}`}>
          <div className="report__overlay__top-bar">
            <h3 className="margin-0">Contents</h3>
            <PlusX onClick={closeMenu} x={true} large={true} />
          </div>
          <div className="report__overlay__menu-wrapper">
            <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '65px 0' }}>
              {children}
            </div>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

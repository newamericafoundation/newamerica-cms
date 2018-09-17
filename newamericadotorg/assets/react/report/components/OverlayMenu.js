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
        {/* <div className="menu-button" >
          <div onClick={() => { hideAttachments(); openMenu(); }}>
            <i className="fa fa-bars" />
            <h5 className="margin-0">
              <span style={{ transform: `translateX(${contentsPosition})`}}>
                Contents
              </span>
            </h5>
          </div>
        </div> */}
        <div className={`report__grey-out ${open ? 'active' : ''}`} onClick={closeMenu}/>
        <div className={`report__overlay ${open ? 'open' : ''}`}>
          {/* <div className="report__overlay__header">

          </div> */}
          <PlusX onClick={closeMenu} x={true} large={true} />
          <div className="report__overlay__menu-wrapper">
            <h3 className="margin-bottom-35">Contents</h3>
            {children}
          </div>
        </div>
      </React.Fragment>
    );
  }
}

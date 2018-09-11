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
    let { children, open, closeMenu } = this.props;
    return (
      <React.Fragment>
        <div className={`report__grey-out ${open ? 'active' : ''}`} onClick={closeMenu}/>
        <div className={`report__overlay ${open ? 'open' : ''}`}>
          <div className="report__overlay__header">
            <PlusX onClick={closeMenu} x={true} large={true} />
          </div>
          <div className="report__overlay__menu-wrapper">
            {children}
          </div>
        </div>
      </React.Fragment>
    );
  }
}

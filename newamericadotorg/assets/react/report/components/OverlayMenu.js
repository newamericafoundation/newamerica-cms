import './OverlayMenu.scss';

import React, { Component } from 'react';
import ContentMenu from './ContentMenu';
import { PlusX } from '../../components/Icons';


export const Overlay = ({ close, open, children, title }) => (
  <React.Fragment>
    <div className={`report__grey-out ${open ? 'active' : ''}`} onClick={close}/>
    <div className={`report__overlay ${open ? 'open' : ''}`}>
      <div className="report__overlay__top-bar">
        <div className="report__overlay__top-bar__content" style={{ margin: '0 auto', maxWidth: '970px' }}>
          <h3 className="margin-0">{title}</h3>
          <PlusX onClick={close} x={true} large={true} />
        </div>
      </div>
      <div className="report__overlay__scroll-wrapper">
        <div style={{ maxWidth: '970px', margin: '0 auto', paddingBottom: '140px' }}>
          {children}
        </div>
      </div>
    </div>
  </React.Fragment>
);

import './TopNav.scss';

import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import ContentMenu from './ContentMenu';

class TopNav extends Component {
  render(){
    let { section, report, openMenu, closeMenu, toggleMenu, menuOpen, showAttachments } = this.props;
    let next = report.sections[section.number],
        previous = report.sections[section.number-2];
    return (
      <div className="report__top-nav">
        <div className="container">
          <div className="row">
            <div className="col-4 col-md-3 col-lg-2 report__top-nav__left">
              <a href="/"><div className="logo white" /></a>
            </div>
            <div className="col-8 col-md-9 col-lg-10 report__top-nav__right">
              <h4 className="white margin-0 report__top-nav__title">
                <Link to={report.url} onClick={closeMenu}>{report.title}</Link>
              </h4>
              {report.attachments.length > 0 &&
              <div className="report__top-nav__icon attch" onClick={() => {
                closeMenu();
                showAttachments();
              }}>
                <i className="fa fa-paperclip circle gray" data-attachments-n={`${report.attachments.length}`}/>
              </div>
              }
              <div className="report__top-nav__icon">
                <i className="fa fa-twitter circle gray" style={{ marginRight: '20px' }}/>
                <i className="fa fa-facebook circle gray" />
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default TopNav;

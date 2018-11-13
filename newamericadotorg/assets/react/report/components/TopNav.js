import './TopNav.scss';

import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import ContentMenu from './ContentMenu';

import { Download } from '../../components/Icons';

class TopNav extends Component {
  render(){
    let { section, report, openMenu, closeMenu, toggleMenu, menuOpen, showAttachments, attchClicked } = this.props;
    let next = report.sections[section.number],
        previous = report.sections[section.number-2];
        console.log(location)
    return (
      <div className="report__top-nav scroll-target" data-scroll-offset="200%">
        <div className="report__top-nav__sticky-wrapper">
        <div className="container">
          <div className="row">
            <div className="col-6 col-md-3 col-lg-2 report__top-nav__left">
              <a href="/"><div className="logo white" /></a>
            </div>
            <div className="col-6 col-md-9 col-lg-10 report__top-nav__right">
              <h4 className="white margin-0 report__top-nav__title" style={{ opacity: section ? 1 : 0 }}>
                <Link to={report.url} onClick={closeMenu} className="ga-track-click" data-action="click_top_nav" data-label="report" data-value="back_to_home">
                  {report.title}
                </Link>
              </h4>
              {report.attachments.length > 0 &&
              <div className={`report__top-nav__icon attch ga-track-click ${attchClicked ? 'clicked' : ''}`} onClick={() => {
                closeMenu();
                showAttachments();
              }} data-action="click_top_nav" data-label="report" data-value="open_downloads">
                <Download data-attachments-n={`${report.attachments.length}`} className="circle-gray"/>
                {!section && <h6 className="inline margin-0 white">Download</h6>}
              </div>
              }
              <div className="report__top-nav__icon">
                <a href={`https://twitter.com/intent/tweet/?url=${'https://' + location.host + report.url}&text=${report.title}&via=newamerica`} className="ga-track-click" data-action="click_social" data-label="report" data-value="twitter">
                  <i className="fa fa-twitter circle gray ga-track-click" style={{ marginRight: '20px' }} />
                </a>
                <a href={`https://www.facebook.com/dialog/share?app_id=1650004735115559&display=popup&href=${'https://' + location.host + report.url}`} className="ga-track-click" data-action="click_social" data-label="report" data-value="facebook">
                  <i className="fa fa-facebook circle gray"/>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
    )
  }
}

export default TopNav;

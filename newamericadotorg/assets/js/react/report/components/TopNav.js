import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import ContentMenu from './ContentMenu';

class TopNav extends Component {
  render(){
    let { section, report, openMenu, closeMenu, toggleMenu, menuOpen } = this.props;
    let next = report.sections[section.number],
        previous = report.sections[section.number-2];
    return (
      <div className="report__top-nav scroll-target" data-scroll-offset="200%">
        <div className="report__top-nav__sticky-wrapper">
        <div className="container">
          <div className={`row gutter-45${menuOpen ? ' menu-open' : ''}`}>
            <div className="report__top-nav__contents col-5 col-md-2">
              <div className={`report__top-nav__contents__menu-wrapper`}>
                <div className="report__top-nav__contents__button" onClick={toggleMenu}>
                  <a className={`button--text border-0 white with-caret--${menuOpen ? 'up' : 'down' }`}>Contents</a>
                </div>
                <ContentMenu {...this.props} activeSection={section}/>
              </div>
          </div>
            <div className="report__top-nav__title col-7 col-md-10">
              <div className="report__top-nav__title__wrapper">
                <h4 className="white margin-0">{report.title}</h4>
                <h6 className="white margin-0 report__top-nav__title__chapter">{` (${section.title})`}</h6>
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

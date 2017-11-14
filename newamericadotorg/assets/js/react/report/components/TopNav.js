import { Component } from 'react';
import { Link } from 'react-router-dom';
import ContentMenu from './ContentMenu';

class TopNav extends Component {
  state = { openMenu: false }

  toggleMenu = () => {
    this.setState({ openMenu: !this.state.openMenu });
  }

  render(){
    let { section, report } = this.props;
    let next = report.sections[section.number],
        previous = report.sections[section.number-2];
    return (
      <div className="report__top-nav scroll-target" data-scroll-offset="200%">
        <div className="report__top-nav__sticky-wrapper">
        <div className="container no-padding">
          <div className="row gutter-45">
            <div className={"report__top-nav__contents col-2 "}>
              <div className={`report__top-nav__contents__menu-wrapper${this.state.openMenu ? ' open' : ''}`}>
                <div className="report__top-nav__contents__button" onClick={this.toggleMenu}>
                  <a className="button--text white with-caret">Contents</a>
                </div>
                <ContentMenu report={report} open={this.state.openMenu} closeMenu={this.toggleMenu} activeSection={section}/>
              </div>
          </div>
            <div className="report__top-nav__title col-10">
              <label className="bold white margin-0">{report.title}</label>
              <label className="white margin-0 report__top-nav__title__chapter">{` (${section.title})`}</label>
            </div>
          </div>
        </div>
        </div>
      </div>
    )
  }
}

export default TopNav;

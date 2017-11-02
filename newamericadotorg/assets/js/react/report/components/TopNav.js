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
          <div className="row no-gutters">
            <div className="report__top-nav__contents col-1">
              <ContentMenu report={report} open={this.state.openMenu} closeMenu={this.toggleMenu} activeSection={section}/>
              <div className="report__top-nav__contents__button" onClick={this.toggleMenu}>
                <i className="fa fa-bars"></i><label>Contents</label>
              </div>
            </div>
            <div className="report__top-nav__title col-auto">
              <label className="bold white">{report.title}</label>
              <label className="white report__top-nav__title__chapter">{` (${section.title})`}</label>
            </div>
            <div className="report__top-nav__arrows col-1">
              <div className={`previous ${previous ? '' : 'inactive'}`}>
                {previous &&
                <Link to={`${report.url}${previous.slug}`}>
                  <i className="fa fa-long-arrow-left" />
                </Link>}
                {!previous &&
                  <i className="fa fa-long-arrow-left" />}
              </div>
              <div className={`next ${next ? '' : 'inactive'}`}>
                {next &&
                <Link to={`${report.url}${next.slug}`}>
                  <i className="fa fa-long-arrow-right" />
                </Link>}
                {!next &&
                  <i className="fa fa-long-arrow-right" />}
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

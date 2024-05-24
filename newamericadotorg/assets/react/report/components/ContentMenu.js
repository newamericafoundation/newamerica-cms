import './ContentMenu.scss';

import { Link } from 'react-router-dom';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { PlusX, Home } from '../../components/Icons';
import { Overlay } from './OverlayMenu';

const Subsection = ({ section, url, closeMenu, action, preview }) => (
  <div className="report__menu__subsection">
    <h6 className="margin-0">
      <Link to={preview ? `/preview${section.url}` : section.url} onClick={closeMenu} className="ga-track-click" data-action={action} data-label="report" data-value="click_menu_subsection">
        {section.title}
      </Link>
    </h6>
  </div>
);

const InteractiveDiv = () => (
  <div className="interactive-div">
    <i className="fa fa-hand-pointer" />
    <div className="interactive-div__text">
      <h6 className="inline">View the interactive graphic in this section!</h6>
    </div>
  </div>
);

const DownArrow = () => (
  <div className="down-arrow-icon-circle">

  </div>
)

const Section = ({ section, expanded, expand, closeMenu, home, action, preview }) => (
    <div className={`report__menu__section ${expanded ? 'expanded' : ''}`}>
      <div className="report__menu__section__title row gutter-0">
        <div className="col-11">
          <Link to={preview ? `/preview${section.url}` : section.url} onClick={closeMenu} className="ga-track-click" data-action={action} data-label="report" data-value="click_menu_section">
            {section.interactive && <InteractiveDiv /> }
            {home && <div className="home-div">
              <Home />
            </div>}
            <h4 className="inline-block margin-0">{section.title}</h4>
          </Link>
        </div>
        <div className="col-1" onClick={() => expand(section.slug) } style={{ background: '#fff', paddingRight: '25px' }}>
          {section.subsections.length > 0 && <div className="icon-plus-wrapper"><PlusX /></div>}
        </div>
      </div>
      {section.subsections.length > 0 &&
        <div className="report__menu__section__subsections" style={
          { maxHeight: expanded ? (section.subsections.length * 100) + 'px' : 0 }
        }>
          {section.subsections.map((s,i)=>(
            <Subsection preview={preview} section={s} key={`sub-${i}`} closeMenu={closeMenu} action={action}/>
          ))}
        </div>
      }
    </div>
);


class ContentMenu extends Component {

  constructor(props){
    super(props);
    this.state = {
      expanded: [],
      lastScrollPosition: 0
    }
  }


  expand = (title) => {
    let i = this.state.expanded.indexOf(title);

    if(i === -1) {
      this.setState({
        expanded: [...this.state.expanded, title]
      });
    } else {
      let expanded = [...this.state.expanded];
      expanded.splice(i,1)
      this.setState({ expanded });
    }

  }

  goTo = (e, title) => {
    let expanded = {};
    this.props.report.sections.map((s)=>{
      expanded[s.title] = s.title == title;
    });
    this.setState({ expanded });
    this.props.closeMenu();
  }

  render(){
    let { report: { url, sections, title }, activeSection, closeMenu, showHome, open, preview } = this.props;

    return (
      <div className="report__content-menu">
        {showHome &&
          <Section preview={preview} closeMenu={closeMenu} home={true} section={{ url, title, slug: '', subsections: [] }} landing={false}/>
        }
        {sections.map((s,i)=>(
          <Section section={s}
            preview={preview}
            landing={showHome ? 'click_menu' : 'click_landing'}
            key={`section-${i}`}
            expand={this.expand}
            expanded={this.state.expanded.indexOf(s.slug) !== -1}
            closeMenu={closeMenu}/>
        ))}
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  windowScrollPosition: state.site.scroll.position
});

export default connect(mapStateToProps)(ContentMenu);

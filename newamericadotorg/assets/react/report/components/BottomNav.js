import './BottomNav.scss';

import { Link } from 'react-router-dom';
import React, { Component } from 'react';

import { Home } from '../../components/Icons';

const Tooltip = ({ content, activeIndex }) => (
  <div className="report__bottom-nav__tooltip" style={{ opacity: content ? 1 : 0, visibility: content ? 'visible' : 'hidden' }}>
    <h6 className="paragraph white margin-0">{content.title}</h6>
    <div className="report__bottom-nav__tooltip__caret" style={{ left: (content.index - activeIndex + 1) * 40 + 10 }}></div>
  </div>
);

class BottomNavButtons extends Component {
  render(){
    let { section, report } = this.props;
    if(!section) section = { number: 0 };
    let next = report.sections[section.number],
        previous = report.sections[section.number-2];

    return (
      <div className="report__bottom-nav">
        <div className="container">
        {previous &&
          <div className="report__bottom-nav__button previous">
            <Link to={`${report.url}${previous.slug}/`} className="button with-caret--left">Prev. Section</Link>
          </div>
        }
        {section.number === 1 &&
          <div className="report__bottom-nav__button previous">
            <Link to={`${report.url}`} className="button with-caret--left">Home</Link>
          </div>
        }
        {next &&
          <div className="report__bottom-nav__button next">
            <Link to={`${report.url}${next.slug}/`} className="button with-caret--right">Next Section</Link>
          </div>
        }
        </div>
      </div>
    );
  }
}

const ChapterList = ({ sections, activeIndex, n, reportUrl, tooltipContent, setTooltip }) => (
  <ul style={{ transform: `translateX(-${activeIndex * 40}px)`, position: 'relative' }}>
    <li className={n === 0 ? 'active' : ''}
      style={{ width: '40px', textAlign: 'center', lineHeight: '36px' }}>
      <Link to={reportUrl}>
        <Home />
      </Link>
    </li>
    {sections.map((s,i) => (
      <li className={n === i ? 'active' : ''} key={`section-${i}`}
        style={{ width: '40px', textAlign: 'center' }}
        onMouseEnter={()=>{ setTooltip({
          title: s.title, index: i
        })} }
        onMouseLeave={()=>{ setTooltip(false)}}>
        <Link to={s.url} style={{ display: 'block' }}>
          <h6 className="inline">{i+1}</h6>
        </Link>
      </li>
    ))}
  </ul>
)

class BottomNav extends Component {
  constructor(props){
    super(props);
    this.state = {
      tooltipContent: false
    }
  }

  setTooltip = (content) => {
    this.setState({ tooltipContent: content });
  }

  render(){
    let { section, report, hideAttachments, openMenu } = this.props;
    let next = report.sections[section.number],
        previous = report.sections[section.number-2];

    let activeIndex = 0;

    if(section.number < 3){
      activeIndex = 0;
    } else {
      activeIndex = section.number-3;
    }

    return (
      <div className="report__bottom-nav-bar">
        <div className="report__bottom-nav-bar__menu" onClick={() => { hideAttachments(); openMenu(); }}>
          <i className="fa fa-bars"/>
          <h6 className="inline">Contents</h6>
        </div>
        <div className="report__bottom-nav-bar__chapter-nav" style={{ position: 'relative' }}>
          <Tooltip content={this.state.tooltipContent} activeIndex={activeIndex}/>
          <div className="report__bottom-nav-bar__button-wrapper" style={{ marginRight: '15px' }}>
            {section.number > 1 &&
              <Link to={report.sections[section.number-2].url} className="prev-button">
                <h6 className="margin-0">Prev. Section</h6>
              </Link>
              }
            {section.number === 1 &&
              <Link to={report.url} className="prev-button">
                <h6 className="margin-0">Prev. Section</h6>
              </Link>
            }
          </div>
          <div style={{ overflow: 'hidden', width: '240px', }} className="report__bottom-nav-bar__chapter-list">

            <ChapterList
              sections={report.sections}
              reportUrl={report.url}
              setTooltip={this.setTooltip}
              tooltipContent={this.state.tooltipContent}
              activeIndex={activeIndex}
              n={section.number-1}/>
          </div>
          <div className={`report__bottom-nav-bar__button-wrapper next`} style={{ marginLeft: '15px' }}>
            {section.number < report.sections.length &&
              <Link to={report.sections[section.number].url} className="next-button">
                <h6 className="margin-0">Next Section</h6>
              </Link>
              }
          </div>
        </div>
      </div>
    );
  }
}

export default BottomNav;

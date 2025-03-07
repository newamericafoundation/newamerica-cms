import './Body.scss';

import React, { Component } from 'react';
import { connect } from 'react-redux';
import ReactDOM from 'react-dom';
import Endnote from './EndnoteAside';

class Body extends Component {
  constructor(props) {
    super(props);
    this.state = {
      endnote: null,
      top: 0,
      citeEl: null
    };
  }

  openEndnote = endnote => {
    let body = this;

    return function() {
      if (this.querySelector('.report__citation').classList.contains('active'))
        return body.closeEndnote();
      body.closeEndnote();
      this.querySelector('.report__citation').classList.add('active');
      body.setState({
        endnote,
        top:
          window.pageYOffset +
          this.getBoundingClientRect().top -
          body.el.offsetTop,
        citeEl: this
      });
    };
  };

  citationEvents = () => {
    let _this = this;
    this.closeEndnote();
    let endnotes = _this.props.report.endnotes;
    let citations = document.querySelectorAll('.report__citation-wrapper');
    this.props.dispatch({
      type: 'ADD_SCROLL_EVENT',
      component: 'site',
      eventObject: {
        selector: '.report__citation-wrapper',
        onLeave: (el, dir) => {
          if (this.state.citeEl === el) this.closeEndnote();
        },
        els: citations,
        // viewHeight
        topOffset: -Math.max(
          document.documentElement.clientHeight,
          window.innerHeight || 0
        ),
        bottomOffset: -65
      }
    });
    for (let c of citations) {
      let i = c.getAttribute('data-citation-number') - 1;
      c.onclick = this.openEndnote(endnotes[i]);
    }
  };

  closeEndnote = el => {
    if (this.state.citeEl)
      this.state.citeEl
        .querySelector('.report__citation')
        .classList.remove('active');
    this.setState({ endnote: null, top: -1000, citeEl: null });
  };

  loadScripts = () => {
    let { report, section } = this.props;
    newamericadotorg.renderDataViz();
  };

  componentDidMount() {
    this.citationEvents();
    if (this.props.section) this.loadScripts();
  }

  componentDidUpdate(prevProps) {
    if (
      prevProps.section.number != this.props.section.number &&
      this.props.section
    ) {
      this.citationEvents();
      this.loadScripts();
      this.props.dispatch({
        type: 'RELOAD_SCROLL_EVENTS',
        component: 'SITE'
      });
    }
  }

  render() {
    let { section, report } = this.props;
    let { endnotes, date, url, report_pdf, title } = report;
    let { endnote, top } = this.state;
    return (
      <div
        className={`container ${endnote ? 'endnote-active' : ''}`}
        ref={el => {
          this.el = el;
        }}
        style={{ position: 'relative' }}
      >
        <Endnote endnote={endnote} top={top} close={this.closeEndnote} />
        <div
          className={`report__body${section.hide_title ? ' hide-title' : ''}`}
        >
          <div className="post-body-wrapper">
            <h1 className="margin-top-0 report__body__section-title">
              {section.title}
            </h1>
            <div
              className="report__body__article"
              dangerouslySetInnerHTML={{ __html: section.body }}
            />
          </div>
        </div>
      </div>
    );
  }
}

export default Body;

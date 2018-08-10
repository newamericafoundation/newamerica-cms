import './Body.scss';

import React, { Component } from 'react';
import Social from './Social';
import Authors from './Authors'
import Endnote from './EndnoteAside';
import { format as formatDate } from 'date-fns';

class Body extends Component {
  constructor(props){
    super(props);
    this.state = {
      endnote: null, top: 0, citeEl: null
    };
  }

  openEndnote = () => {
    let _this = this;

    return function(){
      let endnotes = _this.props.report.endnotes;
      let number = +this.getAttribute('data-citation-number');
      if(_this.state.citeEl==this){
        _this.closeEndnote();
      } else {
        if(_this.state.citeEl)
          _this.state.citeEl.classList.remove('active');
        this.classList.add('active');
        _this.setState({ endnote: endnotes[number-1], top: this.offsetTop, citeEl: this });
      }
    }
  }

  citationEvents = () => {
    let _this = this;
    let citations = document.querySelectorAll('.report__citation');
    this.props.dispatch({
      type: 'ADD_SCROLL_EVENT',
      component: 'site',
      eventObject: {
        selector: '.report__citation',
        onLeave: (el, dir) => {if(this.state.citeEl==el) this.closeEndnote();},
        els: citations,
        // viewHeight
        topOffset: -Math.max(document.documentElement.clientHeight, window.innerHeight || 0),
        bottomOffset: -65
      }
    });
    for(let c of citations){
      c.onclick = this.openEndnote()
    }
  }

  closeEndnote = () => {
    if(this.state.citeEl)
      this.state.citeEl.classList.remove('active');
    this.setState({ endnote: null, top: -1000, citeEl: null });
  }

  renderDataViz = (tries=0) => {
    let viz = document.querySelectorAll('.na-dataviz');
    if(!viz) return;
    if(!window.renderDataViz){
      if(tries<3) setTimeout(()=>{ this.renderDataViz(tries++); }, 500);
      return;
    }
    for(let i=0; i<viz.length; i++){
      window.renderDataViz(viz[i]);
    }
  }

  loadScripts = () => {
    let { report, section } = this.props;
    this.renderDataViz();
    if(!this.el) return;
    if(report.data_project_external_script && document.querySelectorAll('.dataviz-project').length){

      const dataScript = document.createElement("script");

      dataScript.src = `https://na-data-projects.s3.amazonaws.com/projects/${report.data_project_external_script}`;
      dataScript.async = true;

      this.el.appendChild(dataScript);
    }
    let scripts = section.body.match(/<script.*?src="(.*?)"/);
    if(scripts){
      const script = document.createElement("script");

      script.src = scripts[1];
      script.async = true;

      this.el.appendChild(script);
    }
  }

  componentDidMount(){
    this.citationEvents();
    this.loadScripts();
  }

  componentDidUpdate(prevProps){
    if(prevProps.location != this.props.location){
      this.citationEvents();
      this.closeEndnote();
      this.loadScripts();
    }

  }

  render(){
    let { section, report, closeMenu } = this.props;
    let { authors, endnotes, date, url, report_pdf, title } = report;
    let { endnote, top } = this.state;
    return (
      <div className="container margin-top-35 margin-top-lg-80" onClick={closeMenu} ref={(el)=>{this.el = el; }}>
      <div className={"report__body row gutter-30 " + (endnote ? 'endnote-active' : '')}>
        <div className="report__body__aside col-11 col-md-6 col-lg-2 push-lg-10">
          <div className="post-aside-wrapper">
            <Authors authors={authors} />
          </div>
        </div>
        <div className={"report__body__aside col-6 col-md-6 col-lg-2 pull-lg-2"}>
          <div className="post-aside-wrapper">
            <Social url={url} report_pdf={report_pdf} title={title}/>
            <Endnote endnote={endnote} top={top} close={this.closeEndnote}/>
          </div>
        </div>
        <div className="report__body__section col-12 col-lg-8 pull-lg-2 margin-top-35 margin-top-lg-0">
          <div className="post-body-wrapper">
            {section.number==1 && <h6 className="report__body__section__date margin-top-0 margin-bottom-35">Published on {formatDate(date, "MMM. DD, YYYY")}</h6>}
            <h2 className="margin-top-0">{section.title}</h2>
            <article className="report__body__section__article" dangerouslySetInnerHTML={{__html: section.body}} />
          </div>
        </div>
      </div>
      </div>
    );
  }
}

export default Body;

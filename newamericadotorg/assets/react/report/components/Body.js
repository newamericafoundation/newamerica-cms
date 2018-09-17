import './Body.scss';

import React, { Component } from 'react';
import ReactDOM from 'react-dom';
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

  openEndnote = (el) => {
    let _this = this;

    return function(){
      this.parentNode.classList.toggle('active');
    }
  }

  citationEvents = () => {
    let _this = this;
    let endnotes = _this.props.report.endnotes;
    let citations = document.querySelectorAll('.report__citation-wrapper');
    // this.props.dispatch({
    //   type: 'ADD_SCROLL_EVENT',
    //   component: 'site',
    //   eventObject: {
    //     selector: '.report__citation-wrapper',
    //     onLeave: (el, dir) => {if(this.state.citeEl==el) this.closeEndnote();},
    //     els: citations,
    //     // viewHeight
    //     topOffset: -Math.max(document.documentElement.clientHeight, window.innerHeight || 0),
    //     bottomOffset: -65
    //   }
    // });
    for(let c of citations){
      let i = c.getAttribute('data-citation-number')-1;
      ReactDOM.render(<Endnote endnote={endnotes[i]} top={top} close={() => this.closeEndnote(c)}/>, c.querySelector('.report__citation__note'));
      c.querySelector('.report__citation').onclick = this.openEndnote();
    }
  }

  closeEndnote = (el) => {
    el.classList.remove('active');
  //  this.setState({ endnote: null, top: -1000, citeEl: null });
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
    if(prevProps.section.number != this.props.section.number){
      this.citationEvents();
      this.loadScripts();
    }

  }

  render(){
    let { section, report, closeMenu } = this.props;
    let { authors, endnotes, date, url, report_pdf, title } = report;
    let { endnote, top } = this.state;
    return (
      <div className={`container ${endnote ? 'endnote-active' : ''}`} onClick={closeMenu} ref={(el)=>{this.el = el; }} style={{ position: 'relative' }}>
        <div className="report__body">
          <div className="post-body-wrapper">
            {section.number==1 && <h6 className="report__body__section__date margin-top-0 margin-bottom-35">Published on {formatDate(date, "MMM. DD, YYYY")}</h6>}
            <h2 className="margin-top-0">{section.title}</h2>
            <div className="report__body__article" dangerouslySetInnerHTML={{__html: section.body}} />
          </div>
        </div>

      </div>
    );
  }
}

export default Body;

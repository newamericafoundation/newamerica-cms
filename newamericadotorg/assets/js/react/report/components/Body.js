import { Component } from 'react';
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
      let endnotes = _this.props.endnotes;
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
        enterOffset: -Math.max(document.documentElement.clientHeight, window.innerHeight || 0),
        leaveOffset: -65
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

  componentDidMount(){
    this.citationEvents();
  }

  componentDidUpdate(prevProps){
    if(prevProps.location != this.props.location){
      this.citationEvents();
      this.closeEndnote();
    }

  }

  render(){
    let { section, authors, endnotes, date, url } = this.props;
    let { endnote, top } = this.state;
    return (
      <div className={"report__body row gutter-45 margin-top-35 margin-top-lg-80 " + (endnote ? 'endnote-active' : '')}>
        <div className="report__body__right-aside col-11 col-md-5 col-lg-2 offset-md-1 offset-lg-0p5 offset-xl-1">
          <Authors authors={authors} />
          <Endnote endnote={endnote} top={top} close={this.closeEndnote}/>
        </div>
        <div className={"report__body__left-aside col-6 col-md-5 col-lg-2 push-lg-7 push-xl-6"}>
          <Social url={url}/>
        </div>
        <div className="report__body__section col-12 col-md-10 col-lg-7 col-xl-6 pull-lg-2 offset-md-1 offset-lg-0 margin-top-35 margin-top-lg-0">
          {section.number==1 && <label className="block report__body__section__date margin-bottom-35">Published on {formatDate(date, "MMM. DD, YYYY")}</label>}
          <h2 className="margin-top-0">{`${section.number}. ${section.title}`}</h2>
          <article className="report__body__section__article" dangerouslySetInnerHTML={{__html: section.body}} />
        </div>
      </div>
    );
  }
}

// right authors

// <div className={"report__body row gutter-45 margin-top-35 margin-top-lg-80 " + (endnote ? 'endnote-active' : '')}>
//   <div className="report__body__right-aside col-11 col-md-5 col-lg-2 col-xl-2 push-lg-9 offset-md-1 offset-lg-0p5 offset-xl-0">
//     <Authors authors={authors} />
//   </div>
//   <div className={"report__body__left-aside col-6 col-md-5 col-lg-2 pull-lg-2 offset-xl-1"}>
//     <Social url={url}/>
//     <Endnote endnote={endnote} top={top} close={this.closeEndnote}/>
//   </div>
//   <div className="report__body__section col-12 col-md-10 col-lg-7 col-xl-6 pull-lg-2 offset-md-1 offset-lg-0 margin-top-35 margin-top-lg-0">
//     {section.number==1 && <label className="block report__body__section__date margin-bottom-35">Published on {formatDate(date, "MMM. DD, YYYY")}</label>}
//     <h2 className="margin-top-0">{`${section.number}. ${section.title}`}</h2>
//     <article className="report__body__section__article" dangerouslySetInnerHTML={{__html: section.body}} />
//   </div>
// </div>




export default Body;

import { Component } from 'react';
import Social from './Social';
import Authors from './Authors'
import Endnote from './EndnoteAside';
import { format as formatDate } from 'date-fns';

class Body extends Component {
  constructor(props){
    super(props);
    this.state = {
      endnote: null, top: 0
    };
  }

  openEndnote = () => {
    let _this = this;

    return function(){
      let endnotes = _this.props.endnotes;
      let number = +this.getAttribute('data-citation-number');
      if(_this.state.endnote)
        _this.closeEndnote();
      else
        _this.setState({ endnote: endnotes[number-1], top: this.offsetTop });
    }
  }

  citationEvents = () => {
    let _this = this;
    let citations = document.querySelectorAll('.report__citation');
    let isMobile = window.innerWidth < 860;
    for(let c of citations){
      if(isMobile){
        c.onclick = this.openEndnote()
      } else {
        c.onmouseenter = this.openEndnote();
        c.onmouseleave = function(){
          _this.closeEndnote();
        }
      }
    }
  }

  closeEndnote = () => {
    this.setState({ endnote: null, top: -250 });
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
    let { section, authors, endnotes, date } = this.props;
    let { endnote, top } = this.state;
    return (
      <div className="report__body row gutter-45">
        <div className={"report__body__left-aside col-12 col-lg-2 offset-0 offset-xl-1 " + (endnote ? 'endnote-active' : '')}>
          <Social />
          <Endnote endnote={endnote} top={top} close={this.closeEndnote}/>
        </div>
        <div className="report__body__right-aside col-12 col-lg-2 push-lg-8 push-xl-6">
          <Authors authors={authors} />
        </div>
        <div className="report__body__section col-12 col-lg-8 col-xl-6 pull-lg-2">
          {section.number==1 && <label className="block report__body__section__date">Published on {formatDate(date, "MMM. DD, YYYY")}</label>}
          <h1 className="no-top-margin">{`${section.number}. ${section.title}`}</h1>
          <div dangerouslySetInnerHTML={{__html: section.body}} />
        </div>
      </div>
    );
  }
}

export default Body;

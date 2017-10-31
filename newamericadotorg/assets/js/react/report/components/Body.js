import { Component } from 'react';
import Social from './Social';
import Authors from './Authors'
import Endnote from './EndnoteAside';

class Body extends Component {
  constructor(props){
    super(props);
    this.state = {
      endnote: null, top: 0
    };
  }

  citationEvents = () => {
    let _this = this;
    let citations = document.querySelectorAll('.report__citation');
    for(let c of citations){
      c.onmouseenter = function(){
        let endnotes = _this.props.endnotes;
        let number = +this.getAttribute('data-citation-number');
        _this.setState({ endnote: endnotes[number-1], top: this.offsetTop });
      }
      c.onmouseleave = function(){
        _this.setState({ endnote: null, top: 0 });
      }
    }
  }

  componentDidMount(){
    this.citationEvents();
  }

  componentDidUpdate(){
    this.citationEvents();
  }

  render(){
    let { section, authors, endnotes } = this.props;
    let { endnote, top } = this.state;
    return (
      <div className="report__body row gutter-45">
        <div className={"report__body__left-aside col-12 col-lg-2 offset-0 offset-xl-1 " + (endnote ? 'endnote-active' : '')}>
          <Social />
          <Endnote endnote={endnote} top={top}/>
        </div>
        <div className="report__body__right-aside col-12 col-lg-2 push-lg-8 push-xl-6">
          <Authors authors={authors} />
        </div>
        <div className="report__body__section col-12 col-lg-8 col-xl-6 pull-lg-2">
          <h1 className="no-top-margin">{`${section.number}. ${section.title}`}</h1>
          <div dangerouslySetInnerHTML={{__html: section.body}} />
        </div>
      </div>
    );
  }
}

export default Body;

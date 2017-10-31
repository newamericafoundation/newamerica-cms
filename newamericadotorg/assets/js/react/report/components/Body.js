import { Component } from 'react';
import Social from './Social';
import Authors from './Authors'

class Body extends Component {
  render(){
    let { section, authors } = this.props;
    return (
      <div className="report__body row gutter-45">
        <div className="report__body__left-aside col-2 offset-0 offset-lg-1">
          <Social />
        </div>
        <div className="report__body__section col-6">
          <h1 className="no-top-margin">{`${section.number}. ${section.title}`}</h1>
          <div dangerouslySetInnerHTML={{__html: section.body}} />
        </div>
        <div className="report__body__right-aside col-2">
          <Authors authors={authors} />
        </div>
      </div>
    );
  }
}

export default Body;

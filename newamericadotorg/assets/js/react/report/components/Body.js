import { Component } from 'react';

class Body extends Component {
  render(){
    let { section } = this.props;
    return (
      <div className="report row gutter-45">
        <div className="report__left-aside col-2 offset-0 offset-lg-1"></div>
        <div className="report__body col-6" dangerouslySetInnerHTML={{__html: section.body}}>

        </div>
      </div>
    );
  }
}

export default Body;

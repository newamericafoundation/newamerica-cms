import { Component } from 'react';

export default class Section extends Component {

  render(){
    let { section } = this.props;

    return (
      <div className="in-depth-section">
        <h1>{section.title}</h1>
      </div>
    );
  }
}

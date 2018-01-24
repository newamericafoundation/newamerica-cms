import { Component } from 'react';

export default class About extends Component {
  componentWillMount(){
    if(window.scrollY > 300){
      window.scrollTo(0, 0);
    }
  }
  render(){
    let { about } = this.props;

    return (
      <div className="program__about margin-top-10">
        <div className="program__about__body post-body" dangerouslySetInnerHTML={{__html: about}} />
      </div>
    );
  }
}

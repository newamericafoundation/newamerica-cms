import { Component } from 'react';


export default class StoryGrid extends Component {

  render(){
    let { story_grid } = this.props;
    return (
      <div className="program__story-grid" dangerouslySetInnerHTML={{__html: story_grid }}/>
    );
  }
}

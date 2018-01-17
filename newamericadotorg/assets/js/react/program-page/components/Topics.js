import { Link, BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import { Component } from 'react';
import { Fetch } from  '../../components/API';

export class Topic extends Component {

  render(){
    return(
      <div className="program__topics__topic"></div>
    );
  }
}

export class TopicsList extends Component {

  render(){
    let { program } = this.props;
    return (
      <div className="program__topics">
        {program.topics.map((topic,i)=>(
          <h2 className="margin-25"><Link to={topic.url}>{topic.title}</Link></h2>
        ))}
      </div>
    );
  }
}

import { Link } from 'react-router-dom';
import { Component } from 'react';
import { Fetch } from '../../components/API';
import { NAME } from '../constants';
import Breadcrumbs from './Breadcrumbs';
import TopicDetails from './TopicDetails';
import TopicContent from './TopicContent';

class Topic extends Component {
render(){
    let { topic, ancestors } = this.props;
    return (
      <div>
        <Breadcrumbs topic={topic} ancestors={ancestors} />
        <TopicDetails topic={topic}/>
        <TopicContent topic={topic} />
      </div>
    );
  }
}

export default Topic;

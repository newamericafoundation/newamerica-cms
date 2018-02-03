import { Component } from 'react';
import { ImageAside, Reel, Body } from '../components';


export default class OurStory extends Component {

  render(){
    let { response: { results : { data } } } = this.props;
    return (
      <div className="home__panels__content">
        <ImageAside data={data.our_community} grayscale={true}/>
        <Reel data={data.our_vision} interval={3000} />
        <Body data={data.our_work} />
      </div>
    );
  }
}

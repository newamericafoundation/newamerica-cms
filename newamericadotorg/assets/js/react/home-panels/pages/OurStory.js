import React, { Component } from 'react';
import ImageAside from '../components/ImageAside';
import Reel from '../components/Reel';
import Body from '../components/Body';


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

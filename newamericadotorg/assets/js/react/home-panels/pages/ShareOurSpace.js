import { Component } from 'react';
import { ImageAside, Reel, Body } from '../components';


export default class ShareOurSpace extends Component {

  render(){
    let { response: { results : { data } } } = this.props;
    return (
      <div className="home__panels__content">
        <ImageAside data={data.partnerships} />
        <Reel data={data.amenities} setHTML={true} interval={7000} panelName="share-our-space"/>
        <ImageAside data={data.host} />
      </div>
    );
  }
}

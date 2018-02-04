import { Component } from 'react';
import { ImageAside, Reel, Body } from '../components';


export default class Jobs extends Component {

  render(){
    let { response: { results : { data } } } = this.props;
    //let frame = data.job_board.iframe[0]
    return (
      <div className="home__panels__content">
        <Body data={data.job_board} />
      </div>
    );
  }
}

import React, { Component } from 'react';
import { Body } from '../components';


export default class PressRoom extends Component {

  render(){
    let { response: { results : { data } } } = this.props;
    return (
      <div className="home__panels__content">
        <Body data={data.general_info} />
      </div>
    );
  }
}

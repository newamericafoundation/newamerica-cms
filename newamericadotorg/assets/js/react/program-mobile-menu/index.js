import React, { Component } from 'react';
import { Response } from '../components/API';
import { NAME, ID } from './constants';
import Menu from './components';

class APP extends Component {
  render(){
    return (
      <Response name="program.detail" component={Menu}/>
    );
  }
}

export default { NAME, ID, APP };

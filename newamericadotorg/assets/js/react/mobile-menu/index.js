import { Component } from 'react';
import { NAME, ID } from './constants';
import Menus from './components/Menus';


class APP extends Component {
  render(){
    return (
      <Menus />
    );
  }
}

export default { NAME, ID, APP };

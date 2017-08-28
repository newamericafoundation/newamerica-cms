import { Component } from 'react';
import { NAME, ID } from './constants';
import Tabs from './components/Tabs';


class APP extends Component {
  render(){
    return (
      <div>
        <Tabs />
      </div>
    );
  }
}


export default { NAME, ID, APP };

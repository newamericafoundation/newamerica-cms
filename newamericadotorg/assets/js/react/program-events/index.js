import { NAME, ID } from './constants';
import { Events } from './components';
import React, { Component } from 'react';
import PropTypes from 'prop-types';

class APP extends Component {
  static propTypes = {
    programId: PropTypes.string,
    contentType: PropTypes.string
  }

  render(){
    return(
      <Events {...this.props} />
    );
  }
}

export default { NAME, ID, APP };

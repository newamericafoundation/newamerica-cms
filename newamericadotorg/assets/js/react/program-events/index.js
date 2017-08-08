import { NAME, ID } from './constants';
import { Events } from './components';
import { Component } from 'react';
import PropTypes from 'prop-types';

class APP extends Component {
  static propTypes = {
    programId: PropTypes.string
  }

  render(){
    return(
      <Events programId={this.props.programId} />
    );
  }
}

export default { NAME, ID, APP };

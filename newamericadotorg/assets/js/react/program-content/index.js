import { NAME, ID } from './constants';
import { Component } from 'react';
import PropTypes from 'prop-types';
import { Content } from './components';

class APP extends Component {
  static propTypes = {
    programId: PropTypes.string.isRequired
  }

  render() {
    return (
      <Content programId={this.props.programId} />
    );
  }
}

export default { NAME, ID, APP };

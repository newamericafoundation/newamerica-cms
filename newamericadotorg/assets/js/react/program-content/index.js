import { NAME, ID } from './constants';
import { Component } from 'react';
import PropTypes from 'prop-types';
import { Content } from './components';

class APP extends Component {
  static propTypes = {
    programId: PropTypes.string.isRequired,
    contentType: PropTypes.string
  }

  render() {
    return (
      <Content {...this.props} />
    );
  }
}

export default { NAME, ID, APP };

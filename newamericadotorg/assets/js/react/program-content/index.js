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
      <section className="program-content-grid container">
        <Content programId={this.props.programId} />
      </section>
    );
  }
}

export default { NAME, ID, APP };

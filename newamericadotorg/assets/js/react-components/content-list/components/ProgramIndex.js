import { connect } from 'react-redux';
import { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import { NAME } from '../constants';
import Fetch from '../../api/components/Fetch';
import { ProgramRoutes } from './Routes';

class ProgramIndex extends Component {
  render(){
    let { programId, program, match } = this.props;

    return (
      <section className="container--medium content-filters">
          <Fetch name='program' endpoint={`program/${programId}`}
            fetchOnMount={true} />
          {program && <ProgramRoutes program={program}/> }
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  program: state.program ? state.program.results : {}
});

export default connect(mapStateToProps)(ProgramIndex);

import { connect } from 'react-redux';
import { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import { NAME } from '../constants';
import { Fetch } from '../../components/API';
import { SubprogramRoutes } from './Routes';

class SubprogramIndex extends Component {
  render(){
    let { subprogramId, subprogram } = this.props;

    return (
      <section className="content-filters">
          <Fetch name='subprogram' endpoint={`subprogram/${subprogramId}`}
            fetchOnMount={true} />
          {subprogram && <SubprogramRoutes subprogram={subprogram}/>}
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  subprogram: state.subprogram ? state.subprogram.results : {}
});

export default connect(mapStateToProps)(SubprogramIndex);

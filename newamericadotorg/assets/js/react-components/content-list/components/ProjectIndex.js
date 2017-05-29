import { connect } from 'react-redux';
import { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import { NAME } from '../constants';
import Fetch from '../../api/components/Fetch';
import { ProjectRoutes } from './Routes';

class ProjectIndex extends Component {
  render(){
    let { projectId, project } = this.props;

    return (
      <section className="container--medium content-filters">
          <Fetch name='project' endpoint={`project/${projectId}`}
            fetchOnMount={true} />
          {project && <ProjectRoutes project={project}/>}
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  project: state.project ? state.project.results : {}
});

export default connect(mapStateToProps)(ProjectIndex);

import { connect } from 'react-redux';
import { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import { NAME } from '../constants';
import Fetch from '../../api/components/Fetch';
import {
  ProjectContentType as ContentTypeRoute,
  Project as ProjectRoute
} from './Routes';

class ProjectSubRoutes extends Component {
  render(){
    let { projectId, project } = this.props;

    return (
      <section className="container--medium content-filters">
          <Fetch name='project' endpoint='project'
            initialQuery={{id: projectId}} fetchOnMount={true} />
          <Switch>
            <ContentTypeRoute
              path={`${project.url}publications`}
              contentType={{slug: 'publications', api_name:'', name:'Publications', title:'Publications'}}
              project={project}
              projectId={projectId} />
            {project.content_types && project.content_types.map((c,i)=>(
              <ContentTypeRoute
                path={c.url}
                contentType={c}
                project={project}
                projectId={projectId} />
            ))}
          </Switch>
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  project: state.project ? ( state.project.results.length ? state.project.results[0] : {} ) : {}
});

export default connect(mapStateToProps)(ProjectSubRoutes);

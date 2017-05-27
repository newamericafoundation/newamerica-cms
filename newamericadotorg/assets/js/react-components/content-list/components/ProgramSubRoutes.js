import { connect } from 'react-redux';
import { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import { NAME } from '../constants';
import Fetch from '../../api/components/Fetch';
import {
  ProgramContentType as ContentTypeRoute,
  Project as ProjectRoute
} from './Routes';

class ProgramSubRoutes extends Component {
  render(){
    let { programId, program, match } = this.props;

    return (
      <section className="container--medium content-filters">
          <Fetch name='program' endpoint='program'
            initialQuery={{id: programId}} fetchOnMount={true} />
          <Switch>
            <ContentTypeRoute
              path={`/${program.slug}/publications`}
              contentType={{slug: 'publications', api_name:'', name:'Publications', title:'Publications'}}
              program={program}
              programId={programId} />
            {program.content_types && program.content_types.map((c,i)=>(
              <ContentTypeRoute
                path={c.url}
                contentType={c}
                program={program}
                programId={programId} />
            ))}
            {program.projects && program.projects.map((p,i)=>(
              <ProjectRoute path={p.url} projectId={p.id} />
            ))}
          </Switch>
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  program: state.program ? ( state.program.results.length ? state.program.results[0] : {} ) : {}
});

export default connect(mapStateToProps)(ProgramSubRoutes);

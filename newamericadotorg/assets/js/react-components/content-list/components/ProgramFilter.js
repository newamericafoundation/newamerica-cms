import { connect } from 'react-redux';
import { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import { NAME } from '../constants';
import ProjectFilter from './ProjectFilter';
import Fetch from '../../api/components/Fetch';

class ProgramFilter extends Component {
  render(){
    let { programId, program, match } = this.props;

    return (
      <section className="container--medium content-filters">
        {program &&
          <Fetch name='program'
            endpoint='program'
            initialQuery={{id: programId}}
            eager={true}
            fetchOnMount={true} />
          }
          <Switch>
            <Route path={`/${program.slug}/publications`} render={(props)=>(
              <ProjectFilter {...props}
                projectId={new URLSearchParams(props.location.search).get('project_id')}
                programId={programId}
                program={program}
                contentType={{slug: 'publications', api_name:'', name:'Publications', title:'Publications'}} />
            )}/>
          {program.content_types && program.content_types.map((c,j)=>(
            <Route path={c.url} render={(props)=>(
                <ProjectFilter {...props}
                  projectId={new URLSearchParams(props.location.search).get('project_id')}
                  programId={programId}
                  program={program}
                  contentType={c} />
              )}/>
          ))}
          </Switch>
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  program: state.program ? ( state.program.results.length ? state.program.results[0] : {} ) : {}
});

export default connect(mapStateToProps)(ProgramFilter);

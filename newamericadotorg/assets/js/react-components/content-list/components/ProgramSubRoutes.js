import { connect } from 'react-redux';
import { Component } from 'react';
import { Route, Switch } from 'react-router-dom';
import { NAME } from '../constants';
import Fetch from '../../api/components/Fetch';
import {
  ProgramPublicationDefault as PublicationRoute,
  ProgramContentType as ContentTypeRoute
} from './Routes';

class ProgramSubRoutes extends Component {
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
            <PublicationRoute
              path={`/${program.slug}/publications`}
              program={program}
              programId={programId} />
            {program.content_types && program.content_types.map((c,i)=>(
                <ContentTypeRoute
                  path={c.url}
                  contentType={c}
                  program={program}
                  programId={programId} />
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

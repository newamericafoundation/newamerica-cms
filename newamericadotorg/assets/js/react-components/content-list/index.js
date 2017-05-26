import { BrowserRouter, Route, Link, Switch } from 'react-router-dom';
import { Component } from 'react';
import { connect } from 'react-redux';
import SiteFilter from './components/SiteFilter';
import ProgramFilter from './components/ProgramFilter';
import ContentList from './components/ContentList';
import { setFetchingStatus } from '../api/actions';
import { NAME, ID } from './constants';

class App extends Component {
  componentWillMount(){
    this.props.dispatch(setFetchingStatus(NAME, true));
  }
  render() {
    let { contentTypes, programs } = this.props;

    return (
      <BrowserRouter>
        <section className="content-list-wrapper container">
          <Switch>
            <Route path='/publications' render={(props)=>(
              <SiteFilter {...props}
                programId={new URLSearchParams(props.location.search).get('program_id')}
                contentType={{slug: 'publications', api_name:'', name:'Publications'}} />
            )}/>
            {contentTypes.map((c,i)=>(
                <Route path={`/${c.slug}`} render={(props)=>(
                  <SiteFilter {...props}
                    programId={new URLSearchParams(props.location.search).get('program_id')}
                    contentType={c} />
                )}/>
            ))}
            {programs.map((p,i)=>(
              <Route path={`/${p.slug}`} render={(props)=>(
                <ProgramFilter {...props} programId={p.id} />
              )} />
            ))}
          </Switch>
          <ContentList />
        </section>
      </BrowserRouter>
    );
  }
}

const mapStateToProps = (state) => ({
  contentTypes: state.contentTypes.results || [],
  programs: state.programData.results || []
});

const APP = connect(mapStateToProps)(App);

export default {
  NAME, ID, APP
};

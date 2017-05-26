import { BrowserRouter, Route, Switch } from 'react-router-dom';
import { Component } from 'react';
import { connect } from 'react-redux';
import SiteFilter from './components/SiteFilter';
import ProgramFilter from './components/ProgramFilter';
import ContentList from './components/ContentList';
import {
  PublicationDefault as PublicationRoute,
  ContentType as ContentTypeRoute,
  Program as ProgramRoute
} from './components/Routes';
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
            <PublicationRoute path="/publications" />
            {contentTypes.map((c,i)=>(
              <ContentTypeRoute path={`/${c.slug}`} contentType={c} />
            ))}
            {programs.map((p,i)=>(
              <ProgramRoute path={`/${p.slug}`} program={p} />
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

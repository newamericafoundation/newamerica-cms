import { BrowserRouter, Route, Switch } from 'react-router-dom';
import { Component } from 'react';
import { connect } from 'react-redux';
import SiteFilter from './components/SiteFilter';
import ProgramFilter from './components/ProgramFilter';
import ContentList from './components/ContentList';
import { IndexRoutes } from './components/Routes';
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
          <IndexRoutes contentTypes={contentTypes} programs={programs} />
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

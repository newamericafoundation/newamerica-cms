/* DocumentMeta defined in ./components/Nav.js */

import { NAME, ID } from './constants';
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Fetch, Response } from '../components/API';
import { Route, Switch, Redirect, Router } from 'react-router-dom';
import GARouter from '../ga-router';
import Publications from './components/Publications';
import Nav from './components/Nav';
import Heading from './components/Heading';
import About from './components/About';
import Events from './components/Events';
import StoryGrid from './components/StoryGrid';
import People from './components/People';
import Subprograms from './components/Subprograms';
import Subscribe from './components/Subscribe';
import { TopicsList, TopicRoutes } from './components/Topics';
import HorizontalNav from '../components/HorizontalNav';
import { LoadingDots } from '../components/Icons';
import { setResponse } from '../api/actions';
import store from '../store';

class ProgramPage extends Component {
  // only transition images on first load
  state = {
    loaded: false
  }
  componentDidMount(){
    setTimeout(()=>{ this.setState({ 'loaded': true }); }, 1500);
  }

  contentSlugs = () => {
    let { response: { results }} = this.props;

    if(!results.content_types) return '';
    if(results.content_types.length === 0) return '';
    return '|' + results.content_types.map((c)=>(c.slug)).join('|');
  }

  render(){
    let { response: { results }, programType, preview } = this.props;
    let root;
    if(preview) root = `admin/pages/${results.id}/edit/preview`
    else root = programType == 'program' ? ':program' : ':program/:subprogram';

    return (
      <div className="container">
          <div className="program__content">
            <Heading program={results} />
            <Route path={`/${root}/:subpage?`} render={(props)=>(<Nav {...props} program={results} root={root} preview={preview}/>)}/>
            <Route path={`/${root}/`} exact render={()=>(<StoryGrid program={results} loaded={this.state.loaded} story_grid={results.story_grid} />)} />
            {results.about && <Route path={`/${root}/about/`} render={()=>(<About program={results} about={results.about} root={root} />)} /> }
            <Route path={`/${root}/our-people/`} render={(props)=>(<People programType={programType} {...props} program={results} /> )} />
            <Route path={`/${root}/events/`} render={(props)=>(<Events programType={programType} {...props} program={results} /> )} />
            <Route path={`/${root}/projects/`} render={(props)=>(<Subprograms {...props} program={results} /> )} />
            <Route path={`/${root}/(publications${this.contentSlugs()})/`} render={(props)=>(<Publications programType={programType} {...props} program={results} /> )} />
            {(results.topics && !preview) &&
            <Route render={(props)=>(
              <Fetch name={`${NAME}.topics`}
                component={TopicRoutes}
                endpoint={'topic'}
                fetchOnMount={true}
                program={results}
                initialQuery={{
                  program_id: results.id
                }}/>
            )}/>}{(results.topics && preview) &&
              <Route render={(props)=>(
                <Response
                  {...props}
                  name={`${NAME}.topics`}
                  component={TopicRoutes}
                  preview={preview}
                  root={root}
                  program={results}/>
              )}/>
            }{results.topics &&
              <Route path={`/${root}/topics/`} exact render={(props)=>(<TopicsList {...props} program={results} root={root} preview={preview} /> )} />}
            <Route path={`/${root}/subscribe/`} render={(props)=>(<Subscribe {...props} subscriptions={results.subscriptions} /> )} />
          </div>
      </div>
    );
  }
}

const LoadingState = ({ title }) => (
  <div className="container">
    <div className="program__header margin-bottom-10">
      <div className="program__heading__wrapper">
          <h1 className="margin-0 promo">
            {title}
          </h1>
      </div>
    </div>
    <div className="horizontal-nav">
      <ul className="inline"><li><h5>&nbsp;</h5></li></ul>
    </div>
    <div className="margin-top-60">
      <LoadingDots />
    </div>
  </div>
);

class APP extends Component {
  static propTypes = {
    programId: PropTypes.string.isRequired,
    programType: PropTypes.string.isRequired,
    programTitle: PropTypes.string.isRequired
  }

  componentDidMount(){
    if(window.initialState){
      store.dispatch(setResponse(NAME, {
        hasNext: false,
        hasPrevious: false,
        page: 1,
        results: window.initialState
      }));

      let topics = window.initialTopicsState || [];
      topics.forEach((t) => this.replaceTopicUrls(t));

      store.dispatch(setResponse(`${NAME}.topics`, {
        hasNext: false,
        hasPrevious: false,
        page: 1,
        results: topics
      }));
    }
  }

  replaceTopicUrls = (t) => {
    let programUrl = window.initialState.url;
    let programId = window.initialState.id;

    t.url = t.url.replace(programUrl, `/admin/pages/${programId}/edit/preview/`);
    if(t.subtopics){
      t.subtopics.forEach((s) => this.replaceTopicUrls(s));
    }
  }

  render() {
    let { programId, programType, programTitle } = this.props;
    return (
      <GARouter>
        <Switch>
        <Route path={`/admin/pages/${programId}/edit/preview/`} render={(props)=>(
          <Response name={NAME}
            component={ProgramPage}
            {...props}
            programType={programType} preview={true} />
        )}/>
        <Route path="/admin/pages/" render={()=>(
          <Redirect to={`/admin/pages/${programId}/edit/preview/`} />
        )}/>
        <Route path="/" render={()=>(
          <Fetch component={ProgramPage}
            name={NAME}
            loadingState={<LoadingState title={programTitle} />}
            endpoint={`${programType}/${programId}`}
            fetchOnMount={true}
            programType={programType}
          />
        )}/>
        </Switch>
      </GARouter>
    );
  }
}

export default { NAME, ID, APP };

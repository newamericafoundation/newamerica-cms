/* DocumentMeta defined in ./components/Nav.js */

import { NAME, ID } from './constants';
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Fetch } from '../components/API';
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
    let { response: { results }, programType } = this.props;
    let root = programType == 'program' ? ':program' : ':program/:subprogram';

    return (
      <div className="container">
        <GARouter>
          <div className="program__content">
            <Route path="/admin/pages/" render={()=>(
              <Redirect to={results.url} />
            )}/>
            <Heading program={results} />
            <Route path={`/${root}/:subpage?`} render={(props)=>(<Nav {...props} program={results}/>)}/>
            <Route path={`/${root}/`} exact render={()=>(<StoryGrid program={results} loaded={this.state.loaded} story_grid={results.story_grid} />)} />
            {results.about && <Route path={`/${root}/about/`} render={()=>(<About program={results} about={results.about} root={root} />)} /> }
            <Route path={`/${root}/our-people/`} render={(props)=>(<People programType={programType} {...props} program={results} /> )} />
            <Route path={`/${root}/events/`} render={(props)=>(<Events programType={programType} {...props} program={results} /> )} />
            <Route path={`/${root}/projects/`} render={(props)=>(<Subprograms {...props} program={results} /> )} />
            <Route path={`/${root}/(publications${this.contentSlugs()})/`} render={(props)=>(<Publications programType={programType} {...props} program={results} /> )} />
            {results.topics &&
            <Route render={(props)=>(
              <Fetch name={`${NAME}.topics`}
                component={TopicRoutes}
                endpoint={'topic'}
                fetchOnMount={true}
                program={results}
                initialQuery={{
                  program_id: results.id
                }}/>
            )}/>}
            {results.topics &&
              <Route path={`/${root}/topics/`} exact render={(props)=>(<TopicsList {...props} program={results} root={root} /> )} />}
            <Route path={`/${root}/subscribe/`} render={(props)=>(<Subscribe {...props} subscriptions={results.subscriptions} /> )} />
          </div>
        </GARouter>
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

  render() {
    let { programId, programType, programTitle } = this.props;
    return (
      <Fetch component={ProgramPage}
        name={NAME}
        loadingState={<LoadingState title={programTitle} />}
        endpoint={`${programType}/${programId}`}
        fetchOnMount={true}
        programType={programType}
      />
    );
  }
}

export default { NAME, ID, APP };

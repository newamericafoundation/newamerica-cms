import { SIMPLE_NAME as NAME, SIMPLE_ID as ID } from './constants';
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Route, Switch, Redirect, Link } from 'react-router-dom';
import GARouter from '../ga-router';
import DocumentMeta from 'react-document-meta';
import { Fetch, Response } from '../components/API';
import Heading from './components/Heading';
import CardLg from './components/CardLg';
import { Promo } from './components/CardPromo';
import PeopleCarousel from './components/PeopleCarousel';
import About from './components/About';
import Subscribe from './components/Subscribe';
import { setResponse } from '../api/actions'
import store from '../store';

class StoryGrid extends Component {
  state = {
    email: null
  }
  render(){
    let { program, match, programType } = this.props;
    if(match.params.subpage) return null;
    let promos = program.story_grid.pages || [];
    let aboutUrl = program.about ? program.about.url : null;
    let subText = program.subscription_card_text || `Be the first to hear about the latest events and research from ${program.name}`;
    return (
      <DocumentMeta title={program.title} description={program.description}>
        <div className="program__story-grid">
          {promos[0] && <CardLg post={promos[0]} />}
          <Fetch name={`${NAME}.people`}
            endpoint="author"
            component={PeopleCarousel}
            fetchOnMount={true}
            initialQuery={{
              [programType == 'program' ? 'program_id' : 'subprogram_id']: program.id,
              limit: 100
            }}/>
          {promos[1] && <CardLg post={promos[1]} />}
          <Promo title="About" linkTo={aboutUrl}>
            <p>{program.description}</p>
          </Promo>
          {promos[2] && <CardLg post={promos[2]} />}
          {(program.subscriptions && !program.hide_subscription_card) &&
          <Promo title="Subscribe">
            <div className="promo__subscribe">
              <h2>{subText}</h2>
              <form>
                <div className="input">
                  <input type="text" name="email" required onChange={(e)=>{this.setState({email: e.target.value})}} />
                  <label className="input__label" htmlFor="email">
                    <h5 className="margin-0">Email Address</h5>
                  </label>
                  <div className="input__submit ">
                    <Link className="button--text with-caret--right" to={`subscribe/?email=${this.state.email}`}>Go</Link>
                  </div>
                </div>
              </form>
            </div>
          </Promo>}
        </div>
      </DocumentMeta>
    );
  }
}

class ProgramPage extends Component {
  render(){
    let { response: { results }, programType, programId } = this.props;
    let root = programType == 'program' ? ':program' : ':program/:subprogram';
    let promos = results.story_grid || [];
    return (
      <div className="container">
        <GARouter>
          <div className="program__content">
            <Route path="/admin/pages/" render={()=>(
              <Redirect to={results.url} />
            )}/>
            <Heading program={results} />
            {results.about && <Route path={`/${root}/(about|${results.about.slug})/`} render={(props)=>(<About about={results.about} program={results} root={root}/>)} />}
            {results.subscriptions && <Route path={`/${root}/subscribe`} render={(props)=>(<Subscribe subscriptions={results.subscriptions}/>)} />}
            <Route path={`/${root}/:subpage?`} render={(props)=>(<StoryGrid {...props} program={results} />)} />
          </div>
        </GARouter>
      </div>
    );
  }
}

class APP extends Component {
  componentDidMount(){
    if(window.initialState){
      store.dispatch(setResponse(NAME, {
        count: 0,
        page: 1,
        hasNext: false,
        hasPrevious: false,
        results: window.initialState
      }));
    }
  }
  static propTypes = {
    programId: PropTypes.string.isRequired,
    programType: PropTypes.string.isRequired
  }

  render() {
    let { programId, programType } = this.props;
    if(window.initialState) return <Response name={NAME} preview={true} component={ProgramPage} programId={programId} programType={programType}/>

    return (
      <Fetch component={ProgramPage}
        name={NAME}
        endpoint={`${programType}/${programId}`}
        initialQuery={{ 'simple': 'true' }}
        fetchOnMount={true}
        programId={programId}
        programType={programType}
      />
    );
  }
}

export default { NAME, ID, APP };

import { SIMPLE_NAME as NAME, SIMPLE_ID as ID } from './constants';
import { Component } from 'react';
import PropTypes from 'prop-types';
import { Route, Switch, Redirect } from 'react-router-dom';
import GARouter from '../ga-router';
import DocumentMeta from 'react-document-meta';
import { Fetch } from '../components/API';
import Heading from './components/Heading';
import CardLg from './components/CardLg';
import { Promo, PeopleCarousel } from './components/CardPromo';
import About from './components/About';


class StoryGrid extends Component {

  render(){
    let { program, match, programType } = this.props;
    if(match.params.subpage) return null;
    let promos = program.story_grid || [];
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
          <Promo title="About">
            <p>{program.description}</p>
          </Promo>
          {promos[2] && <CardLg post={promos[2]} />}
          <Promo title="Subscribe">
            <div className="promo__subscribe">
              <h2>Be the first to hear about the latest events and research from {program.name}</h2>
              <div className="input">
                <input type="text" required />
                <label className="input__label button--text">Email Address</label>
                <label className="input__submit button--text with-caret--right">Go</label>
              </div>
            </div>
          </Promo>
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
            <Heading program={results} />
            <Route path={`/${root}/about/`} render={(props)=>(<About {...props} program={results} />)} />
            <Route path={`/${root}/:subpage?`} render={(props)=>(<StoryGrid {...props} program={results} />)} />
          </div>
        </GARouter>
      </div>
    );
  }
}

class APP extends Component {
  static propTypes = {
    programId: PropTypes.string.isRequired,
    programType: PropTypes.string.isRequired
  }

  render() {
    let { programId, programType } = this.props;
    return (
      <Fetch component={ProgramPage}
        name={NAME}
        endpoint={`${programType}/${programId}`}
        initialQuery={{ 'image_rendition': 'fill-800x375' }}
        fetchOnMount={true}
        programId={programId}
        programType={programType}
      />
    );
  }
}

export default { NAME, ID, APP };

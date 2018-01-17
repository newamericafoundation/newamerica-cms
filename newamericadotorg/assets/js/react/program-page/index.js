import { NAME, ID } from './constants';
import { Component } from 'react';
import PropTypes from 'prop-types';
import { Fetch } from '../components/API';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import Publications from './components/Publications';
import Nav from './components/Nav';
import Heading from './components/Heading';
import About from './components/About';
import StoryGrid from './components/StoryGrid';
import People from './components/People';
class ProgramPage extends Component {
  render(){
    let { response: { results }, programId } = this.props;

    return (
      <div className="container">
        <Router>
          <div className="">
            <Heading program={results} />
            <Route path='/:program/:subpage?' render={(props)=>(<Nav {...props} program={results}/>)}/>
            <Switch>
              <Route path='/:program/' exact render={()=>(<StoryGrid story_grid={results.story_grid} />)} />
              <Route path='/:program/about' render={()=>(<About about={results.about} />)} />
              <Route path='/:program/our-people/' render={(props)=>(<People {...props} program={results} /> )} />
              <Route path='/:program/publications/' render={(props)=>(<Publications {...props} program={results} /> )} />
              {results.content_types.map((c,i)=>(
                <Route path={`/:program/${c.slug}/`} render={(props)=>(<Publications {...props} program={results} /> )} />
              ))}
            </Switch>
          </div>
        </Router>
      </div>
    );
  }
}

class APP extends Component {
  static propTypes = {
    programId: PropTypes.string.isRequired
  }

  render() {
    let { programId } = this.props;
    return (
      <Fetch component={ProgramPage}
        name={NAME}
        endpoint={`program/${programId}`}
        fetchOnMount={true}
        programId={programId}
      />
    );
  }
}

export default { NAME, ID, APP };

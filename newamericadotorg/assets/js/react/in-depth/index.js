import { Component } from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect, Link } from 'react-router-dom';
import { CSSTransitionGroup } from 'react-transition-group'
import { Fetch, Response } from '../components/API';
import { NAME, ID } from './constants';
import Project from './components/Project';
import Section, { Header } from './components/Section';

class InDepthRoutes extends Component {
  getSection = (sectionSlug) => {
    let { response: { results }} = this.props;
    return results.sections.find((s)=>(s.slug===sectionSlug));
  }

  componentDidMount() {
    let { response: { results }} = this.props;
    for(let i=0; i<results.sections.length; i++){
      let img = new Image();
      img.src = results.sections[i].story_image;
    }
  }

  render() {
    let { response: { results }} = this.props;
    return (
      <Router>
        <Route render={({ location })=>(
          <CSSTransitionGroup
            transitionName="fade"
            transitionEnterTimeout={500}
            transitionLeaveTimeout={500}>
            <Route path="/in-depth/:projectSlug/:sectionSlug" render={()=>(
              <Header project={results}/>
            )}/>
            <Switch key={location.key} location={location}>
              <Route exact path="/in-depth/:projectSlug" render={()=>(
                <Project project={results} />
              )}/>
              <Route exact path="/in-depth/:projectSlug/:sectionSlug" render={({ match })=>(
                <Section section={this.getSection(match.params.sectionSlug)} project={results} />
              )}/>
            </Switch>
          </CSSTransitionGroup>
        )}/>
      </Router>
    );
  }
}

class APP extends Component {

  render(){
    let { projectId } = this.props;
    return (
      <Fetch name={NAME}
        endpoint={`in-depth/${projectId}`}
        fetchOnMount={true}
        component={InDepthRoutes} />
    )
  }
}


export default { NAME, ID, APP };

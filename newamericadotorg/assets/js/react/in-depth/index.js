import { Component } from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect, Link } from 'react-router-dom';
import { CSSTransitionGroup } from 'react-transition-group'
import { Fetch, Response } from '../components/API';
import { NAME, ID } from './constants';
import Project from './components/Project';
import Section, { Header } from './components/Section';

class InDepthRoutes extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isReady: false
    };
  }

  getSection = (sectionSlug) => {
    let { response: { results }} = this.props;
    let index = 0;
    let page = results.sections.find((s,i)=>{
      if(s.slug===sectionSlug){
        index=i;
        return true;
      }
    });
    return { page, index };
  }

  componentWillMount() {
    let { response: { results }} = this.props;
    for(let i=0; i<results.sections.length; i++){
      let img = new Image();
      img.src = results.sections[i].story_image;
    }
  }

  componentDidMount() {
    let { startTime } = this.props;
    let elapsedTime = new Date() - startTime;

    if(elapsedTime > 3250){
      this.setState({ isReady: true });
    } else {
      setTimeout(()=>{
        this.setState({ isReady: true });
      }, 3250-elapsedTime);
    }
  }

  render() {
    let { response: { results }} = this.props;
    return (
      <Router>
        {this.state.isReady &&
        <Route render={({ location })=>(
          <span>
            <Route path="/in-depth/:projectSlug/:sectionSlug" render={({ match })=>(
              <Header project={results} sectionIndex={this.getSection(match.params.sectionSlug).index}/>
            )}/>
            <CSSTransitionGroup
              transitionName="fade"
              transitionAppear={true}
              transitionAppearTimeout={250}
              transitionEnterTimeout={500}
              transitionLeaveTimeout={500}>
              <Switch key={location.key} location={location}>
                <Route exact path="/in-depth/:projectSlug" render={()=>(
                  <Project project={results} />
                )}/>
                <Route exact path="/in-depth/:projectSlug/:sectionSlug" render={({ match })=>(
                  <Section section={this.getSection(match.params.sectionSlug)} project={results} />
                )}/>
              </Switch>
            </CSSTransitionGroup>
          </span>
        )}/>
        }
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
        startTime={new Date()}
        component={InDepthRoutes} />
    )
  }
}


export default { NAME, ID, APP };

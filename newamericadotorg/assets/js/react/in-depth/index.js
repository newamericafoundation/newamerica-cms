import { Component } from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect, Link } from 'react-router-dom';
import { CSSTransitionGroup } from 'react-transition-group'
import { Fetch, Response } from '../components/API';
import { NAME, ID } from './constants';
import Project from './components/Project';
import Section from './components/Section';
import Header from './components/Header';
import ScrollToTop from './components/ScrollToTop';

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

    if(elapsedTime > 2250){
      this.setState({ isReady: true });
    } else {
      setTimeout(()=>{
        this.setState({ isReady: true });
      }, 2250-elapsedTime);
    }
  }

  render() {
    let { response: { results }} = this.props;
    return (
      <Router>
        {this.state.isReady &&
        <Route path="/in-depth/:projectSlug?/:sectionSlug?" render={({ location, match })=>(
          <div className={`in-depth-window ${match.params.sectionSlug && match.params.sectionSlug != 'about' ? 'section' : ''}`}>
            <Route path="/in-depth/:projectSlug/:sectionSlug" render={({ match })=>(
              <Header project={results} match={match} sectionIndex={this.getSection(match.params.sectionSlug).index}/>
            )}/>
            <CSSTransitionGroup
              component="div"
              className="in-depth__content"
              transitionName="fade"
              transitionAppear={true}
              transitionAppearTimeout={250}
              transitionEnterTimeout={1000}
              transitionLeaveTimeout={1000}>
              <Switch key={location.key} location={location}>
                <Route exact path="/in-depth/:projectSlug/(|about)" render={()=>(
                  <Project project={results} />
                )}/>
                <Route path="/in-depth/:projectSlug/:sectionSlug" render={({ match })=>(
                  <Section section={this.getSection(match.params.sectionSlug)} project={results} />
                )}/>
              </Switch>
            </CSSTransitionGroup>
          </div>
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

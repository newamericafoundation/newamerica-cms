import { Component } from 'react';
import { NAME, ID } from './constants';
import { Fetch } from '../components/API';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import Heading from './components/Heading';
import Body from './components/Body';
import TopNav from './components/TopNav';
import BottomNav from './components/BottomNav';

class Report extends Component {
  getSection = () => {
    let { report, match: { params } } = this.props;

    if(!params.sectionSlug) return {};
    return report.sections.find((s)=>( s.slug==params.sectionSlug ));
  }

  anchorTag = () => {
    const anchor = this.props.location.hash.replace('#', '');

    if (anchor) {
      const el = document.getElementById(anchor);
      if (el) {
        const { top } = el.getBoundingClientRect();
        const { pageYOffset } = window;
        window.scrollTo(0,top+pageYOffset-50)
      }
      return true;
    }
  }

  componentDidMount(){
    this.props.dispatch({
      type: 'RELOAD_SCROLL_EVENTS',
      component: 'site'
    });
    this.anchorTag();
  }

  componentDidUpdate(prevProps) {
    if (this.props.location !== prevProps.location) {
      window.scrollTo(0, 50)
      this.props.dispatch({
        type: 'RELOAD_SCROLL_EVENTS',
        component: 'site'
      });

      this.anchorTag();
    }
  }

  render(){
    let { location, match, report } = this.props;
    let section = this.getSection();
    return (
      <div className='report no-last-child-margin'>
        <TopNav section={section} report={report} />
        <div className="container no-padding">
          {section.number===1 &&
            <Heading report={report}/>
          }
          <Body section={section}
            authors={report.authors}
            endnotes={report.endnotes}
            date={report.date}
            dispatch={this.props.dispatch}
            location={location}
            url={report.url}/>
        </div>
        <BottomNav section={section} report={report} />
      </div>
    );
  }
}

class Routes extends Component {
  reportRender = (props) => {
    let { response: { results }} = this.props;
    return (<Report {...props} dispatch={this.props.dispatch} report={results} />);
  }

  redirect = (props) => {
    let { response: { results }} = this.props;
    return <Redirect to={`${props.match.url}${results.sections[0].slug}`} />
  }

  render(){
    return (
      <Router>
        <Switch>
          <Route path='/:program/reports/:reportTitle/:sectionSlug' render={this.reportRender} />
          <Route path='/:program/reports/:reportTitle' render={this.redirect} />
          <Route path='/:program/:subprogram/reports/:reportTitle/:sectionSlug' render={this.reportRender} />
          <Route path='/:program/:subprogram/reports/:reportTitle' render={this.redirect} />
        </Switch>
      </Router>
    );
  }
}

class APP extends Component {
  render(){
    let { reportId } = this.props;
    return (
      <Fetch name={NAME}
        endpoint={`report/${reportId}`}
        fetchOnMount={true}
        component={Routes} />
    );
  }
}


export default { APP, NAME, ID };

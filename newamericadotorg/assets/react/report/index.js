import React, { Component } from 'react';
import { NAME, ID } from './constants';
import { Fetch, Response } from '../components/API';
import { Route, Switch, Redirect } from 'react-router-dom';
import GARouter from '../ga-router';
import DocumentMeta from 'react-document-meta';
import Heading from './components/Heading';
import Body from './components/Body';
import TopNav from './components/TopNav';
import BottomNav from './components/BottomNav';
import store from '../store';
import { setResponse } from '../api/actions';
import ContentMenu from './components/ContentMenu';
import OverlayMenu from './components/OverlayMenu';
import Attachments from './components/Attachments';

class Report extends Component {
  state = { menuOpen: false, contentsPosition: '0%', attchsOpen: false }

  openMenu = (e) => {
    this.setState({ menuOpen: true });
  }

  closeMenu = (e) => {
    this.setState({ menuOpen: false });
  }

  showAttachments = () => {
    this.setState({ attchsOpen: true });
  }

  hideAttachments = () => {
    this.setState({ attchsOpen: false });
  }

  animateMenu = (position) => {
    this.setState({ contentsPosition: position });
  }

  getSection = () => {
    let { report, match: { params } } = this.props;

    if(!params.sectionSlug) return false;
    return report.sections.find((s)=>( s.slug==params.sectionSlug ));
  }

  anchorTag = () => {
    const anchor = this.props.location.hash.replace('#', '');

    if (anchor) {
      const el = document.getElementById(anchor);
      if (el) {
        const { top } = el.getBoundingClientRect();
        let positionY = top-140;
        window.scrollTo(0, positionY);
      }
      return true;
    }
  }

  componentDidMount(){
    newamericadotorg.actions.addScrollEvent({
      selector: '.report',
      onTick: (el, dir, prog) => {
        let pos = prog < 130/el.offsetHeight ? '0%' : (prog > (el.offsetHeight-500)/el.offsetHeight ? '0%' : '-100%');
        this.animateMenu(pos);
      }
    });

    this.props.dispatch({
      type: 'RELOAD_SCROLL_EVENTS',
      component: 'site'
    });
    this.anchorTag();
    // react-router shim for oti colors
    if(this.props.report.programs.length > 0){
      if(this.props.report.programs[0].slug == 'oti') document.body.classList.add('oti');
    }
  }

  componentDidUpdate(prevProps) {

    if (this.props.location !== prevProps.location) {
      this.props.dispatch({
        type: 'RELOAD_SCROLL_EVENTS',
        component: 'site'
      });

      window.scrollTo(0, 0);
      this.anchorTag();
    }
  }

  render(){
    let { location, match, report, redirect } = this.props;
    let section = this.getSection();

    let showHeading = !section || report.sections.length===1;
    let showMenu = !section && report.sections.length > 1;
    let showBody = section || (!section && report.sections.length===1);
    let showOverlay = !!section;
    return (
      <DocumentMeta title={`${report.title}: ${section.title}`} description={report.search_description}>
        <div className='report'>
          <TopNav section={section} report={report}
            openMenu={this.openMenu}
            closeMenu={this.closeMenu}
            showAttachments={this.showAttachments}
            hideAttachments={this.hideAttachments}
            menuOpen={this.state.menuOpen} />
            {showHeading &&
              <Heading report={report}/>
            }
            {showMenu &&
              <div className="container margin-90">
                <ContentMenu report={report} closeMenu={this.closeMenu}/>
              </div>
            }
            {showBody && <Body section={section}
              report={report}
              dispatch={this.props.dispatch}
              location={location}
              closeMenu={this.closeMenu}/>
            }
          {showOverlay &&
            <OverlayMenu report={report}
                open={this.state.menuOpen}
                openMenu={this.openMenu}
                closeMenu={this.closeMenu}
                hideAttachments={this.hideAttachments}
                contentsPosition={this.state.contentsPosition}>
              <ContentMenu report={report} activeSection={section.slug} closeMenu={this.closeMenu}/>
            </OverlayMenu>
            }
          {showOverlay && <BottomNav section={section} report={report} />}
          {report.attachments.length > 0 &&
            <Attachments attachments={report.attachments}
              hideAttachments={this.hideAttachments}
              attchsOpen={this.state.attchsOpen}/>
          }
        </div>
      </DocumentMeta>
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
    let { response: { results }} = this.props;
    if(!results) return null;
    return (
      <GARouter>
        <Switch>
          <Route path={`/admin/pages`} render={() => (
            <Redirect to={results.url} />
          )} />
          <Route path='/:program/reports/:reportTitle/:sectionSlug?' render={this.reportRender} />
          <Route path='/:program/:subprogram/reports/:reportTitle/:sectionSlug?' render={this.reportRender} />
        </Switch>
      </GARouter>
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

  render(){
    let { reportId } = this.props;

    if(window.initialState) return <Response name={NAME} component={Routes} />

    return (
      <Fetch name={NAME}
      endpoint={`report/${reportId}`}
      fetchOnMount={true}
      component={Routes} />
    );
  }
}


export default { APP, NAME, ID };

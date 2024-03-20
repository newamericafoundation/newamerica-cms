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
import { Overlay } from './components/OverlayMenu';
import ContentMenu from './components/ContentMenu';
import Attachments from './components/Attachments';
import FeaturedSections from './components/FeaturedSections';
import Authors from './components/Authors';

const SinglePage = ({ report, dispatch, location }) => (
  <div className={`report single-page`}>
    <Heading report={report} />

    <Body
      section={report.sections[0]}
      report={report}
      dispatch={dispatch}
      location={location}
    />

    {report.authors && <div
      className="container report__body single-page-body margin-0"
      id="authors"
    >
      <div className="post-body-wrapper">
        <h3 className="margin-bottom-25">Authors</h3>
        <Authors authors={report.authors} md={true} />
      </div>
    </div>}

    {report.acknowledgments && (
      <div
        className="container report__body single-page-body margin-0"
        id="acknowledgments"
      >
        <div className="post-body-wrapper">
          <h3 className="margin-top-0 margin-bottom-25">Acknowledgments</h3>
          <div
            className="report__acknowledgments"
            dangerouslySetInnerHTML={{ __html: report.acknowledgments }}
          />
          {report.partner_logo && (
            <div className="margin-top-25">
              <img src={report.partner_logo} alt={report.partner_logo_alt} />
            </div>
          )}
        </div>
      </div>
    )}
  </div>
);

const Landing = ({ report, dispatch, location, closeMenu, preview }) => (
  <div className={`report landing`}>
    <Heading report={report} />

    {report.abstract && (
      <div className="container margin-80" id="abstract">
        <h3 className="margin-top-0 margin-bottom-25">Abstract</h3>
        <div
          className="report__abstract"
          dangerouslySetInnerHTML={{ __html: report.abstract }}
          style={{ maxWidth: '800px' }}
        />
      </div>
    )}

    {report.featured_sections.length > 0 && (
      <div className="container margin-80" id="featured">
        <h3 className="margin-top-0 margin-bottom-25">Featured Sections</h3>
        <div className="featured__scroll-wrapper">
          <FeaturedSections featuredSections={report.featured_sections} />
        </div>
      </div>
    )}

    <div className="container margin-80" id="contents">
      <h3 className="margin-top-0 margin-bottom-25">Contents</h3>
      <ContentMenu preview={preview} report={report} closeMenu={closeMenu} />
    </div>

    {report.authors && <div className="container margin-80" id="authors">
      <h3 className="margin-top-0 margin-bottom-25">Authors</h3>
      <Authors authors={report.authors} />
    </div>}

    {report.acknowledgments && (
      <div className="container margin-80" id="acknowledgments">
        <h3 className="margin-top-0 margin-bottom-25">Acknowledgments</h3>
        <div
          className="report__acknowledgments"
          dangerouslySetInnerHTML={{ __html: report.acknowledgments }}
          style={{ maxWidth: '800px' }}
        />
        {report.partner_logo && (
          <div className="margin-top-25">
            <img src={report.partner_logo} alt={report.partner_logo_alt} />
          </div>
        )}
      </div>
    )}
  </div>
);

class Report extends Component {
  constructor(props) {
    super(props);
    this.state = {
      menuOpen: false,
      contentsPosition: '0%',
      attchsOpen: false,
      section: this.getSection(),
      attchClicked: false
    };
  }

  fixBody = () => {
    const top = window.pageYOffset;
    document.body.style.overflow = 'hidden';
    document.body.style.position = 'fixed';
    document.body.style.top = -top + 'px';
  };

  unfixBody = () => {
    document.body.style.overflow = 'auto';
    document.body.style.position = 'static';
    if (document.body.style.top)
      window.scrollTo(0, -document.body.style.top.replace('px', ''));

    document.body.style.top = null;
  };

  openMenu = e => {
    this.fixBody();
    this.setState({ menuOpen: true });
  };

  closeMenu = e => {
    this.unfixBody();
    this.setState({ menuOpen: false });
  };

  showAttachments = () => {
    this.fixBody();
    this.setState({ attchsOpen: true, attchClicked: true });
  };

  hideAttachments = () => {
    this.unfixBody();
    this.setState({ attchsOpen: false });
  };

  animateMenu = position => {
    this.setState({ contentsPosition: position });
  };

  getSection = () => {
    let {
      report,
      match: { params }
    } = this.props;

    if (!params.sectionSlug) return false;
    return report.sections.find(s => s.slug == params.sectionSlug);
  };

  anchorTag = () => {
    const anchor = this.props.location.hash.replace('#', '');

    if (anchor) {
      const el = document.getElementById(anchor);
      if (el) {
        const { top } = el.getBoundingClientRect();
        let positionY = top + document.documentElement.scrollTop;
        window.scrollTo(0, positionY);
      }
      return true;
    }
  };

  componentDidMount() {
    let { report } = this.props;
    this.props.dispatch({
      type: 'RELOAD_SCROLL_EVENTS',
      component: 'site'
    });
    this.anchorTag();
    // react-router shim for oti colors
    if (this.props.report.programs.length > 0) {
      if (this.props.report.programs[0].slug == 'oti')
        document.body.classList.add('oti');
    }
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.props.location !== prevProps.location) {
      this.props.dispatch({
        type: 'RELOAD_SCROLL_EVENTS',
        component: 'site'
      });

      window.scrollTo(0, 0);
      this.setState({ section: this.getSection() });
    }

    if (this.state.section != prevState.section) {
      this.anchorTag();
    }
  }

  render() {
    let { location, match, report, redirect, dispatch } = this.props;
    let { section, attchClicked } = this.state;

    let singlePage = report.sections.length === 1;
    let landing = !section && !singlePage;

    return (
      <DocumentMeta
        title={`${report.title}${section ? ': ' + section.title : ''}`}
        description={report.search_description}
      >
        <TopNav
          section={section}
          report={report}
          openMenu={this.openMenu}
          closeMenu={this.closeMenu}
          showAttachments={this.showAttachments}
          hideAttachments={this.hideAttachments}
          attchClicked={attchClicked}
          menuOpen={this.state.menuOpen}
        />

        <main>

          {singlePage && <SinglePage {...this.props} />}

          {landing && <Landing closeMenu={this.closeMenu} {...this.props} />}

          {section && (
            <div className={`report section`}>
              <Body
                section={section}
                report={report}
                dispatch={this.props.dispatch}
                location={location}
              />
            </div>
          )}

        </main>

        <div
          className={`bottom-nav-wrapper scroll-target ${
            section ? 'show' : 'hide'
          }`}
          data-scroll-offset="65"
          data-scroll-trigger-point="bottom"
        >
          <BottomNav
            preview={this.props.preview}
            section={section}
            report={report}
            openMenu={this.openMenu}
            hideAttachments={this.hideAttachments}
          />
        </div>

        <Overlay
          title="Contents"
          close={this.closeMenu}
          open={this.state.menuOpen}
        >
          <ContentMenu
            report={report}
            closeMenu={this.closeMenu}
            showHome={true}
            preview={this.props.preview}
          />
        </Overlay>

        {report.attachments.length > 0 && (
          <Attachments
            attachments={report.attachments}
            hideAttachments={this.hideAttachments}
            attchsOpen={this.state.attchsOpen}
          />
        )}
      </DocumentMeta>
    );
  }
}

class Routes extends Component {
  reportRender = props => {
    let {
      response: { results }
    } = this.props;
    return (
      <Report {...props} dispatch={this.props.dispatch} report={results} />
    );
  };

  redirect = props => {
    let {
      response: { results }
    } = this.props;
    return <Redirect to={`${props.match.url}${results.sections[0].slug}`} />;
  };

  render() {
    let {
      response: { results }
    } = this.props;
    if (!results) return null;
    return (
      <GARouter>
        <Switch>
          <Route
            path={`/admin/pages`}
            render={() => <Redirect to={results.url} />}
          />
          <Route
            path={`/h_preview`}
            render={(props) => this.reportRender(Object.assign(props, {preview: true}))}
          />
          <Route
            path="/preview/:program/:subprogram/reports/:reportTitle/:sectionSlug?"
            render={(props) => this.reportRender(Object.assign(props, {preview: true}))}
          />
          <Route
            path="/preview/:program/reports/:reportTitle/:sectionSlug?"
            render={(props) => this.reportRender(Object.assign(props, {preview: true}))}
          />
          <Route
            path="/:program/reports/:reportTitle/:sectionSlug?"
            render={this.reportRender}
          />
          <Route
            path="/:program/:subprogram/reports/:reportTitle/:sectionSlug?"
            render={this.reportRender}
          />
        </Switch>
      </GARouter>
    );
  }
}

class APP extends Component {
  componentDidMount() {
    if (window.initialState) {
      store.dispatch(
        setResponse(NAME, {
          count: 0,
          page: 1,
          hasNext: false,
          hasPrevious: false,
          results: window.initialState
        })
      );
    }
  }

  render() {
    let { reportId, preview, token, contentType } = this.props;

    if (preview) {
      return (
        <Fetch
          name={NAME}
          endpoint={`preview`}
          initialQuery={{'content_type': contentType, token: token}}
          fetchOnMount={true}
          component={Routes}
        />
      );
    }

    if (window.initialState) return <Response name={NAME} component={Routes} />;

    return (
      <Fetch
        name={NAME}
        endpoint={`report/${reportId}`}
        fetchOnMount={true}
        component={Routes}
      />
    );
  }
}

export default { APP, NAME, ID };

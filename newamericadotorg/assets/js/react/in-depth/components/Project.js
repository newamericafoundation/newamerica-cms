import { Component } from 'react';
import { Link, Route, Switch } from 'react-router-dom';
import Contents from './TableOfContents';
import ScrollToTop from './ScrollToTop';
import loadExternalScript from '../load-external-script';

const Intro = ({ slug, project: { title, subheading }}) => (
  <div className="in-depth__intro">
    <div className="in-depth__intro__text">
      <div className="in-depth__intro__text__logo">
        <div className="logo bug in-depth-logo-bug"></div>
        <h4 className="no-margin">In-Depth</h4>
      </div>
      <div className="in-depth__intro__text__heading">
        <h1 className={`centered narrow-margin`}>{title}</h1>
        {subheading && <p className="in-depth__intro__text__heading__sub centered no-margin">{subheading}</p>}
      </div>
      <div className="in-depth__intro__text__link">
        <Link to={`/in-depth/${slug}/about`}>
          <label className="in-depth-label">
            Contents
            <i className="fa fa-arrow-right"></i>
          </label>
        </Link>
      </div>
    </div>
  </div>
);

const About = ({ project: { sections, body }}) => (
  <div className="in-depth__about">
    <div className="row">
      {body && <div className="in-depth__about__text col-md-6">
        <label className="in-depth-label">About</label>
        <div className="in-depth__project__text__body" dangerouslySetInnerHTML={{__html: body}}/>
      </div>}
      <div className="in-depth__about__contents col-md-6">
        <Contents sections={sections} />
      </div>
    </div>
  </div>
);

export default class Project extends Component {
  componentDidMount(){
    let { project } = this.props;
    loadExternalScript(project.data_project_external_script);
  }

  render(){
    let { project } = this.props;

    return (
      <Switch>
        <Route exact path="/in-depth/:projectSlug" render={({match})=>( <Intro slug={match.params.projectSlug} project={project}/> )} />
        <Route path="/in-depth/:projectSlug/about" render={()=>( <About project={project}/> )} />
      </Switch>
    );
  }
}

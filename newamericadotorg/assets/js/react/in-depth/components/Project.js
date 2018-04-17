import { Component } from 'react';
import { Link, Route, Switch } from 'react-router-dom';
import Contents from './TableOfContents';
import ScrollToTop from './ScrollToTop';
import loadExternalScript from '../load-external-script';

const Intro = ({ slug, project: { title, subheading }}) => (
  <div className="in-depth__intro">
    <div className="in-depth__intro__text">
      <div className="in-depth__intro__text__logo">
        <a href="/"><div className="logo bug in-depth-logo-bug"></div></a>
        <h4 className="margin-0">In-Depth</h4>
      </div>
      <div className="in-depth__intro__text__heading">
        <h1 className={`centered margin-5`}>{title}</h1>
        {subheading && <p className="in-depth__intro__text__heading__sub centered margin-0">{subheading}</p>}
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

class AboutBody extends Component {
  constructor(props){
    super(props);
    this.state = { active: false };
    this.el = {};
  }
  render(){
    let { body } = this.props;
    return (
      <div ref={(el)=>{ this.el=el; }} className="in-depth__about__text col-lg-6">
        <label className="in-depth-label">About</label>
        <div className={`in-depth__about__text__body ${this.state.active ? 'active': ''}`} dangerouslySetInnerHTML={{__html: body}}/>
        {this.el.offsetHeight > 250 && <div className="read-more" onClick={()=>{this.setState({active: !this.state.active})}}>
          {this.state.active && <label className="in-depth-label">Read Less -</label>}
          {!this.state.active && <label className="in-depth-label">Read More +</label>}
        </div>}
      </div>
    );
  }
}

const About = ({ project: { sections, body }}) => (
  <div className="in-depth__about">
    <div className="row">
      {body && <AboutBody body={body}/>}
      <div className="in-depth__about__contents col-lg-6">
        <Contents sections={sections} />
      </div>
    </div>
  </div>
);

export default class Project extends Component {
  componentDidMount(){
    let { project } = this.props;
    setTimeout(()=>{
      loadExternalScript(project.data_project_external_script);
    }, 600);
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

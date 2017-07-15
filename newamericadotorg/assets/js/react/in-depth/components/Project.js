import { Component } from 'react';
import { Link } from 'react-router-dom';
import ScrollToTop from './ScrollToTop';
import loadExternalScript from '../load-external-script';

const Heading = ({ project: { story_image, title } }) => (
  <section className="in-depth__heading in-depth__project__heading">
    <header className="in-depth__project__heading__header">
        <div className="in-depth__project__heading__header__logo-wrapper">
          <div className="logo sm white"/>
        </div>
        <div className="in-depth__project__heading__header__in-depth-title">
          <h3 className>In Depth</h3>
        </div>
    </header>
    <div className="in-depth__heading__image-wrapper">
      <div className="in-depth__heading__image" style={{backgroundImage: `url(${story_image})`}}></div>
    </div>
    <div className="in-depth__heading__text">
      <h1 className="in-depth__heading__text__title">{title}</h1>
    </div>
  </section>
);

const Contents = ({ sections }) => (
  <div className="in-depth__project__body__contents">
    <h2>Contents</h2>
    <ul className="in-depth__project__body__contents__list">
    {sections.map((s,i)=>(
      <li>
        <label className="lg active"><Link to={s.url}>{s.title}</Link></label>
        <p>{s.story_excerpt}</p>
      </li>
    ))}
    </ul>
  </div>
)

export default class Project extends Component {
  componentDidMount(){
    let { project } = this.props;
    loadExternalScript(project.data_project_external_script);
  }

  render(){
    let { project } = this.props;

    return (
      <div className="in-depth__project">
        <ScrollToTop />
        <Heading project={project} />
        <section className={`in-depth__project__body ${project.body ? 'with-body': ''}`}>
          <div className="container--medium">
            {project.sections.length>0 && <Contents sections={project.sections} />}
            {project.body &&
              <div className="in-depth__project__body__text" dangerouslySetInnerHTML={{__html: project.body}}/>
            }
          </div>
        </section>
      </div>
    );
  }
}

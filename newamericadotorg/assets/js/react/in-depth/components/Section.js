import { Component } from 'react';
import { Link } from 'react-router-dom';
import ScrollToTop from './ScrollToTop';
import loadExternalScript from '../load-external-script';

const Header = ({ project }) => (
  <header className="container--full-width in-depth__section__header">
    <div className="row">
      <div className="in-depth__section__header__project-title col-3">
        <label className="lg active">
          <a className="newamerica-name" href="/">NEW<br/>AMERICA</a> / <a className="in-depth-name" href="/in-depth">In Depth</a></label>
        <h4 className="narrow-margin"><Link to={project.url}>{project.title}</Link></h4>
      </div>
      <div className="in-depth__section__header__section-list col-9">
        {project.sections.map((s,i)=>(
          <div className="in-depth__section__header__section-list__item">
            <Link to={s.url}>
              <div className="in-depth__section__header__section-list__item__image">
                <img src={s.story_image_sm} />
              </div>
              <label className="in-depth__section__header__section-list__item__text lg block">
                {s.title}
              </label>
            </Link>
          </div>
        ))}
      </div>
    </div>
  </header>
)

const Heading = ({ section: { story_image, title }, project }) => (
  <section className="in-depth__heading in-depth__section__heading">
    <div className="in-depth__heading__image-wrapper">
      <div className="in-depth__heading__image" style={{backgroundImage: `url(${story_image})`}}></div>
    </div>
    <div className="in-depth__heading__text">
      <h2 className="in-depth__heading__text__title">{title}</h2>
    </div>
  </section>
);

export default class Section extends Component {
  componentDidMount(){
    let { project } = this.props;
    loadExternalScript(project.data_project_external_script);
  }

  render(){
    let { section, project } = this.props;

    return (
      <div className="in-depth__section">
        <ScrollToTop />
        <Heading section={section} project={project} />
        <article className="in-depth__section__body container--narrow" dangerouslySetInnerHTML={{__html: section.body}}/>
      </div>
    );
  }
}

export { Header }

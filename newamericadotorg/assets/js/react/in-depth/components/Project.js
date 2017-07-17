import { Component } from 'react';
import { Link } from 'react-router-dom';
import ScrollToTop from './ScrollToTop';
import loadExternalScript from '../load-external-script';

const getSectionUrl = (url) => {
  let relativeLink = /(\/in-depth\/.+)/.exec(url);
  if(relativeLink) return relativeLink[1];
  return false;
}

const QuickNav = ({ buttons, sections }) => (
  <nav className="in-depth__project__quick-nav">
    {buttons.length > 0 && <label className="lg active">Get Started:</label>}
    {buttons.map((b,i)=>(
      <div className="in-depth__project__quick-nav__item">
        {(i===0 && getSectionUrl(b.url)) &&
          <Link to={getSectionUrl(b.url)} className="button">
            {sections[0].title.indexOf(':')!=-1 ? sections[0].title : `Section 1: ${sections[0].title}` }
          </Link>
        }
        {(i>0 && getSectionUrl(b.url)) &&
          <Link to={getSectionUrl(b.url)} className="button white">{b.text}</Link>}
        {!getSectionUrl(b.url) &&
          <a href={b.url} className="button white">{b.text}</a>}
      </div>
    ))}
  </nav>
);

const Heading = ({ project: { story_image, title, sections, buttons } }) => (
  <section className="in-depth__heading in-depth__project__heading">
    <header className="in-depth__project__heading__header">
        <div className="in-depth__project__heading__header__logo-wrapper">
          <a href="/"><div className="logo sm white"/></a>
        </div>
        <div className="in-depth__project__heading__header__in-depth-title">
          <a href="/in-depth"><h3>In Depth</h3></a>
        </div>
    </header>
    <div className="in-depth__heading__image-wrapper">
      <div className="in-depth__heading__image" style={{backgroundImage: `url(${story_image})`}}></div>
    </div>
    <div className="in-depth__heading__text">
      <h1 className="in-depth__heading__text__title">{title}</h1>
    </div>
    <QuickNav sections={sections} buttons={buttons} />
    <div className="see-more">
      <i className="fa fa-arrow-circle-down"></i>
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
);

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

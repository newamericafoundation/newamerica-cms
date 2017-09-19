import { Component } from 'react';
import { Link } from 'react-router-dom';
import SectionNav from './SectionNav';
import ScrollToTop from './ScrollToTop';
import loadExternalScript from '../load-external-script';

const Heading = ({ section: { page, index }, project }) => (
  <section className="in-depth__heading">
    <div className="in-depth__heading__text">
      <h1 className="in-depth__heading__text__title no-margin">{page.title}</h1>
    </div>
  </section>
);

export default class Section extends Component {
  componentDidMount(){
    let { project } = this.props;
    setTimeout(()=>{
      loadExternalScript(project.data_project_external_script)
    },600);

    this.props.dispatch({
      type: 'RELOAD_SCROLL_EVENTS',
      component: 'site'
    });
  }

  render(){
    let { section, project } = this.props;
    return (
      <div className="in-depth__section">
        <ScrollToTop />
        <div className="container">
          <Heading section={section} project={project} />
          <div className="row">
            <aside className="in-depth__authors col-md-4 col-xl-3">
              <label className="in-depth-label">Authors</label>
              {project.authors.map((a)=>(
                <div className="in-depth__author">
                  <label className="in-depth__author__name">
                    <a href={a.url}>
                      {`${a.first_name} ${a.last_name}`}
                    </a>
                  </label>
                  <p className="in-depth__author__position no-margin">{a.position}</p>
                </div>
              ))}
            </aside>
            <article className="in-depth__section__body scroll-target post-body col-md-8 col-xl-9"
              data-scroll-target=".in-depth__header"
              dangerouslySetInnerHTML={{__html: section.page.body}}/>
          </div>
        </div>
        <SectionNav sections={project.sections} currentIndex={section.index} />
      </div>
    );
  }
}

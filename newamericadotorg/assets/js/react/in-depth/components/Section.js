import { Component } from 'react';
import { Link } from 'react-router-dom';
import Slider from 'react-slick';
import ScrollToTop from './ScrollToTop';
import loadExternalScript from '../load-external-script';

const Header = ({ project, sectionIndex }) => (
  <header className="container--full-width in-depth__section__header">
    <div className="row">
      <div className="in-depth__section__header__project-title col-3">
        <label className="lg active">
          <a className="newamerica-name" href="/">NEW<br/>AMERICA</a> / <a className="in-depth-name" href="/in-depth">In Depth</a></label>
        <h4 className="narrow-margin"><Link to={project.url}>{project.title}</Link></h4>
      </div>
      <div className="in-depth__section__header__section-list col-9">
        <Slider
          infinite={false}
          speed={500}
          slidesToShow={4}
          slidesToScroll={4}
          initialSlide={Math.floor(sectionIndex/4)*4}
          prevArrow={<div><i className="fa fa-arrow-circle-left"></i></div>}
          nextArrow={<div><i className="fa fa-arrow-circle-right"></i></div>}>
          {project.sections.map((s,i)=>(
            <div className={`in-depth__section__header__section-list__item ${i===sectionIndex ? 'active' : ''}`}>
              <Link draggable={false} to={s.url} onDragStart={()=>{console.log('here!')}}>
                <div className="in-depth__section__header__section-list__item__image">
                  <img src={s.story_image_sm} draggable={false}/>
                </div>
                <label className="in-depth__section__header__section-list__item__text lg">
                  {s.title}
                </label>
              </Link>
            </div>
          ))}
          </Slider>
      </div>
    </div>
  </header>
)

const Heading = ({ section: { page, index }, project }) => (
  <section className="in-depth__heading in-depth__section__heading">
    <div className="in-depth__heading__image-wrapper">
      <div className="in-depth__heading__image" style={{backgroundImage: `url(${page.story_image})`}}></div>
    </div>
    <div className="in-depth__heading__text">
      <h2 className="in-depth__heading__text__title">{page.title}</h2>
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
        <article className="in-depth__section__body container--narrow" dangerouslySetInnerHTML={{__html: section.page.body}}/>
      </div>
    );
  }
}

export { Header }

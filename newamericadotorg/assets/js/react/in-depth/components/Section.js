import { Component } from 'react';
import ScrollToTop from './ScrollToTop';
import loadExternalScript from '../load-external-script';

const Heading = ({ section: { story_image, title } }) => (
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
    let { section } = this.props;

    return (
      <div className="in-depth__section">
        <ScrollToTop />
        <Heading section={section} />
        <article className="in-depth__section__body container--narrow" dangerouslySetInnerHTML={{__html: section.body}}/>
      </div>
    );
  }
}

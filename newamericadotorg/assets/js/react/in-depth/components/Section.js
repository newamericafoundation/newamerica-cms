import { Component } from 'react';
import { Link } from 'react-router-dom';
import ScrollToTop from './ScrollToTop';
import loadExternalScript from '../load-external-script';

const Heading = ({ section: { page, index }, project }) => (
  <section className="in-depth__heading">
    <div className="in-depth__heading__text">
      <h1 className="in-depth__heading__text__title">{page.title}</h1>
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

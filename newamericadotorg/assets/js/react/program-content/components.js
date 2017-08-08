import { NAME, IMAGE_RENDITION } from './constants';
import { Component } from 'react';
import { Fetch } from '../components/API';

export const ContentGridItem = ({ item, className }) => (
  <div className={`content-grid__item ${className} ${item.story_image? 'with-image' : ''}`}>
      {item.story_image &&
        <div className="content-grid__item__image-wrapper">
          <img src={item.story_image} className="content-grid__item__image" />
        </div>
      }
      <div className="content-grid__item__text">
        <label className="content-grid__item__text__content-type narrow-margin">{item.content_type.name}</label>
        <h4 className="no-margin content-grid__item__text__title">
          <a href={item.url} className="content-grid__item__link-wrapper">{item.title}</a>
        </h4>
        <p className="content-grid__item__text__description narrow-margin gray">{item.story_excerpt}</p>
      </div>
  </div>
);

export const ContentGrid = ({ response }) => (
  <section className="container--full-width program-block">
  	<div className="program-block__heading">
  		<h1 className="centered narrow-margin">Publications</h1>
  		<p className="program-heading__subheading subheading--h1 centered">
  			Political Reform program publications help to generate new ideas, voices, and technologies.
  		</p>
  	</div>
  	<section className="program-content-grid container">
      <div className="row">
        {response.results.map((item, i) => (
          <ContentGridItem item={item} className="col-md-3" />
        ))}
      </div>
    </section>
  	<div className="program-block__button-wrapper button-wrapper centered">
  		<a className="button transparent" href="{{page.url}}publications/">View All Publications</a>
  	</div>
  </section>
);

export class Content extends Component {
  render(){
    let { programId } = this.props;

    return(
      <Fetch
        name='program.content'
        endpoint="post"
        fetchOnMount={true}
        component={ContentGrid}
        showLoading={true}
        renderIfNoResults={false}
        transition={true}
        initialQuery={{
          page_size: 4,
          image_rendition: IMAGE_RENDITION,
          program_id: programId
        }}
      />
    );
  }
}

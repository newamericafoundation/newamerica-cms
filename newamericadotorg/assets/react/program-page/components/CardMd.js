import React, { Component } from 'react';
import Image from '../../components/Image';

export default class CardMd extends Component {
  render(){
    let { post, image_size, loaded } = this.props;
    return (
      <div className={`card md ${image_size || ''} md-side`}>
        <a href={post.url} className="row gutter-0">
          <div className="col-6 col-md-12">
            <div className="card__image">
              <Image thumbnail={post.story_image_thumbnail.url} image={post.story_image.url} alt={post.story_imagee_alt} loaded={loaded}/>
            </div>
          </div>
          <div className="col-6 col-md-12">
            <div className="card__text">
              {/* <h3 className="card__text__title bold margin-top-0 block">{post.title}</h3> */}
              <h4 className="card__text__title margin-0">
                <span><u>{post.seo_title || post.title}</u></span>
              </h4>
              <h6 className="card__text__program caption margin-top-10 margin-bottom-0">
                {post.programs ? post.programs[0].name : ''} {post.content_type ? post.content_type.name : ''}
              </h6>
            </div>
          </div>
        </a>
      </div>
    )
  }
}

import React, { Component } from 'react';
import Image from '../../components/Image';
import ellipsize from '../../../lib/utils/ellipsize';

export default class CardSm extends Component {
  render(){
    let { post } = this.props;

    return (
      <div className="card sm">
        <a href={post.url} className="row no-gutters">
          <div className="col-6">
            <div className={`card__image ${post.story_image ? '' : 'no-image'}`}>
              <Image thumbnail={post.story_image_thumbnail} image={post.story_image}/>
            </div>
          </div>
          <div className="col-6">
            <div className="card__text">
              <h4 className="card__text__title margin-0">
                <span><u>{ellipsize(post.seo_title || post.title)}</u></span>
              </h4>
              <h6 className="card__text__program caption margin-top-10 margin-bottom-0">
                {post.content_type ? post.content_type.name : ''}
              </h6>
            </div>
          </div>
        </a>
      </div>
    );
  }
}

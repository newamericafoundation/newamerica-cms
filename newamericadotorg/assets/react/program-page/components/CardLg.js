import React, { Component } from 'react';
import Image from '../../components/Image';

export default class CardLg extends Component {
 constructor(props){
    super(props);
    this.state = {
      imageLoaded: props.loaded
    }
  }

  onImageLoad = () => {
    this.setState({ imageLoaded: true });
  }

  render(){
    let { post, loaded } = this.props;
    return (
      <div className="card lg">
        <a href={post.url} className="row no-gutters">
          <div className="col-12 col-md-8">
            <div className="card__image">
              {post.story_image &&
                <Image thumbnail={post.story_image_thumbnail.url} image={post.story_image.url} loaded={loaded}/>
              }
            </div>
          </div>
          <div className="col-12 col-md-4">
            <div className="card__text">
              <h2 className="card__text__title margin-0 block">
                <span><u>{post.seo_title || post.title}</u></span>
              </h2>
              <h6 className="card__text__subtitle margin-10">{post.story_excerpt}</h6>
              <h6 className="card__text__program caption margin-top-10 margin-bottom-0">
                {post.programs ? post.programs[0].title : ''} {post.content_type ? post.content_type.name : ''}</h6>
            </div>
          </div>
          </a>
      </div>
    )
  }
}

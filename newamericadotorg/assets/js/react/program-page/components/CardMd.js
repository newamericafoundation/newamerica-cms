import { Component } from 'react';
import Image from '../../components/Image';

export default class CardMd extends Component {
  render(){
    let { post, image_size, loaded } = this.props;
    return (
      <div className={`card md ${image_size || ''}`}>
        <a href={post.url}>
          <div className="card__image">
            <Image thumbnail={post.story_image_thumbnail} image={post.story_image} loaded={loaded}/>
          </div>
          <div className="card__text">
            <label className="card__text__title bold margin-top-0 block">{post.title}</label>
            <label className="card__text__program caption margin-bottom-0 block">
              {post.programs ? post.programs[0].name : ''} {post.content_type ? post.content_type.name : ''}
            </label>
          </div>
        </a>
      </div>
    )
  }
}

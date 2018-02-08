import { Component } from 'react';
import Image from '../../components/Image';

export default class CardMd extends Component {
  render(){
    let { post, image_size, loaded } = this.props;
    return (
      <div className={`card md ${image_size || ''} md-side`}>
        <a href={post.url} className="row gutter-0">
          <div className="col-6 col-md-12">
            <div className="card__image">
              <Image thumbnail={post.story_image_thumbnail} image={post.story_image} loaded={loaded}/>
            </div>
          </div>
          <div className="col-6 col-md-12">
            <div className="card__text">
              <label className="card__text__title bold margin-top-0 block">{post.title}</label>
              <label className="card__text__program caption margin-bottom-0 block">
                {post.programs ? post.programs[0].name : ''} {post.content_type ? post.content_type.name : ''}
              </label>
            </div>
          </div>
        </a>
      </div>
    )
  }
}

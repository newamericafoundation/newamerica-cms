import { Component } from 'react';
import Image from '../../components/Image';

export default class CardMd extends Component {
  contentType = () => {
    let { post } = this.props;
    if(post.content_type){
      return post.content_type.name == 'redirect page' ? 'External Website' : post.content_type.name;
    }

    return '';
  }
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
              {/* <h3 className="card__text__title bold margin-top-0 block">{post.title}</h3> */}
              <label className="card__text__title bold margin-top-0 block link">
                <span><u>{post.title}</u></span>
              </label>
              <label className="card__text__program caption margin-bottom-0 block">
                {post.programs ? post.programs[0].name : ''} {this.contentType()}
              </label>
            </div>
          </div>
        </a>
      </div>
    )
  }
}

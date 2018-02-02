import { Component } from 'react';

export default class CardMd extends Component {
  state = {
    imageLoaded: false
  }

  onImageLoad = () => {
    this.setState({ imageLoaded: true });
  }

  render(){
    let { post, image_size } = this.props;
    return (
      <div className={`card md ${image_size || ''}`}>
        <a href={post.url}>
          <div className="card__image">
            <div className="card__image__background" style={{ backgroundImage: `url(${post.story_image_thumbnail})`}} />
            <img className={`${this.state.imageLoaded ? 'loaded' : ''}`} src={post.story_image} onLoad={this.onImageLoad}/>
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

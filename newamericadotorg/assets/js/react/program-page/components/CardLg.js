import { Component } from 'react';

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
    let { post } = this.props;
    return (
      <div className="card lg">
        <a href={post.url} className="row no-gutters">
          <div className="col-8" style={{paddingRight: '3px'}}>
            <div className="card__image">
              <div className="card__image__background" style={{ backgroundImage: `url(${post.story_image_thumbnail})`}} />
              <img className={`${this.state.imageLoaded ? 'loaded' : ''}`} src={post.story_image} onLoad={this.onImageLoad}/>
            </div>
          </div>
          <div className="col-4">
            <div className="card__text">
              <h2 className="card__text__title margin-top-0 block">{post.title}</h2>
              <label className="card__text__subtitle subtitle block">{post.story_excerpt}</label>
              <label className="card__text__program caption margin-bottom-0 block">
                {post.programs ? post.programs[0].title : ''}
                {post.content_type ? post.content_type.name : ''}</label>
            </div>
          </div>
          </a>
      </div>
    )
  }
}

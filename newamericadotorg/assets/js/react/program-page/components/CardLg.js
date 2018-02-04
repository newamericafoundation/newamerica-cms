import { Component } from 'react';
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
          <div className="col-8" style={{paddingRight: '3px'}}>
            <div className="card__image">
              <Image thumbnail={post.story_image_thumbnail} image={post.story_image} loaded={loaded}/>
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

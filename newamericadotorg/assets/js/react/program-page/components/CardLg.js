import { Component } from 'react';
import Image from '../../components/Image';

export default class CardLg extends Component {
 constructor(props){
    super(props);
    this.state = {
      imageLoaded: props.loaded
    }
  }

  contentType = () => {
    let { post } = this.props;
    if(post.content_type){
      return post.content_type.name == 'redirect page' ? 'External Website' : post.content_type.name;
    }

    return '';
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
              <Image thumbnail={post.story_image_thumbnail} image={post.story_image} loaded={loaded}/>
            </div>
          </div>
          <div className="col-12 col-md-4">
            <div className="card__text">
              <h2 className="card__text__title margin-0 block">
                <span><u>{post.title}</u></span>
              </h2>
              <h6 className="card__text__subtitle margin-10">{post.story_excerpt}</h6>
              <h6 className="card__text__program caption margin-top-10 margin-bottom-0">
                {post.programs ? post.programs[0].title : ''} {this.contentType()}</h6>
            </div>
          </div>
          </a>
      </div>
    )
  }
}

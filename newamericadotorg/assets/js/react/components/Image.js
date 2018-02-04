import { Component } from 'react';

export default class Image extends Component {
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
    let { thumbnail, image } = this.props;
    return (
      <span>
        {thumbnail && <div className="card__image__background temp-image" style={{ backgroundImage: `url(${thumbnail})`}} />}
        <img className={`${this.state.imageLoaded ? 'loaded' : ''}`} src={image} onLoad={this.onImageLoad}/>
      </span>
    );
  }
}

import { Component } from 'react';
import { connect } from 'react-redux';
import getNestedState from '../../../utils/get-nested-state';
import { loadArticleImage, setIsReady, clearArticleImages } from '../actions';

class Preload extends Component {
  loaded = false;
  componentWillMount(){
    this.clear(this.props);
  }

  componentWillUpdate(nextProps){
    if(this.props.edition !== nextProps.edition) return this.clear(nextProps);
    let { edition, images } = nextProps;
    if(!edition || !images) return;
    if(edition.length===0) return;
    if(!this.loaded) return this.preloadImages(nexProps);
    if(edition.articles.length === images.length){
      nextProps.dispatch(setIsReady(true));
    }
  }

  clear = (props) => {
    props.dispatch(clearArticleImages());
    props.dispatch(setIsReady(false));
    if(props.edition){
      if(props.edition.length!==0) this.preloadImages(props);
    }
  }
  preloadImages(props){
    let { edition: { articles } } = props;
    for(let i=0; i<articles.length; i++){
      let img = new Image();
      img.onload = () => {
        this.props.dispatch(loadArticleImage(img));
      }
      img.src = articles[i].story_image_sm;
      let img2 = new Image();
      img2.src = articles[i].story_image;
    }
    return this.loaded = true;
  }

  render(){
    return null;
  }
}

const mapStateToProps = (state) => ({
  images: getNestedState(state, 'weekly.edition.articleImages'),
  edition: getNestedState(state, 'weekly.edition.results')
});

export default connect(mapStateToProps)(Preload);

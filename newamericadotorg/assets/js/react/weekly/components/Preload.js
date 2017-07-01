import { Component } from 'react';
import { connect } from 'react-redux';
import getNestedState from '../../../utils/get-nested-state';
import { loadArticleImage, setIsReady, clearArticleImages } from '../actions';

class Preload extends Component {
  start;
  timeout = 0;
  componentWillMount(){
    this.clear(this.props);
    if(!this.props.isReady && this.props.match.params.article){
      this.setAsReady(this.props);
    }
  }

  componentWillUpdate(nextProps){
    if(this.props.edition !== nextProps.edition) return this.clear(nextProps);
    let { edition, images, isReady } = nextProps;
    if(!edition || !images) return;
    if(edition.length===0) return;
    if(edition.articles.length === images.length && !isReady)
      return this.setAsReady(nextProps);
  }

  setAsReady = (props) => {
    clearTimeout(this.timeout);
    let elapsed = new Date() - this.start;
    if(elapsed>=800) props.dispatch(setIsReady(true));
    setTimeout(()=>{
      props.dispatch(setIsReady(true));
    }, 800-elapsed);
  }

  clear = (props) => {
    this.start = new Date();
    props.dispatch(clearArticleImages());
    props.dispatch(setIsReady(false));
    if(props.edition){
      if(props.edition.length!==0) this.preloadImages(props);
    }
    // you have 4 seconds to load images or it's loading without you
    this.timeout = setTimeout(()=>{
      this.setAsReady(props);
    }, 4000);
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
  }

  render(){
    return null;
  }
}

const mapStateToProps = (state) => ({
  images: getNestedState(state, 'weekly.edition.articleImages'),
  edition: getNestedState(state, 'weekly.edition.results'),
  isReady: getNestedState(state, 'weekly.edition.isReady')
});

export default connect(mapStateToProps)(Preload);

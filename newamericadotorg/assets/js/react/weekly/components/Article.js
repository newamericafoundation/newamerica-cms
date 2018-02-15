import Heading from './Heading';
import { Link } from 'react-router-dom';
import { Component } from 'react';
import { reloadScrollEvents } from '../actions';
import ScrollToTop from './ScrollToTop';
import SmoothScroll from 'smooth-scroll';

export default class Article extends Component {
  constructor(props){
    super(props);
    this.state = {
      article: this.getArticle(),
      smoothScroll: new SmoothScroll()
    }
  }

  getArticle = () => {
    let { edition : { articles }, match: { params }} = this.props;
    return articles.find(a => a.slug == params.articleSlug);
  }

  componentWillMount(){
    //setTimeout(()=>{ this.state.smoothScroll.animateScroll(70, { speed: 600 }) }, 600 );
    //setTimeout(()=>{ window.scrollTo(0, 70); }, 150);
    window.scrollTo(0, 70)
    //this.props.dispatch(reloadScrollEvents());
  }

  render(){
    let { edition } = this.props;
    let { article } = this.state;
    return (
      <section className="weekly-article weekly-frame"
        dangerouslySetInnerHTML={{__html: article.post }}>
      </section>
    );
  }
}

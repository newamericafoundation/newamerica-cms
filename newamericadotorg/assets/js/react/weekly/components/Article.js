import Heading from './Heading';
import { Link } from 'react-router-dom';
import { Component } from 'react';
import { reloadScrollEvents } from '../actions';
import ScrollToTop from './ScrollToTop';

export default class Article extends Component {
  constructor(props){
    super(props);
    this.state = {
      article: this.getArticle()
    }
  }

  getArticle = () => {
    let { edition : { articles }, match: { params }} = this.props;
    return articles.find(a => a.slug == params.articleSlug);
  }

  componentWillMount(){
    window.scrollTo(0,75);
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

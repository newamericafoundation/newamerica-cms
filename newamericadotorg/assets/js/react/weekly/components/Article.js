import './Article.scss';

import Heading from './Heading';
import { Link } from 'react-router-dom';
import React, { Component } from 'react';
import { reloadScrollEvents } from '../actions';
import { connect } from 'react-redux';
import bowser from 'bowser';

class Article extends Component {
  constructor(props){
    super(props);
    this.state = {
      article: this.getArticle(),
      scrollPosition: 0
    }
  }

  componentDidMount(){
    if(window.scrollY > 135){
      if(bowser.safari) setTimeout(()=>{window.scrollTo(0, 71);},1);
      else window.scrollTo(0, 71);
    }
  }

  componentWillUpdate(prevProps){
    if(this.props.scrollPosition != 70 && this.state.scrollPosition != this.props.scrollPosition){
      this.setState({ scrollPosition: this.props.scrollPosition });
    }
  }

  getArticle = () => {
    let { edition : { articles }, match: { params }} = this.props;
    return articles.find(a => a.slug == params.articleSlug);
  }

  render(){
    let { edition } = this.props;
    let { article } = this.state;

    return (
      <section className="weekly-article weekly-frame" style={{ top: `${-this.state.scrollPosition + 65 + 70}px`}}
        dangerouslySetInnerHTML={{__html: article.post }}>
      </section>
    );
  }
}

const mapStateToProps = (state) => ({
  scrollPosition : state.site.scroll.position
});

export default Article = connect(mapStateToProps)(Article);

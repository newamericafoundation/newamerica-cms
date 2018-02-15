import Heading from './Heading';
import { Link } from 'react-router-dom';
import { Component } from 'react';
import { reloadScrollEvents } from '../actions';
import { connect } from 'react-redux';

class Article extends Component {
  constructor(props){
    super(props);
    this.state = {
      article: this.getArticle(),
      scrollPosition: 0
    }
  }

  componentWillMount(){
    if(window.scrollY > 135){
      window.scrollTo(0, 71);
    }
  }

  componentWillUpdate(prevProps){
    if(this.props.scrollPosition != 70 && this.state.scrollPosition != this.props.scrollPosition){
      this.setState({ scrollPosition: this.props.scrollPosition });
    }
      console.log(prevProps.scrollPosition);
      console.log(this.props.scrollPosition);
      console.log(this.state.scrollPosition);
      console.log('\n');
  }

  getArticle = () => {
    let { edition : { articles }, match: { params }} = this.props;
    return articles.find(a => a.slug == params.articleSlug);
  }

  render(){
    let { edition } = this.props;
    let { article } = this.state;
    //console.log(this.state.scrollPosition)
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

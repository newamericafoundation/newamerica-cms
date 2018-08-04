import getNestedState from '../../../utils/get-nested-state';
import { loadArticleImage, clearArticleImages } from '../actions';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';

class LoadingPage extends Component {
  start = new Date()
  componentWillMount(){
    this.state = {
      ready: false
    };
  }

  componentWillUpdate(props){
    if(props.isReady){
      let passedTime = new Date() - this.start
      if(passedTime>=5000) return this.setState({ ready: true });
      setTimeout(()=>{
        this.setState({ ready: true });
      }, 5000-passedTime);
    };
  }

  render(){
    if(!this.state.ready){
      return (
        <section className="weekly-loading">
          <div className="weekly-loading__text">
            <div className="weekly-loading__text__logo logo sm white"></div>
            <h4 className="weekly-loading__text__title">The Weekly</h4>
            <h1 className="weekly-loading__text__tagline">
              <span className="tagline-1">New ideas & voices in policy.</span>
              <span className="tagline-2">Delivered every Thursday.</span>
            </h1>
          </div>
        </section>
      );
    }

    return <Redirect to={`/weekly/${this.props.edition.slug}`}/>;
  }
}

const mapStateToProps = (state) => ({
  edition: getNestedState(state, 'weekly.edition.results'),
  images: getNestedState(state, 'weekly.edition.articleImages'),
  isReady: getNestedState(state, 'weekly.edition.isReady')
});

export default connect(mapStateToProps)(LoadingPage);

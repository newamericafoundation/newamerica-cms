import './StoryGrid.scss';

import React, { Component } from 'react';
import { connect } from 'react-redux';
import CardMd from './CardMd';
import CardLg from './CardLg';
import CardVariable from './CardVariable';
import { PromoMd } from './CardPromo';
import { Fetch } from '../../components/API';
import InfiniteLoadMore from '../../components/InfiniteLoadMore';
import { NAME } from '../constants';
import bowser from 'bowser';

const browser = bowser.getParser(window.navigator.userAgent);
const isValidBrowser = browser.satisfies({
  windows: {
    "internet explorer": ">9",
    "edge": ">12"
  },
  macos: {
    safari: ">10"
  },
  mobile: {
    safari: '>10.2'
  },
  chrome: ">49",
  firefox: ">51",
  opera: ">43"
});

const AboutCard = ({ program }) => (
  <PromoMd title="About" link={{ to: 'about', label: 'Read More'}}>
    <h2 className="margin-25">
      <span className="desktop-about-text" style={{whiteSpace: 'nowrap'}} dangerouslySetInnerHTML={{ __html: manualBreaks24(program.description).text}}/>
      <span className="tablet-about-text">
        {program.description.length > 270 ? program.description.slice(0,270) + ' ...' : program.description}
      </span>
      <span className="mobile-about-text">
        {program.description.length > 170 ? program.description.slice(0,170) + ' ...' : program.description}
      </span>
    </h2>
  </PromoMd>
);

class SubscribeCard extends Component {
  state = {
    email: null
  }

  render(){
    let { program } = this.props;
    let subText = program.subscription_card_text || `Be the first to hear about the latest events and research from ${program.name}`;

    return (
      <PromoMd title="Subscribe" link={{ to: `subscribe/?email=${this.state.email}`, label: 'Go'}}>
        <h2 className="margin-25">{subText}</h2>
        <div className="input">
          <input required type="text" name="email"
            onChange={(e)=>{this.setState({email: e.target.value})}}
            value={this.state.email||''} />
          <label className="input__label" htmlFor="email"><h5 className="margin-0">Email Address</h5></label>
        </div>
      </PromoMd>
    );
  }
}

class MoreStories extends Component {
  state = {
    rowHeight: 4
  }

  getMoreStories = () => {
    let { setQueryParam, fetchAndAppend, response, program, count, story_grid } = this.props;
    if((!response.hasNext && response.page !== 1) || count <= 7 || program.story_grid.pages.length > 7) return false;

    setQueryParam('page', response.page+1);
    return fetchAndAppend;
  }

  getCardRowSpan = (item) => {
    let { windowWidth } = this.props;
    let { rowHeight } = this.state;
    let imgSize, textSize;
    let len = item.title.length;

    if(len > 115) textSize = 150;
    else if(len > 75) textSize = 134;
    else if(len > 42) textSize = 114;
    else textSize = 96;

    if(!item.story_image) {
      imgSize = 0;
    } else {
      let ratio = item.story_image.height / item.story_image.width;
      imgSize = ratio * Math.min(1180/3 - 5, (windowWidth - 30)/3 - 5);
    }

    return Math.round((imgSize+textSize)/rowHeight);
  }

  renderGridItem = (item, i) => {
    let { rowHeight } = this.state;
    let padding = Math.round(10/rowHeight);
    let { program } = this.props;

    switch(item){
      case 'about':
        let aboutSpan = (manualBreaks24(program.description).lines * 30) + 152;
        aboutSpan = Math.max(400,Math.round(aboutSpan))
        aboutSpan = Math.round(aboutSpan/rowHeight) + padding;
        return (
          <div className="masonry__item" key={`mason-item-${i}`} style={{
            gridRowEnd: `span ${aboutSpan}`}}>
            <AboutCard program={program} />
          </div>
        );
      case 'subscribe':
        let subSpan = Math.round(400/rowHeight) + padding;
        return (
          <div className="masonry__item" key={`mason-item-${i}`} style={{
            gridRowEnd: `span ${subSpan}`}}>
            <SubscribeCard program={program} />
          </div>
        );
      default:
        let span = this.getCardRowSpan(item) + padding;
        return (
            <div className="masonry__item" key={`mason-item-${i}`} style={{
              gridRowEnd: `span ${span}`}}>
              <CardVariable post={item}/>
            </div>
        );
    }
  }

  render(){
    let { response, features, count } = this.props;
    return(
        <div className={`masonry ${!isValidBrowser ? 'disabled' : ''}`}>
          {features.map((p,i)=>(
            this.renderGridItem(p,i)
          ))}
          {response.results.map((f,i)=>(
            this.renderGridItem(f, `more-${i}`)
          ))}
          <InfiniteLoadMore
            onNextPage={this.getMoreStories}
            response={this.props.response}
            infiniteOnMount={true}
            showLoadingDots={false}
            bottomOffset={-400}/>
       </div>
    );
  }
}

const mapStateToProps = (state) => ({
  windowWidth: state.site.windowWidth
});

MoreStories = connect(mapStateToProps)(MoreStories);

export default class StoryGrid extends Component {

  render(){
    let { story_grid, loaded, program, programType } = this.props;

    let features = [...story_grid.pages];
    let lead = features.shift(0);
    features = ['subscribe', ...features.splice(0,3), 'about', ...features];

    if(story_grid.pages.length===0){
      return (
        <div className="program__story-grid">
          <div className="row gutter-10">
            <div className="col-12">
              <h1 className="margin-top-60">We're just getting started! <br/>Check back soon.</h1>
            </div>
          </div>
        </div>
      );
    }
    return (
      <div className="program__story-grid">
        <div className="row gutter-10">
          <div className="col-12">
            <CardLg post={lead} loaded={loaded}/>
          </div>
          <div className="col-12">
            <Fetch component={MoreStories}
              name={`${NAME}.featured`}
              renderGridItem={this.renderGridItem}
              count={story_grid.count}
              features={features}
              program={program}
              endpoint={`${programType}/${program.id}/featured`}
              initialQuery={{
                page_size: 7
              }}/>
          </div>
        </div>
      </div>
    );
  }
}

function manualBreaks24(text){
  let limit = window.innerWidth > 1125 ? 30 : 26;
  let len = text.length;
  let t = text.split('');
  let _t = [...t];
  let lastSpace = 0;
  let j = 1;
  let lines = 1;
  for(let i=1; i<t.length; i++){
    if(t[i]===' ') lastSpace = i;
    if(j%limit === 0){
      _t[lastSpace] = '&nbsp;<span class="br"></span>';
      j = 1;
      i = lastSpace + 1;
      lines++;
    }
    j++;
  }

  return {
    text: _t.join(''),
    lines
  }
}

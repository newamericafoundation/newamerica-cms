import './Reel.scss';

import React from 'react';
import Panel from './Panel';

export default class Reel extends Panel {

  constructor(props){
    super(props);
    let { data } = props;
    this.state = {
      len: data.paragraph.length+1,
      index: -1,
      pause: false
    }
  }

  componentDidMount(){
    this.nextFrame();
    this.play();
  }

  play = () => {
    setInterval(()=>{
      this.nextFrame();
    }, this.props.interval)
  }

  pause = () => {
    setTimeout(()=>{
      this.setState({
        pause: true,
        index: 0
      });
    }, 1200);

    setTimeout(()=>{
      this.setState({
        pause: false
      });
    }, 1500);
  }

  nextFrame = () => {
    let { len, index, offset } = this.state;
    let { data } = this.props;
    if(index >= len-2) this.pause();

    if(index >= len-1) index = 0;
    else index += 1;

    this.setState({
      index
    });
  }

  reelContent = (p,i) => {
    let { setHTML, data } = this.props;
    let { index } = this.state;
    if(setHTML)
      return (
        <div className={`home__reel__frame ${index===i ? 'active' : ''}`} key={`frame-${i}`}>
          <div className="home__reel__frame__wrapper" dangerouslySetInnerHTML={{__html: p }} />
        </div>
      );

    return (
      <div className={`home__reel__frame ${index===i ? 'active' : ''}`} key={`frame-${i}`}>
        <h1 className="margin-0">{this.parseHTMLText(p)}</h1>
      </div>
    );
  }

  render(){
    let { data, panelName='' } = this.props;
    let { index, pause, len} = this.state;
    return (
      <section className={`home__panel__promo scroll-target`} data-scroll-trigger-point="bottom" data-scroll-offset="10vh">
        <div className="container--1080">
          <div className={`row gutter-20 home__reel ${panelName}`}>
            <div className="col-md-6">
              <div className="home__panel__promo__text">
                <h1 className="promo margin-top-0 margin-bottom-15">{data.heading[0]}</h1>
                <p className="margin-bottom-35 margin-top-15">{this.parseHTMLText(data.introduction[0])}</p>
              </div>
            </div>
            <div className="col-md-5 push-md-1">
              <div className={`home__reel__frames ${pause ? 'pause' : ''}`} style={{top: `${-index * 100}%`}}>
                {data.paragraph.map((p,i)=>(
                  this.reelContent(p,i)
                ))}
                {this.reelContent(data.paragraph[0], len-1)}
              </div>
            </div>
          </div>
        </div>
      </section>
    );
  }
}

import './ImageAside.scss';

import Panel from './Panel';
import React from 'react';

export default class ImageAside extends Panel {
  render(){
    let { data, grayscale } = this.props;
    return (
      <section className="home__panel__image-aside padding-110 scroll-target" data-scroll-trigger-point="bottom" data-scroll-offset="10vh">
        <div className="container--1080">
          <div className="row gutter-20">
            <div className="col-md-6 home__panel__image-aside__image margin-bottom-35">
              <img src={data.inline_image[0].url} className={`${grayscale ? 'grayscale' : ''}`} />
            </div>
            <div className="col-md-5 push-md-1 home__panel__image-aside__text" >
              <div className="home__panel__image-aside__text__wrapper">
                <h1 className="margin-top-0 margin-bottom-25">{data.heading[0]}</h1>
                <p className="margin-bottom-0 margin-top-25">
                  {this.parseHTMLText(data.introduction[0])}
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    );
  }
}

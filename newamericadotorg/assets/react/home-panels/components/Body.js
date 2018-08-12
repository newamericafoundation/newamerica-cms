import './Body.scss';

import React from 'react';
import Panel from './Panel';

export default class Body extends Panel {
  render(){
    let { data, aside } = this.props;

    return (
      <section className="home__panel__body padding-80">
        <div className="container--1080">
          <div className="row gutter-20">
            <article className="col-md-7 post-body home__panel__body__text">
              {data.heading.map((h,i)=>(
                <div className="" key={`heading-${i}`}>
                  <h1 className="margin-top-0">{data.heading[i]}</h1>
                  <p dangerouslySetInnerHTML={{__html: data.paragraph[i]}} />
                  {this.props.children}
                </div>
              ))}
            </article>
            {(data.resource_kit || aside) &&
            <div className="col-md-4 push-md-1 margin-top-35 margin-top-md-0 home__panel__body__aside">
              {aside &&
                <div className="aside margin-bottom-25">
                  {aside}
                </div>
              }
              {data.resource_kit && <div className="aside">
                <h4 className="margin-top-0 margin-bottom-5">{data.resource_kit[0].title}</h4>
                <h6 className="margin-top-0 margin-bottom-25">{data.resource_kit[0].description}</h6>
                {data.resource_kit[0].resources.map((r,i)=>(
                  <div className="aside__item" key={`resource-${i}`}>
                    <h3 className="link"><a href={r.value.resource}><u>{r.value.name}</u></a></h3>
                    {r.value.description && <h6 className="margin-0">{this.parseHTMLText(r.value.description)}</h6>}
                  </div>
                ))}
              </div>}

            </div>}
          </div>
        </div>
      </section>
    );
  }
}

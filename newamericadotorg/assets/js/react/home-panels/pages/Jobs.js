import { Component } from 'react';
import { ImageAside, Reel, Body } from '../components';


export default class Jobs extends Component {

  render(){
    let { response: { results : { data } } } = this.props;
    let frame = data.job.iframe[0]
    return (
      <section className="home__panel__body">
        <div className="container--1080">
          <div className="row gutter-20">
            <article className="col-md-7 post-body home__panel__body__text">
              <iframe src={fram.source_url} />
            </article>
          </div>
        </div>
      </section>
    );
  }
}

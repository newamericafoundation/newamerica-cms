import { Component } from 'react';
import { Slider } from '../components/Carousel';

const NAME = 'inDepthSectionNav';
const ID = 'in-depth-section-nav';

class APP extends Component {

  render(){
    let { sections, currentSlide } = this.props;
    console.log(currentSlide);
    sections = JSON.parse(sections);
    return (
      <div className="in-depth-section-nav">
          <Slider
            initialSlide={+currentSlide}
            slidesToShow={4}
            slideToScroll={1}
            infinite={false}
            nextArrow={<div><label className="with-caret--right white"/></div>}
            prevArrow={<div><label className="with-caret--left white"/></div>}>
            {sections.map((s,i)=>(
              <div key={`section-${i}`}>
                <label className={`white centered${+currentSlide==i ? ' bold' : ''}`}>
                  <a href={s.url}>{s.title}</a>
                </label>
              </div>
            ))}
            <div />
          </Slider>
      </div>
    );
  }
}

export default { APP, ID, NAME };

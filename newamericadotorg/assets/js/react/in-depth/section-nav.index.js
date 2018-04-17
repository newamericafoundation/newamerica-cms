import { Component } from 'react';
import { Slider } from '../components/Carousel';
import { connect } from 'react-redux';

const NAME = 'inDepthSectionNav';
const ID = 'in-depth-section-nav';

class APP extends Component {
  goTo = (e) => {
    window.location = e.target.value;
  }
  render(){
    let { sections, currentSlide, windowWidth } = this.props;
    sections = JSON.parse(sections);

    if(windowWidth <= 768){
      return (
        <div className="in-depth__section__mobile-selector">
          <select onChange={this.goTo} className="in-depth__section__mobile-selector__select">
            {sections.map((s,i)=>(
              <option key={`section-${i}`} selected={+currentSlide==i} value={s.url}>{s.title}</option>
            ))}
          </select>
        </div>
      );
    }

    return (
      <div className="in-depth-section-nav">
          <Slider
            initialSlide={+currentSlide}
            slideToScroll={1}
            infinite={false}
            responsive={[
              {breakpoint: 960, settings: {slidesToShow: 2}},
              {breakpoint: 100000, settings: {slidesToShow: 3}}
            ]}
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

const mapStateToProps = (state) => ({
  windowWidth: state.site.windowWidth
});

APP = connect(mapStateToProps)(APP);

export default { APP, ID, NAME };

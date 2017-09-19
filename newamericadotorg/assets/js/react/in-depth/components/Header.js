import { Link } from 'react-router-dom';
import { Slider } from '../../components/Carousel';
import { Component } from 'react';

class SectionItem extends Component {
  constructor(props){
    super(props);
    this.state = { hover: false };
  }
  onEnter = () => {
    this.setState({ hover: true });
  }
  onLeave = () => {
    this.setState({ hover: false });
  }
  render(){
    let { i, s } = this.props;
    let { hover } = this.state;
    let mobile = window.innerWidth <= 860;
    let limit = mobile ? 36 : 17;
    return (
      <div onMouseEnter={this.onEnter} onMouseLeave={this.onLeave}>
        <Link to={s.url}>
          {(!hover || mobile) &&
            <label className="in-depth__header__section-list__item__text">
              {s.title.length > limit ? `${s.title.slice(0,limit)}...` : s.title}
            </label>}
          {(hover && !mobile) &&
            <label className="in-depth__header__section-list__item__text">
              {s.title}
            </label>}
        </Link>
      </div>
    );
  }
}

export default class Header extends Component {

  goTo = (index) => {
    this.refs.slider.slickGoTo(index);
  }

  render(){
    let { project, sectionIndex, match } = this.props;
    let goToIndex = window.innerWidth < 860 ? sectionIndex : Math.floor(sectionIndex/3)*3;
    if(this.refs.slider) this.goTo(goToIndex);
    return (
      <header className="in-depth__header">
        <div className="row">
          <div className="in-depth__header__project-title col-12 col-lg-auto">
            <a href="/">
              <div className="logo bug white in-depth-logo-bug sm"></div>
            </a>
            <label>
              <Link to={`${project.url}`}>{project.title}</Link>
            </label>
          </div>
          {match.params.sectionSlug != 'about' &&
            <div className="in-depth__header__section-list col-12 col-lg-auto">
            <Slider
              ref='slider'
              infinite={false}
              speed={500}
              slidesToShow={3}
              slidesToScroll={3}
              responsive={[
                { breakpoint: 860, settings: { slidesToShow: 1, slidesToScroll: 1, initialSlide: sectionIndex }}
              ]}
              prevArrow={<div><div></div></div>}
              nextArrow={<div><div></div></div>}>
              {project.sections.map((s,i)=>(
                <div className={`in-depth__header__section-list__item ${i===sectionIndex ? 'active' : ''} ${s.title.length > 17 ? 'long-text' : ''}`}>
                  <SectionItem s={s} i={i}/>
                </div>
              ))}
            </Slider>
          </div>}
        </div>
      </header>
    );
  }
}

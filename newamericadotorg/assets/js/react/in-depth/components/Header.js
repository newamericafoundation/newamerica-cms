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
    return (
      <div onMouseEnter={this.onEnter} onMouseLeave={this.onLeave}>
        <Link to={s.url}>
          {!hover &&
            <label className="in-depth__header__section-list__item__text">
              {s.title.length > 17 ? `${s.title.slice(0,17)}...` : s.title}
            </label>}
          {hover &&
            <label className="in-depth__header__section-list__item__text">
              {s.title}
            </label>}
        </Link>
      </div>
    );
  }
}


const Header = ({ project, sectionIndex, match }) => (
  <header className="in-depth__header">
    <div className="row">
      <div className="in-depth__header__project-title col-auto">
        <a href="/">
          <div className="logo bug white in-depth-logo-bug sm"></div>
        </a>
        <label>
          <Link to={`${project.url}`}>{project.title}</Link>
        </label>
      </div>
      {match.params.sectionSlug != 'about' &&
        <div className="in-depth__header__section-list col-auto">
        <Slider
          infinite={false}
          speed={500}
          slidesToShow={3}
          slidesToScroll={3}
          initialSlide={Math.floor(sectionIndex/3)*3}
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

export default Header;

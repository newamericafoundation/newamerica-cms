import { Link } from 'react-router-dom';
import { Slider } from '../../components/Carousel';

const Header = ({ project, sectionIndex, match }) => (
  <header className="in-depth__header">
    <div className="row">
      <div className="in-depth__header__project-title col-auto">
        <a href="/">
          <div className="logo bug white in-depth-logo-bug sm"></div>
        </a>
        <label>
          <Link to={project.url}>{project.title}</Link>
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
            <div className={`in-depth__header__section-list__item ${i===sectionIndex ? 'active' : ''}`}>
              <Link draggable={false} to={s.url}>
                <label className="in-depth__header__section-list__item__text">
                  {s.title.length > 25 ? `${s.title.slice(0,25)}...` : s.title}
                </label>
              </Link>
            </div>
          ))}
        </Slider>
      </div>}
    </div>
  </header>
);

export default Header;

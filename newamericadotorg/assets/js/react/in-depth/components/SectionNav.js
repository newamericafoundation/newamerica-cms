import { Link } from 'react-router-dom';

const SectionNav = ({ sections, currentIndex }) => (
  <div className="in-depth__section-nav">
    {currentIndex > 0 &&
      <div className="in-depth__section-nav__prev">
        <label className="in-depth-label block">Previous</label>
        <Link to={sections[currentIndex-1].url}>
          <label className="margin-0">{sections[currentIndex-1].title}</label>
        </Link>
      </div>
    }{currentIndex < sections.length-1 &&
      <div className="in-depth__section-nav__next">
        <label className="in-depth-label block">Next</label>
        <Link to={sections[currentIndex+1].url}>
          <label className="margin-0">{sections[currentIndex+1].title}</label>
        </Link>
      </div>
    }
  </div>
);

export default SectionNav;

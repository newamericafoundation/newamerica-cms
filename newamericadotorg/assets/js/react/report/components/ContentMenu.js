import { Link } from 'react-router-dom';

const ContentMenu = ({ report: { url, sections }, open, closeMenu, activeSection }) => (
  <div className={`report__content-menu ${open ? 'open' : ''}`}>
    {sections.map((s,i)=>(
      <div className={`report__content-menu__item ${activeSection==s ? 'active' : ''}`} onClick={closeMenu}>
        <Link to={`${url}${s.slug}`}>
          <label className="white">{`${s.number}. ${s.title}`}</label>
        </Link>
      </div>
    ))}
  </div>
);

export default ContentMenu;

import { Link } from 'react-router-dom';

const ContentMenu = ({ report: { url, sections }, open, closeMenu }) => (
  <div className={`report__content-menu ${open ? 'open' : ''}`}>
    {sections.map((s,i)=>(
      <div className="report__content-menu__item" onClick={closeMenu}>
        <Link to={`${url}${s.slug}`}>
          <label className="white">{`${s.number}. ${s.title}`}</label>
        </Link>
      </div>
    ))}
  </div>
);

export default ContentMenu;

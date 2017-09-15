import { Link } from 'react-router-dom';

const Contents = ({ sections }) => (
  <div className="in-depth__contents">
    <label className="in-depth-label">Contents</label>
    <ul className="in-depth__table-of-contents">
    {sections.map((s,i)=>(
      <li>
        <h4 className="no-margin"><Link to={s.url}>{s.title}</Link></h4>
        <p className="no-margin">{s.story_excerpt}</p>
      </li>
    ))}
    </ul>
  </div>
);

export default Contents;

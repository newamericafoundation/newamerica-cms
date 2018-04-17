import { Link } from 'react-router-dom';

const Contents = ({ sections }) => (
  <div className="in-depth__contents">
    <label className="in-depth-label">Contents</label>
    <ul className="in-depth__table-of-contents">
    {sections.map((s,i)=>(
      <li>
        <h4 className="margin-0"><Link to={s.url}>{s.title}</Link></h4>
        <p className="margin-0">{s.story_excerpt}</p>
      </li>
    ))}
    </ul>
  </div>
);

export default Contents;

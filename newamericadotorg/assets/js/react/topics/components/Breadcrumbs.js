import { Link } from 'react-router-dom';

const Breadcrumbs = ({ topic, ancestors }) => (
  <section className="container--wide">
    <div className="breadcrumbs">
      <label className="breadcrumbs__item">
        <a href={topic.program.url}>{topic.program.title}</a>
      </label>
      <label className="breadcrumbs__item">
        <a href={`${topic.program.url}/topic/`}>Topic</a>
      </label>
      {ancestors.map((a,i)=>(
        <label className="breadcrumbs__item">
          <Link to={ a.url }>{ a.title }</Link>
        </label>
      ))}
    </div>
  </section>
);

export default Breadcrumbs;

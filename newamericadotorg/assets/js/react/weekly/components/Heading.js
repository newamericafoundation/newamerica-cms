import { format as formatDate } from 'date-fns';
const Heading = ({ post : { authors, title, url, story_image, date } }) => (
  <section className="container--medium weekly-heading">

    <div className='weekly-heading__text row'>
      <div className="weekly-heading__text__title">
        <h1 className="narrow-margin">{title}</h1>
      </div>
      <div className="weekly-heading__text__date-author-wrapper">
        <label className="weekly-heading__text__date">
          {formatDate(date, 'MMMM D, YYYY')}
        </label>
      {authors.length &&
        <label className="active weekly-heading__text__author">
          <a href={authors[0].url}>{authors[0].first_name} {authors[0].last_name}</a>
        </label>
      }
      </div>
    </div>
    <div className="weekly-heading__image-wrapper row">
      <div className='weekly-heading__image'
        style={{ backgroundImage: `url(${story_image})`}}></div>
    </div>

  </section>
);

export default Heading;

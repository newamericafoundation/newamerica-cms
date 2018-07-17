import { format as formatDate } from 'date-fns';
const Heading = ({ post : { authors, title, url, story_image, date } }) => (
  <section className="container--medium weekly-heading">

    <div className='weekly-heading__text'>
      <div className="weekly-heading__text__title">
        <h1 className="margin-5">{title}</h1>
      </div>
      <div className="weekly-heading__text__date-author-wrapper">
        <h6 className="weekly-heading__text__date inline">
          {formatDate(date, 'MMMM D, YYYY')}
        </h6>
      {authors.length &&
        <h6 className="active weekly-heading__text__author inline">
          <a href={authors[0].url}>{authors[0].first_name} {authors[0].last_name}</a>
        </h6>
      }
      </div>
    </div>
    <div className="weekly-heading__image-wrapper">
      <div className='weekly-heading__image'
        style={{ backgroundImage: `url(${story_image})`}}></div>
    </div>

  </section>
);

export default Heading;

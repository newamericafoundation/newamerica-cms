const Heading = ({ page, post : { authors, title, url, story_image } }) => (
  <section className="container--full-width weekly-heading">
    <div className={`weekly-heading__image with-overlay--black ${page}`}
      style={{ backgroundImage: `url(${story_image})`}}></div>

    <div className="weekly-heading__lead-story container--wide">
      <div className={`weekly-heading__lead-story__text row ${page}`}>
        {authors.length &&
          <label className="active weekly-heading__lead-story__text__author">
            By <a href={authors[0].url}>{authors[0].first_name} {authors[0].last_name}</a>
          </label>
        }
        <div className="weekly-heading__lead-story__text__title">
          <h1 className="narrow-margin">{title}</h1>
        </div>
      </div>
    </div>

    <div className={`weekly-heading__also-in-this-edition ${page}`}>
      <label className="active lg">Also In This Edition <i className="fa fa-arrow-down sm"></i></label>
    </div>
  </section>
);

export default Heading;

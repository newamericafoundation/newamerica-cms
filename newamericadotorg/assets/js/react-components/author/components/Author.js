const Image = ({ author: { profile_image }}) => (
  <div className="author__image-wrapper">
    <div className="author__image" style={{ backgroundImage: `url(${profile_image})` }}></div>
  </div>
);

const Text = ({ author: { url, short_bio, first_name, last_name, position }}) => (
  <div className="author__text">
    <a href={url} className="author__link-wrapper">
      {short_bio &&
        <div className="author__text__short-bio" dangerouslySetInnerHTML={{__html: short_bio }}></div>
      }
      <p className="author__text__name">
        {first_name + ' ' + last_name}
      </p>
      <label className="author__text__position">
        {position}
      </label>
    </a>
  </div>
);

const Author = ({ author, classes }) => (
  <div className={`author ${classes} ${author.profile_image ? 'with-image' : ''}`}>
    <div className='row no-gutters'>
      {author.profile_image &&
        <Image author={author} />
      }
      <Text author={author} />
    </div>
  </div>
);

export default Author;

import { format as formatDate } from 'date-fns';
import Image from './Image'

export const Person = ({ person }) => (
  <div className="card person">
    <a href={person.url}>
      <div className={`card__image ${!person.profile_image ? 'no-image' : ''}`}>
        {person.profile_image &&
          <Image image={person.profile_image} />}
      </div>
      <div className="card__text">
        <h3 className="card__text__title">{person.first_name} {person.last_name}</h3>
        <label className="caption block">{person.position}</label>
      </div>
    </a>
  </div>
);


export const EventItem = ({ event }) => (
  <div className="card event-card">
    <a href={event.url}>
      <div className={`card__image ${!event.story_image ? 'no-image' : ''}`}>
        <Image image={event.story_image} />
      </div>
    </a>
    <div className="card__text">
      <a href={event.url}>
        <label className="margin-top-0 block">{formatDate(event.date, 'MMM. Do, YYYY')}</label>
        <h3 className="card__text__title bold block">{event.title}</h3>
        <label className="subtitle block">{event.story_excerpt}</label>
        <label className="caption block">{event.city}, {event.state}</label>
      </a>
      <label className="event__rsvp button--text block margin-0">
        <a className="with-caret" href={event.url}>RSVP</a>
      </label>
    </div>
  </div>
);

const punctuation = (i, authors) => {
  let len = authors.length;
  if(i == len-2 && len > 2)
    return (<span className="punc">&nbsp;, &&nbsp;</span>);
  if(i == len-2 && len>1)
    return (<span className="punc">&nbsp;&nbsp;&&nbsp;</span>);
  if(i != len-1)
    return (<span className="punc">&nbsp;,&nbsp;</span>)

}

export const PublicationListItem = ({ post }) => (
  <div className={`card list ${post.content_type ? post.content_type.api_name : ''}`}>
    <a href={post.url}>
      <div className={`card__image ${!post.story_image ? 'no-image' : ''}`}>
        <Image image={post.story_image} />
      </div>
      </a>
    <div className="card__text">
      <a href={post.url}>
        <label className="card__text__date margin-top-0 block">{formatDate(post.date, 'MMM. Do, YYYY')}</label>
        <h3 className="card__text__title bold block">{post.title}</h3>
      </a>
      {post.authors &&
      <label className="card__text__authors link subtitle">
        {post.authors.map((a, i)=>(
          <span className="subtitle inline" key={`author-${i}`}>
            <a href={a.url}>{a.first_name} {a.last_name}</a>
            {punctuation(i, post.authors)}
          </span>
        ))}
      </label>}
      <a href={post.url}>
        {post.programs &&
        <label className="card__text__program caption margin-bottom-0 block">
          {post.programs[0] ? post.programs[0].name : ''} {post.content_type ? post.content_type.name : ''}
        </label>}
      </a>
    </div>
  </div>
);

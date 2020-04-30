import React from 'react';

import { format as formatDate, parseISO } from 'date-fns/esm';
import Image from './Image';

export const Person = ({ person }) => (
  <div className="card person">
    <a href={person.url}>
      <div className={`card__image ${!person.profile_image ? 'no-image' : ''}`}>
        {person.profile_image && <Image image={person.profile_image} />}
      </div>
      <div className="card__text">
        {/* <h3 className="card__text__title">{person.first_name} {person.last_name}</h3> */}
        <h4 className="card__text__title margin-10">
          <span>
            <u>
              {person.first_name} {person.last_name}
            </u>
          </span>
        </h4>
        <div className="h6 caption margin-10">{person.position}</div>
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
        <div className="h6 margin-0">
          {formatDate(parseISO(event.date), 'MMM. do, yyyy')}
        </div>
        {/* <h3 className="card__text__title bold block">{event.title}</h3> */}
        <h4 className="card__text__title margin-10">
          <span>
            <u>{event.seo_title || event.title}</u>
          </span>
        </h4>
        <div className="h6 margin-10">{event.story_excerpt}</div>
        <div className="h6 caption margin-0">
          {event.online_only ? 'Online Only' : [event.city, event.state ].filter(e => e).join(', ')}
        </div>
      </a>
      <div className="h6 event__rsvp button--text link margin-0">
        <a className="with-caret" href={event.rsvp_link} target="_blank" rel="noopener noreferrer">
          <u>RSVP</u>
        </a>
      </div>
    </div>
  </div>
);

const punctuation = (i, len) => {
  if (i == len - 2 && len > 2)
    return (
      <div className="h6 inline margin-0" key={`punc-${i}`}>
        , and&nbsp;
      </div>
    );
  if (i == len - 2 && len > 1)
    return (
      <div className="h6 inline margin-0" key={`punc-${i}`}>
        &nbsp;and&nbsp;
      </div>
    );
  if (i != len - 1)
    return (
      <div className="h6 inline margin-0" key={`punc-${i}`}>
        ,&nbsp;
      </div>
    );

  return false;
};

const generateAuthors = authors => {
  let authorElements = [];
  let len = authors.length;
  let _authors = [...authors];
  if (len > 3) _authors = authors.splice(0, 3);
  _authors.forEach((a, i) => {
    authorElements.push(
      <div className="h6 inline link margin-0" key={`author-${i}`}>
        <a href={a.url}>
          <u>
            {a.first_name} {a.last_name}
          </u>
        </a>
      </div>
    );
    let punc = punctuation(i, len);
    if (punc) authorElements.push(punc);
  });

  if (len === 4)
    authorElements.push(<div className="h6 inline bold"> {len - 3} more</div>);
  else if (len > 4)
    authorElements.push(<div className="h6 inline bold">and {len - 3} more</div>);

  return authorElements;
};

export const PublicationListItem = ({ post }) => (
  <div
    className={`card list ${
      post.content_type ? `card--${post.content_type.api_name}` : ''
    }`}
  >
    <a href={post.url}>
      <div className={`card__image ${!post.story_image ? 'no-image' : ''}`}>
        <Image image={post.story_image} />
      </div>
    </a>
    <div className="card__text">
      <a href={post.url}>
        {post.date && (
          <div className="h6 card__text__date margin-top-0 margin-bottom-5 margin-bottom-md-15">
            {formatDate(parseISO(post.date), 'MMM. do, yyyy')}
          </div>
        )}
        <h4 className="card__text__title margin-0">
          <span>
            <u>{post.seo_title || post.title}</u>
          </span>
        </h4>
        {post.story_excerpt && (
          <div className="h6 margin-top-5 margin-bottom-0 card__text__excerpt">
            {post.story_excerpt}
          </div>
        )}
      </a>

      {post.authors && (
        <div className="card__text__authors margin-top-5 margin-bottom-0">
          {post.authors.length > 0 && (
            <span>
              <div className="h6 inline margin-0">By:&nbsp;</div>
              {generateAuthors(post.authors)}
            </span>
          )}
        </div>
      )}
      {post.programs && (
        <div className="h6 card__text__program caption margin-top-5 margin-top-md-15 margin-bottom-0">
          {post.programs[0] ? post.programs[0].name : ''}{' '}
          {post.content_type ? post.content_type.name : ''}
        </div>
      )}
    </div>
  </div>
);

import { format as formatDate } from 'date-fns';

const RSVP = () => (
  <div className="event-list__item__rsvp">
    <span className="event-list__item__rsvp__text">
      <i className="fa fa-ticket"></i> Now Available
    </span>
  </div>
)

const Image = ({ event: { story_image }, hasRSVP }) => (
  <div className="portrait-content-grid__item__image-wrapper">
    <img className="portrait-content-grid__item__image" src={story_image}/>
    {hasRSVP && <RSVP/>}
  </div>
);

const DummyImage = () => (
  <div className="portrait-content-grid__item__image-wrapper dummy-image">
    <i className="portrait-content-grid__item__no-image fa fa-calendar"></i>
    <svg className="portrait-content-grid__item__image" width="200px" height="290px"></svg>
  </div>
);

const Title = ({title}) => (
  <label className="active portrait-content-grid__item__text__heading">
    {title}
  </label>
)

const Programs = ({programs}) => (
  <label className="block portrait-content-grid__item__text__programs">
    {programs.map((p,i)=>(
      <span key={`program=${i}`}>
        <a href={p.url}>{p.name}</a>
        {i<programs.length-2 && ', '}
        {i==programs.length-2 && ' and '}
      </span>
    ))}
  </label>
)

const Time = ({startDate, endDate}) => (
  <label className= "block portrait-content-grid__item__text__date">
    <span className="block event-list__item__text__date__wrap">
      {formatDate(startDate, 'MMMM D, YYYY')}
    </span>
    {(endDate>startDate && endDate!=startDate) &&
      <span>{' - '}
        <span className="event-list__item__text__date__wrap">
          {formatDate(endDate, 'MMMM D, YYYY')}
        </span>
      </span>
    }
  </label>
)

const Location = ({city, state}) => (
  <label className="block portrait-content-grid__item__text__location">
    <i className="fa fa-map-marker no-padding sm"></i> {city}, {state}
  </label>
)

const Text = ({event: { title, programs, projects, date, end_date, city, state }}) => (
  <div className="portrait-content-grid__item__text">
    <Title title={title} />
    {programs && <Programs programs={programs} />}
    {date && <Time startDate={date} endDate={end_date} />}
    {(city&&state) && <Location city={city} state={state} />}
  </div>
);

export default ({ item, cols, hasRSVP }) => (
  <div
    className={`portrait-content-grid__item event-list__item ${cols} ${item.story_image ? ' with-image' : ''}`}>
    <a href={item.url} className="portrait-content-grid__item__link-wrapper">
      {item.story_image && <Image event={item} hasRSVP={hasRSVP}/>}
      {!item.story_image && <DummyImage />}
      <Text event={item} />
    </a>
  </div>
);

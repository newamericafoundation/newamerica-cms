import { format as formatDate } from 'date-fns';

const RSVP = () => (
  <div className="event-list__item__rsvp">
    <span className="event-list__item__rsvp__text">
      <i className="fa fa-ticket"></i> Now Available
    </span>
  </div>
);

const Programs = ({programs}) => (
  <div className="portrait-content-grid__item__text__programs">
    {programs.map((p,i)=>(
      <label key={`program=${i}`}>
        <a href={p.url}>{p.name}</a>
        {i<programs.length-2 && ', '}
        {i==programs.length-2 && ' and '}
      </label>
    ))}
  </div>
);

const Image = ({ event: { story_image, date, programs }}) => (
  <div className="portrait-content-grid__item__image-wrapper">
    <img className="portrait-content-grid__item__image" src={story_image}/>
    {/* {(new Date(date)>=new Date()) && <RSVP/>} */}
  </div>
);

const DummyImage = ({ event: { programs }}) => (
  <div className="portrait-content-grid__item__image-wrapper dummy-image">
    <i className="portrait-content-grid__item__no-image fa fa-calendar"></i>
    <svg className="portrait-content-grid__item__image" width="200px" height="290px"></svg>
    {programs && <Programs programs={programs} />}
  </div>
);

const Title = ({title}) => (
  <label className="portrait-content-grid__item__text__heading md active">
    {title}
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
    <i className="fa fa-map-marker no-padding xs"></i> {city}, {state}
  </label>
)

const Text = ({event: { title, programs, projects, date, end_date, city, state }}) => (
  <div className="portrait-content-grid__item__text">
    {date && <Time startDate={date} endDate={end_date} />}
    <Title title={title} />
    {programs && <Programs programs={programs} />}
    {(city&&state) && <Location city={city} state={state} />}
  </div>
);

export default ({ item, cols }) => (
  <div
    className={`portrait-content-grid__item event-list__item ${cols} ${item.story_image ? ' with-image' : ''}`}>
    <a href={item.url} className="portrait-content-grid__item__link-wrapper">
      {item.story_image && <Image event={item}/>}
      {!item.story_image && <DummyImage event={item} />}
      <Text event={item} />
    </a>
  </div>
);

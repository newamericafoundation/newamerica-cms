import { format as formatDate } from 'date-fns';

const Image = ({ event: { story_image }}) => (
  <div className="portrait-content-grid__item__image-wrapper">
    <img className="portrait-content-grid__item__image" src={story_image}/>
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
    <Time startDate={date} endDate={end_date} />
    <Location city={city} state={state} />
  </div>
)

export default ({ event, colxl2 }) => (
  <div
    className={`portrait-content-grid__item event-list__item col-4 col-md-3 ${colxl2 ? ' col-xl-2': ''} ${event.story_image ? ' with-image' : ''}`}>
    <a href={event.url} className="portrait-content-grid__item__link-wrapper">
      <DummyImage />
      {event.story_image && <Image event={event} />}

      <Text event={event} />
    </a>
  </div>
);

import { format as formatDate } from 'date-fns';

const Image = ({ event: { story_image }}) => (
  <div className="portrait-content-grid__item__image-wrapper">
    <img className="portrait-content-grid__item__image" src={story_image}/>
  </div>
);

const DummyImage = () => (
  <div className="portrait-content-grid__item__image-wrapper">
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
    { formatDate(startDate, 'MMMM D, YYYY') + (endDate ? ' - ' + formatDate(endDate, 'MMMM D, YYYY') : '') }
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

export default ({ event }) => (
  <div className={`portrait-content-grid__item col-sm-6 col-md-4 col-lg-3 col-xl-2 ${event.story_image ? ' with-image' : ''}`}>
    <a href={event.url} className="portrait-content-grid__item__link-wrapper">
      {event.story_image && <Image event={event} />}
      {!event.story_image && <DummyImage />}
      <Text event={event} />
    </a>
  </div>
);

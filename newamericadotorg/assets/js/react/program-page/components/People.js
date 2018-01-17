import { Component } from 'react';
import { Fetch } from '../../components/API';

const Person = ({ person }) => (
  <div className="card person">
    <a href={person.url}>
      <div className={`card__image ${!person.profile_image ? 'no-image' : ''}`}>
        {person.profile_image &&
          <img src={person.profile_image} />}
      </div>
      <div className="card__text">
        <h3 className="card__text__title">{person.first_name} {person.last_name}</h3>
        <label className="caption block">{person.position}</label>
      </div>
    </a>
  </div>
);

class PersonsList extends Component {

  render(){
    let { response : { results, isFetching } } = this.props;
    return (
      <div className="program__people__list row gutter-10">
        {results.map((person, i) => (
          <div className="col-md-4 col-12">
            <Person person={person} />
          </div>
        ))}
      </div>
    );
  }
}

export default class People extends Component {
  render(){
    let { program } = this.props;
    return (
      <Fetch name="program.people"
        endpoint="author"
        component={PersonsList}
        fetchOnMount={true}
        initialQuery={{
          program_id: program.id,
          limit: 100
        }}/>
    );
  }
}

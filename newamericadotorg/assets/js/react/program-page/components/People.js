import { NAME } from '../constants';
import { Component } from 'react';
import { Fetch } from '../../components/API';
import Image from '../../components/Image';

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

export class PersonsList extends Component {

  render(){
    let { response : { results, isFetching }, children } = this.props;
    if(results.length===0) return null;
    return (
      <div className="program__people__list row gutter-10">
        {children}
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
    let { program, programType } = this.props;
    return (
      <Fetch name={`${NAME}.people`}
        endpoint="author"
        component={PersonsList}
        fetchOnMount={true}
        initialQuery={{
          [programType == 'program' ? 'program_id' : 'subprogram_id']: program.id,
          limit: 100
        }}/>
    );
  }
}

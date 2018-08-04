import './PeopleCarousel.scss';

import React, { Component } from 'react';
import Promo from './CardPromo';
import { Slider } from '../../components/Slider';
import { Arrow } from '../../components/Icons';

const Person = ({ person }) => (
  <div className="promo__people-carousel__person">
    <div className="promo__people-carousel__person__image">
      <img className="promo__people-carousel__person__image__background" src={person.profile_image} />
    </div>
    <div className="promo__people-carousel__person__text">
      <h3 className="margin-top-0">{person.first_name} {person.last_name}</h3>
      <h6 className="caption">{person.position}</h6>
      <h6>{person.description}</h6>
    </div>
  </div>
);

export default class PeopleCarousel extends Component {
  render(){
    let { response : { results } } = this.props;
    if(results.length === 0) return null;
    let persons = results.map((p,i)=>( <div><Person person={p} /></div>));
    return(
      <Promo title="Our People">
        <div className="promo__people-carousel">
          <Slider
            infinite={true}//results.length > 1}
            speed={500}
            slidesToShow={1}
            slidesToScroll={1}
            prevArrow={<div className="slider-arrow--left"><Arrow direction="left"/></div>}
            nextArrow={<div className="slider-arrow--right"><Arrow direction="right"/></div>}>
            {persons}
          </Slider>
        </div>
      </Promo>
    );
  }
}

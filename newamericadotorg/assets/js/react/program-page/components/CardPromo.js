import { Component } from 'react';
import { Slider } from '../../components/Carousel';
import { Link } from 'react-router-dom';

export class Promo extends Component {

  render(){
    let { title } = this.props;

    return (
      <div className="card promo row gutter-0">
        <div className="promo__heading col-2">
          <label className="block button--text white margin-top-0">{title}</label>
        </div>
        <div className="card__text col-10">
          {this.props.children}
        </div>
      </div>
    );
  }
}

export class PromoMd extends Component {
  render(){
    let { title, link : { label, to }} = this.props;

    return (
      <div className="card promo-md">
        <div className="card__text">
          <label className="block margin-top-0">{title}</label>
          {this.props.children}
        </div>
        <div className="card__link-to">
          <label className="button--text with-caret--right">
            <Link to={to}>{label}</Link>
          </label>
        </div>
      </div>
    );
  }
}

const Person = ({ person }) => (
  <div className="promo__people-carousel__person">
    <div className="promo__people-carousel__person__image">
      <img className="promo__people-carousel__person__image__background" src={person.profile_image} />
    </div>
    <div className="promo__people-carousel__person__text">
      <h3 className="margin-top-0">{person.first_name} {person.last_name}</h3>
      <label className="block caption">{person.position}</label>
      <label className="block">{person.description}</label>
    </div>
  </div>
);


export class PeopleCarousel extends Component {
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
            prevArrow={<div className="slider-arrow--left"><i className="fa fa-long-arrow-left"/></div>}
            nextArrow={<div className="slider-arrow--right"><i className="fa fa-long-arrow-right"/></div>}>
            {persons}
          </Slider>
        </div>
      </Promo>
    );
  }
}

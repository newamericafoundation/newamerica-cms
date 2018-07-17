import { Component } from 'react';
import { Slider } from '../../components/Carousel';
import { Link } from 'react-router-dom';
import { Arrow } from '../../components/Icons';

export class Promo extends Component {

  render(){
    let { title, linkTo } = this.props;

    return (
      <div className="card promo row gutter-0">

          <div className="promo__heading col-12 col-lg-2">
            {linkTo && <Link to={linkTo}>
              <h5 className="white margin-0">{title}</h5>
            </Link>}
            {!linkTo &&
              <h5 className="white margin-0">{title}</h5>
            }
          </div>

          <div className="card__text col-12 col-lg-10">
            {linkTo && <Link to={linkTo}>
              {this.props.children}
            </Link>}
            {!linkTo && this.props.children}
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
          <h6 className="margin-top-0">{title}</h6>
          {this.props.children}
        </div>
        <div className="card__link-to">
          <Link to={to} className="button--text link with-caret--right">
            {label}
          </Link>
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
      <h6 className="caption">{person.position}</h6>
      <h6>{person.description}</h6>
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
            prevArrow={<div className="slider-arrow--left"><Arrow direction="left"/></div>}
            nextArrow={<div className="slider-arrow--right"><Arrow direction="right"/></div>}>
            {persons}
          </Slider>
        </div>
      </Promo>
    );
  }
}
